import torchvision
from object_detection.processing import get_model

CARS_RCNN_MODEL = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
DEFECTS_MODEL = None
# get_model("model/mobilenetv2_80_3_cl.dict")
