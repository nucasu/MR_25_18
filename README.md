Ecco il tuo README tradotto in inglese e con i blocchi di comandi sistemati in Markdown.

text
# MR_25_18 – Hydra + TurtleBot3

ROS 2 workspace that integrates Hydra-ROS with TurtleBot3 (real or simulated) to build a **3D scene graph** from depth camera and odometry data. [web:7][web:193]

## Requirements

- ROS 2 Jazzy (on Ubuntu 24.04 or Docker image `osrf/ros:jazzy-desktop`) [web:200]
- Docker + Docker Compose installed on the host
- Git + vcstool (`vcs`) to manage ROS repositories [web:7]
- GPU / X11 configured if you want to use RViz/Gazebo from inside the container [web:205]

## Installation

1. Clone the repository:

```bash
cd ~
git clone https://github.com/nucasu/MR_25_18.git MR_25_18
cd MR_25_18
Initialize the ROS 2 workspace and external packages (Hydra, Kimera, etc.):

bash
cd ros_ws/src
vcs import . < hydra_ros/install/ros2_docker.yaml
Build the development Docker image (Hydra + ROS 2):

bash
cd ~/MR_25_18/ros_ws/src/hydra_ros/docker
make build PROFILE=minimal
Start the container:

bash
make run PROFILE=minimal
This starts a hydra-minimal container with the workspace mounted at /root/hydra_ws. [web:7]

Building the workspace inside the container
Inside the container:

bash
docker exec -it hydra-minimal bash
bash
cd /root/hydra_ws
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
MAKEFLAGS="-j2" colcon build --parallel-workers 2 --symlink-install --continue-on-error
For every new shell:

bash
cd /root/hydra_ws
source install/setup.bash
Usage – Hydra with TurtleBot3 in simulation
(Optional) Start the TurtleBot3 simulation in Gazebo inside the container or from another ROS 2 environment that shares the same network and ROS_DOMAIN_ID. [web:93][web:194]

Example (if TurtleBot3 is installed in the container):

bash
export TURTLEBOT3_MODEL=waffle_pi
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
Launch Hydra-ROS:

bash
cd /root/hydra_ws
source install/setup.bash

ros2 launch hydra_ros hydra.launch.yaml \
  dataset:=<dataset_name> \
  labelspace:=<labelspace_name> \
  start_visualizer:=true \
  start_rviz:=true
Choose dataset and labelspace among:

install/hydra/share/hydra/config/datasets/

install/hydra_ros/share/hydra_ros/config/datasets/

install/hydra/share/hydra/config/label_spaces/ [web:7]

Check the topics:

bash
ros2 topic list
Configure the YAML files in hydra_ros/config/datasets/ so that the topic names (depth, odom, TF, etc.) match those published by TurtleBot3/Gazebo. [web:74]

Project structure
ros_ws/ – ROS 2 workspace

src/hydra/ – Hydra core (scene graph engine)

src/hydra_ros/ – ROS 2 interface and Docker launch files

other packages: Kimera, spark_dsg, etc.

ros_ws/src/hydra_ros/docker/ – Dockerfile, docker-compose.yml, Makefile (build, run, …)

MR_25_18/ – Project-specific configuration, scripts and documentation

text

Se vuoi, nel prossimo passo si può aggiungere una sezione “Known issues / tips” con i problemi che hai incontrato (memoria, `CMakeCache`, ecc.).