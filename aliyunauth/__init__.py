__version__ = "0.1.2"
__author__ = "SkyLothar"
__email__ = "allothar@gmail.com"
__url__ = "http://github.com/skylothar/requests-aliyun"

from .ecs import EcsAuth
from .oss import OssAuth
from .rds import RdsAuth


__all__ = ["EcsAuth", "OssAuth", "RdsAuth"]
