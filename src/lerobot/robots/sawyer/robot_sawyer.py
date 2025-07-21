from lerobot.robots import Robot
from lerobot.robots.sawyer.configuration_sawyer import SawyerRobotConfig
from lerobot.cameras.utils import make_cameras_from_configs
import rospy
import intera_interface

class SawyerRobot(Robot):
    config_class = SawyerRobotConfig
    name = "sawyer"

    def __init__(self, config: SawyerRobotConfig):
        super().__init__(config)
        rospy.init_node('enable_sawyer')
        rs = intera_interface.RobotEnable(intera_interface.CHECK_VERSION)
        rs.enable()
        print("Robot enabled!")
        self.limb = intera_interface.Limb('right')
        self.robot_enable = intera_interface.RobotEnable()
        self._is_connected = False
        self.cameras = make_cameras_from_configs(config.cameras)

    @property
    def observation_features(self):
        # Static description of joint angles + cameras
        features = {name: float for name in self.limb.joint_names()}
        for cam_key, cam in self.cameras.items():
            features[cam_key] = (cam.height, cam.width, cam.channels)
        return features

    @property
    def action_features(self):
        # Same as observation_features for position control (joints only)
        return {name: float for name in self.limb.joint_names()}

    def connect(self, calibrate=True):
        self.robot_enable.enable()
        for cam in self.cameras.values():
            cam.connect()
        self._is_connected = True

    def disconnect(self):
        for cam in self.cameras.values():
            cam.disconnect()
        self._is_connected = False

    def get_observation(self):
        if not self._is_connected:
            raise RuntimeError("Sawyer is not connected.")
        obs = self.limb.joint_angles()
        for cam_key, cam in self.cameras.items():
            obs[cam_key] = cam.async_read()
        return obs

    def send_action(self, action):
        if not self._is_connected:
            raise RuntimeError("Sawyer is not connected.")
        
        #need an if else or sth
        self.limb.set_joint_positions(action)
        return action
        
        # Ignore the input action, just return the current joint angles
        #return self.limb.joint_angles()

    # Required abstract methods/properties
    @property
    def is_connected(self):
        return self._is_connected

    @property
    def is_calibrated(self):
        return True  # No calibration needed for Sawyer

    def calibrate(self):
        pass  # No calibration needed for Sawyer

    def configure(self):
        pass  # No special configuration needed for Sawyer

'''
if __name__ == "__main__":
    from configuration_sawyer import SawyerRobotConfig
    import time

    # Create config (edit ip_address if needed)
    config = SawyerRobotConfig(ip_address="192.168.XXX.XXX")
    robot = SawyerRobot(config)
    print("Connecting to Sawyer...")
    robot.connect()
    print("Connected.")

    print("Current joint angles:")
    obs = robot.get_observation()
    print(obs)

    # Send current position as a test action (no movement)
    print("Sending current joint angles as action...")
    robot.send_action(obs)
    print("Action sent.")

    time.sleep(1)
    print("Disconnecting...")
    robot.disconnect()
    print("Disconnected.")
'''