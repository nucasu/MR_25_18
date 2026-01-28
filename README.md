# Integration of Hydra with the TurtleBot3 simulation

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

4. Return to the host system terminal:
```bash
exit
``` 

5. Modify Docker file in `hydra_ws/src/hydra_ros/docker/minimal/docker-compose.yml` by adding `- /tmp/.X11-unix:/tmp/.X11-unix` in the `volumes` section and `ipc: host` as the last line of the code, in order to enable communication with the ROS workspace and support graphical visualization.

6. Build the Hydra workspace environment:
```bash
cd hydra_ws/src/hydra_ros/docker
make build PROFILE=minimal
make up PROFILE=minimal
make shell PROFILE=minimal
MAKEFLAGS="-j2" colcon build --parallel-workers 2
```

7. Return to the host system terminal:
```bash
exit
cd -
``` 

## Simulation

1. Run Hydra:
```bash
./run_hydra.sh
source install/setup.bash
ros2 launch hydra_tb3 hydra_tb3.launch.yaml
```
> RViz2 will start with an empty visualization window.

2. Open a new terminal and launch the TurtleBot3 simulation:
```bash
./run.sh
source install/setup.bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo turtlebot3_house.launch.py
```
> Gazebo will start, showing the TurtleBot navigating inside the house, while the scene graph is generated in real time in the RViz2 window.

3. After the robot finishes navigating the environment, terminate the process and save the generated scene graph by pressing `Ctrl + C` in both terminals. All the components of the scene graph will be saved in `hydra_ws/house_scene_graph`.

## Project structure

- `docker_ws/`: Docker files and scripts to build docker images for ROS workspace
- `hydra_ws/`: Hydra workspace
- `ros_ws/`: ROS 2 workspace
- `chown_me.sh`: bash script to change the owner of files from root to user
- `run.sh`: bash script to run ROS container
- `exec.sh`: bash script to open a shell to an already running ROS container
- `run_hydra.sh`: bash script to run ROS container
