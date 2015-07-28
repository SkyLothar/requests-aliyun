__version__ = "0.2.4"
__author__ = "SkyLothar"
__email__ = "allothar@gmail.com"
__url__ = "http://github.com/skylothar/requests-aliyun"

from .ecs import EcsAuth
from .oss import OssAuth
from .rds import RdsAuth
from .slb import SlbAuth
from .cms import CmsAuth


__all__ = ["EcsAuth", "OssAuth", "RdsAuth", "SlbAuth", "CmsAuth"]
