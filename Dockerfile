FROM ntklab/monoped_rl:latest

SHELL ["/bin/bash", "-c"]

ENV PATH="/root/miniconda3/bin:$PATH"

RUN conda init bash && \
    conda create -n d4pg python=3.10 -y && \
    source /root/miniconda3/etc/profile.d/conda.sh && \
    conda activate d4pg && \
    git config --global url."https://github.com/".insteadOf "git://github.com/" && \
    pip install dm-acme[tf,jax] && \
    pip uninstall -y tensorflow-datasets tensorflow-metadata && \
    pip install \
        rospkg pyyaml "protobuf<3.21" gym "numpy<2" dm_control && \
    pip install \
        nvidia-cuda-runtime-cu11==11.7.99 \
        nvidia-cudnn-cu11==8.6.0.163 \
        nvidia-cublas-cu11 \
        nvidia-cufft-cu11 \
        nvidia-curand-cu11 \
        nvidia-cusolver-cu11 \
        nvidia-cusparse-cu11

COPY ./my_hopper_training/ /root/monoped_ws/src/my_hopper_training/
RUN chmod +x /root/monoped_ws/src/my_hopper_training/src/d4pg.py

RUN echo "source /root/miniconda3/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate d4pg" >> ~/.bashrc && \
    echo "export LD_LIBRARY_PATH=/opt/ros/noetic/lib:/opt/ros/noetic/lib/x86_64-linux-gnu:\$LD_LIBRARY_PATH" >> ~/.bashrc && \
    echo "export LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:\$CONDA_PREFIX/lib" >> ~/.bashrc && \
    echo "export LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:\
/root/miniconda3/envs/d4pg/lib/python3.10/site-packages/nvidia/cuda_runtime/lib:\
/root/miniconda3/envs/d4pg/lib/python3.10/site-packages/nvidia/cublas/lib:\
/root/miniconda3/envs/d4pg/lib/python3.10/site-packages/nvidia/cudnn/lib:\
/root/miniconda3/envs/d4pg/lib/python3.10/site-packages/nvidia/cufft/lib:\
/root/miniconda3/envs/d4pg/lib/python3.10/site-packages/nvidia/curand/lib:\
/root/miniconda3/envs/d4pg/lib/python3.10/site-packages/nvidia/cusolver/lib:\
/root/miniconda3/envs/d4pg/lib/python3.10/site-packages/nvidia/cusparse/lib" >> ~/.bashrc && \
    echo "source /opt/ros/noetic/setup.sh" >> ~/.bashrc && \
    echo "source /root/monoped_ws/devel_isolated/setup.sh" >> ~/.bashrc

WORKDIR /root/monoped_ws/src/my_hopper_training/src
