# Sawyer Robot Integration for LeRobot

This folder contains the integration code for using the Sawyer robot arm with the LeRobot framework.

## Prerequisites

- **Sawyer robot** with Intera 5.x firmware
- **Development workstation** running Ubuntu 16.04 LTS (recommended)
- **ROS Kinetic** installed and working
- **Intera SDK** installed and working
- **LeRobot** installed in your Python environment

## Environment Setup

Before running any Python code that uses the Sawyer robot (including LeRobot scripts), you **must** source the Intera/ROS environment so that all required environment variables are set. This is done using the `intera.sh` script provided by the Intera SDK.

https://github.com/RethinkRobotics/intera_sdk

### 1. Open a terminal

### 2. Source the Intera/ROS environment

```
cd ~/ros_ws
source ./intera.sh
```

- This sets up `ROS_MASTER_URI`, `ROS_IP`, `PYTHONPATH`, and other required variables.
- You must do this **in every terminal** before running any code that communicates with the robot.

### 3. Run your LeRobot Python script

```
huggingface-cli login --token "insert ur token here" --add-to-git-credential


python -m lerobot.record \
    --robot.type=sawyer \
    --robot.id=my_sawyer \
    --teleop.type=keyboard \
    --teleop.id=my_keyboard \
    --dataset.repo_id=${HF_USER}/record-test \
    --dataset.num_episodes=5 \
    --dataset.single_task="Grab the black cube"
```

Replay Script:
```
python -m lerobot.replay \
    --robot.type=sawyer \
    --robot.id=my_sawyer \
    --dataset.repo_id=${HF_USER}/record-test2 \
    --dataset.episode=0 # choose the episode you want to replay
```

Or, if using Jupyter, start Jupyter **after** sourcing `intera.sh`:

```
jupyter notebook
```

## NumPy Version Requirement for ROS/Intera

**If you are using LeRobot with ROS Noetic and the Intera SDK, you must use NumPy 1.x.**

ROS Noetic and its Python/C++ bindings (like `cv_bridge`, `intera_interface`, etc.) are not compatible with NumPy 2.x as of mid-2024. Using NumPy 2.x will cause errors like `_ARRAY_API not found` or crashes in ROS/Intera code.

### How to Downgrade NumPy

**With pip:**
```
pip install 'numpy<2'
```

**With conda:**
```
conda install numpy=1.26
```

This will not break LeRobot, and is required for stable operation with ROS/Intera.

## Troubleshooting: Common Import Errors

### 1. `ModuleNotFoundError: No module named 'lerobot'`

If you see this error when running a script directly, you may need to set your `PYTHONPATH` so Python can find the LeRobot source code:

```
export PYTHONPATH=$PYTHONPATH:/path/to/lerobot-main/src
```
Replace `/path/to/lerobot-main` with the actual path to your LeRobot repository.

### 2. `ModuleNotFoundError: No module named 'intera_interface'`

This means your ROS/Intera environment is not sourced. Make sure you have run:

```
cd ~/ros_ws
source ./intera.sh
```

in the same terminal session before running your script.

### 3. `ModuleNotFoundError: No module named 'rospkg'` (or other ROS Python packages)

If you see this error, you need to install the missing ROS Python packages in your current Python environment:

```
pip install rospkg catkin_pkg
```
If you see errors for other missing packages (like `rosgraph`, `rosparam`, etc.), install them similarly:

```
pip install <package_name>
```

## Minimal Example

```python
from lerobot.robots.sawyer.robot_sawyer import SawyerRobot
from lerobot.robots.sawyer.configuration_sawyer import SawyerRobotConfig

config = SawyerRobotConfig(ip_address="192.168.XXX.XXX")
robot = SawyerRobot(config)
robot.connect()
obs = robot.get_observation()
print(obs)
```

## References
- [LeRobot Integrate Hardware Tutorial](https://huggingface.co/docs/lerobot/integrate_hardware)
- [Rethink Robotics Sawyer SDK Documentation](https://github.com/RethinkRobotics/sawyer_robot) 