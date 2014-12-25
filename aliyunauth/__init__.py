__version__ = "0.1.0"
__author__ = "SkyLothar"
__email__ = "allothar@gmail.com"
__url__ = "http://github.com/skylothar/requests-aliyun"

from .oss import OssAuth
from .ecs import EcsAuth


__all__ = ["EcsAuth", "OssAuth"]
