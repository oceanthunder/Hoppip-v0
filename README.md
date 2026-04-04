# Hoppip-v0
Distributed Distributional DDPG (D4PG) training for a one-legged hopper robot (Monoped-V0) in Gazebo/ROS, using Acme and Reverb, so that it jumps!


https://github.com/user-attachments/assets/b699f626-6673-437c-92aa-38b9d0b3d77a


## Architecture
![Block Image](assets/block.png)

## Setup
Pull the docker image:
```bash
docker pull oceanthunder/hoppip-v0:latest
```

Run the image:
```bash
xhost +local:root

docker run -it \
    --rm \
    --gpus all \
    --name hoppip-v0 \
	-p 6006:6006 \
    --privileged \
    --env=DISPLAY \
    --env=QT_X11_NO_MITSHM=1 \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    oceanthunder/hoppip-v0 \
    /bin/bash
```

Launch the Gazebo simulation:
```bash
export LD_LIBRARY_PATH=/opt/ros/noetic/lib:/opt/ros/noetic/lib/x86_64-linux-gnu
roslaunch my_legged_robots_sims main.launch
```

In a new terminal:
```bash
docker exec -it hoppip-v0 /bin/bash
```

Train using D4PG:
```bash
roslaunch my_hopper_training d4pg.launch
```

## Configs
If you want to use TD3/SAC/A2C, modify the start_training_v2.py file inside my_hopper_training/src and then run:
```bash
roslaunch my_hopper_training main.launch
```

If you want to tweak the rewards, modify the file at /root/monoped_ws/src/my_hopper_training/config/learn_params.yaml
