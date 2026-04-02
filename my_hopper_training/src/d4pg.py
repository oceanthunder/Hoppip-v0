#!/usr/bin/env python3
from typing import Callable, Dict, Sequence, Union

from absl import app
from absl import flags
from acme import specs
from acme.agents.tf import d4pg
import helpers
from acme.tf import networks
from acme.tf import utils as tf2_utils
import launchpad as lp
import numpy as np
import sonnet as snt
import tensorflow as tf
import rospy

FLAGS = flags.FLAGS
_MAX_ACTOR_STEPS = flags.DEFINE_integer(
    'max_actor_steps', None,
    'Number of actor steps to run; defaults to None for an endless loop.')


def make_networks(
    action_spec: specs.BoundedArray,
    policy_layer_sizes: Sequence[int] = (256, 256, 256),
    critic_layer_sizes: Sequence[int] = (512, 512, 256),
    vmin: float = -1000.,
    vmax: float = 10000.,
    num_atoms: int = 51,
) -> Dict[str, Union[snt.Module, Callable[[tf.Tensor], tf.Tensor]]]:
    num_dimensions = np.prod(action_spec.shape, dtype=int)

    policy_network = snt.Sequential([
        networks.LayerNormMLP(policy_layer_sizes, activate_final=True),
        networks.NearZeroInitializedLinear(num_dimensions),
        networks.TanhToSpec(action_spec)
    ])
    critic_network = snt.Sequential([
        networks.CriticMultiplexer(),
        networks.LayerNormMLP(critic_layer_sizes, activate_final=True),
        networks.DiscreteValuedHead(vmin, vmax, num_atoms),
    ])

    return {
        'policy': policy_network,
        'critic': critic_network,
        'observation': tf2_utils.batch_concat,
    }


def main(_):
    rospy.init_node('acme_d4pg_monoped', anonymous=True, log_level=rospy.INFO)

    def env_factory(evaluation: bool):
        return helpers.make_env(evaluation=evaluation)

    program_builder = d4pg.DistributedD4PG(
        environment_factory=env_factory,
        network_factory=make_networks,
        max_actor_steps=_MAX_ACTOR_STEPS.value,
        num_actors=1,
        min_replay_size=1000,   
        batch_size=256,
        discount=0.99,
        n_step=5,
        sigma=0.3,  
        log_every=10.0,  
    )

    lp.launch(programs=program_builder.build())


if __name__ == '__main__':
    app.run(main)

