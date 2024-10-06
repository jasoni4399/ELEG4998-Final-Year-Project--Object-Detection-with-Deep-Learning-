import logging
from enum import Enum

logger: logging.Logger = logging.getLogger(__name__)


class MethodAveragePrecision(Enum):
    EVERY_POINT_INTERPOLATION=1
    ELEVENT_POINT_INTERPOLATION=2

class CoordinatesType(Enum):
    RELATIVE=1
    ABSOLUTE=2

class BBType(Enum):
    GROUND_TRUTH=1
    DETECTED=2

class BBFormat(Enum):
    XYWH=1
    XYX2Y2=2
    PASCAL_XML=3
    YOLO=4

class FileFormat(Enum):
    ABSOLUTE_TEXT=1
    PASCAL=2
    LABLE_ME=3
    COCO=4
    CVAT=5
    YOLO=6
    OPENIMAGE=7
    IMAGENET=8
    UNKNOWN=9