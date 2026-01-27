# MR_25_18 – Integration of Hydra with the TurtleBot3 simulation

The objective of this project is to map an environment within the TurtleBot3 simulation by acquiring sensors data and using Hydra to reconstruct a 3D map generating a scene graph.

## Requirements

- Docker
- ROS 2 Jazzy

## Installation

1. Clone the repository including all submodules:

```bash
git clone --recurse-submodules https://github.com/nucasu/MR_25_18.git
cd MR_25_18
```

2. Set execution permissions for the project scripts:
   
```bash
chmod +x chown_me.sh exec.sh run.sh run_hydra.sh docker_ws/build_MR_25_18.sh
```

3. Build the ROS workspace environment:
```bash
./docker_ws/build_MR_25_18.sh
./run.sh
colcon build --symlink-install
```

4. Exit the Docker container and return to the host system terminal:
```bash
exit
``` 

5. Build the Hydra workspace environment::
```bash

```

This starts a `hydra-minimal` container with the workspace mounted at `/root/hydra_ws`.

## Building the workspace inside the container

Inside the container:
```bash
docker exec -it hydra-minimal bash
```
undefined
```bash
cd /root/hydra_ws
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
MAKEFLAGS="-j2" colcon build --parallel-workers 2 --symlink-install --continue-on-error
```

For every new shell:
```bash
cd /root/hydra_ws
source install/setup.bash
```

## Usage – Hydra with TurtleBot3 in simulation

1. (Optional) Start the TurtleBot3 simulation in Gazebo **inside the container** or from another ROS 2 environment that shares the same network and `ROS_DOMAIN_ID`.

Example (if TurtleBot3 is installed in the container):
```bash
export TURTLEBOT3_MODEL=waffle_pi
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

2. Launch Hydra-ROS:
```bash
cd /root/hydra_ws
source install/setup.bash

ros2 launch hydra_ros hydra.launch.yaml
dataset:=<dataset_name>
labelspace:=<labelspace_name>
start_visualizer:=true
start_rviz:=true
```

Choose `dataset` and `labelspace` among:

- `install/hydra/share/hydra/config/datasets/`
- `install/hydra_ros/share/hydra_ros/config/datasets/`
- `install/hydra/share/hydra/config/label_spaces/`

3. Check the topics:
```bash
ros2 topic list
```

Configure the YAML files in `hydra_ros/config/datasets/` so that the topic names (depth, odom, TF, etc.) match those published by TurtleBot3/Gazebo.

## Project structure

- `ros_ws/` – ROS 2 workspace  
  - `src/hydra/` – Hydra core (scene graph engine)  
  - `src/hydra_ros/` – ROS 2 interface and Docker launch files  
  - other packages: Kimera, spark_dsg, etc.  
- `ros_ws/src/hydra_ros/docker/` – Dockerfile, `docker-compose.yml`, Makefile (`build`, `run`, …)  
- `MR_25_18/` – Project-specific configuration, scripts and documentation
