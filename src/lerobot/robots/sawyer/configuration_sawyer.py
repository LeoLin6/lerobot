from dataclasses import dataclass, field
from lerobot.cameras import CameraConfig
from lerobot.cameras.opencv import OpenCVCameraConfig
from lerobot.robots import RobotConfig

@RobotConfig.register_subclass("sawyer")
@dataclass
class SawyerRobotConfig(RobotConfig):
    #ip_address: str = "192.168.XXX.XXX"  # Sawyer's IP or connection info
    cameras: dict[str, CameraConfig] = field(default_factory=dict)


