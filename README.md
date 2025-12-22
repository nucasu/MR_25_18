# MR_25_18 – Hydra + TurtleBot3

Workspace ROS 2 che integra Hydra-ROS con TurtleBot3 (reale o in simulazione) per costruire una **scene graph 3D** a partire dai dati della depth camera e dell’odometria.

## Requisiti

- ROS 2 Jazzy (su Ubuntu 24.04 o immagine Docker `osrf/ros:jazzy-desktop`) 
- Docker + Docker Compose installati sull’host
- Git + vcstool (`vcs`) per gestire i repository ROS 
- Scheda grafica/X11 configurato se vuoi usare RViz/Gazebo dal container 

## Installazione

1. Clona il repository:

cd ~
git clone https://github.com/nucasu/MR_25_18.git MR_25_18
cd MR_25_18

2. Inizializza il workspace ROS 2 e i pacchetti esterni (Hydra, Kimera, ecc.):

cd ros_ws/src
vcs import . < hydra_ros/install/ros2_docker.yaml

3. Costruisci l’immagine Docker di sviluppo (Hydra + ROS 2):

cd ~/MR_25_18/ros_ws/src/hydra_ros/docker
make build PROFILE=minimal

4. Avvia il container:

make run PROFILE=minimal

Questo crea un container `hydra-minimal` con il workspace montato in `/root/hydra_ws`. 

## Build del workspace nel container

Dentro al container:

docker exec -it hydra-minimal bash

cd /root/hydra_ws
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
MAKEFLAGS="-j2" colcon build --parallel-workers 2 --symlink-install --continue-on-error

Ogni nuova sessione:

cd /root/hydra_ws
source install/setup.bash

## Uso – Hydra con TurtleBot3 in simulazione

1. (Opzionale) Lancia la simulazione TurtleBot3 in Gazebo **dentro il container** o da un altro ambiente ROS 2 che condivida la rete e il `ROS_DOMAIN_ID`. 

   Esempio (se hai TurtleBot3 installato nel container):

export TURTLEBOT3_MODEL=waffle_pi
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py

2. Lancia Hydra-ROS:

cd /root/hydra_ws
source install/setup.bash

ros2 launch hydra_ros hydra.launch.yaml
dataset:=<nome_dataset>
labelspace:=<nome_labelspace>
start_visualizer:=true
start_rviz:=true


Scegli `dataset` e `labelspace` tra quelli presenti in:

- `install/hydra/share/hydra/config/datasets/`
- `install/hydra_ros/share/hydra_ros/config/datasets/`
- `install/hydra/share/hydra/config/label_spaces/` 

3. Verifica i topic:

ros2 topic list

Configura i file YAML in `hydra_ros/config/datasets/` in modo che i nomi dei topic (depth, odom, TF, ecc.) coincidano con quelli pubblicati da TurtleBot3/Gazebo. 

## Struttura del progetto

- `ros_ws/` – Workspace ROS 2
- `src/hydra/` – Core Hydra (scene graph engine)
- `src/hydra_ros/` – Interfaccia ROS 2 e launcher Docker
- altri pacchetti: Kimera, spark_dsg, ecc.
- `ros_ws/src/hydra_ros/docker/` – Dockerfile, `docker-compose.yml`, Makefile (`build`, `run`, …)
- `MR_25_18/` – Configurazioni, script e documentazione specifici del progetto
