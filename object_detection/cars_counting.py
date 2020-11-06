import cv2
import torch
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torch import tensor
import numpy as np
from PIL import Image


def detect_auto(model, image):
    # переводим модель в тестовый режим
    model = model.eval()
    # загружаем картинку со стандартным преобразованием цветов
    img_numpy = image[:,:,::-1]
    # преобразуем картинку в torch тензор 
    img = torch.from_numpy(img_numpy.astype('float32')).permute(2,0,1)
    # приводим масштаб цветов к (0. , 1.)
    img = img / 255.
    # нейросеть предсказывает, что находится на картинке и обводит распознанные обьекты рамкой
    predictions = model(img[None,...])
    # print(predictions)
    return predictions


def intersection_over_union(boxA, boxB):
    """ intersection over union"""
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    interArea = max(0, xB - xA + 1.) * max(0, yB - yA + 1.)
    boxAArea = (boxA[2] - boxA[0] + 1.) * (boxA[3] - boxA[1] + 1.)
    boxBArea = (boxB[2] - boxB[0] + 1.) * (boxB[3] - boxB[1] + 1.)
    iou = float(interArea) / float(boxAArea + boxBArea - interArea)
    return iou


def intersection_over_b_area(boxA, boxB):
    """ intersection over area 2"""
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    interArea = max(0, xB - xA + 1.) * max(0, yB - yA + 1.)
    boxBArea = (boxB[2] - boxB[0] + 1.) * (boxB[3] - boxB[1] + 1.)
    return float(interArea)/float(boxBArea)


def plot_non_max_suppression(numpy_img, preds, label, color):
    """ non max suppression + duplicates suppression"""
    def suppress(box, boxes, indexes):
        print([intersection_over_union(box, boxes[i]) for i in indexes])
        ious_50 = [i for i in indexes if(intersection_over_union(box, boxes[i]) >= 0.50)]
        duplicates = [i for i in indexes if(intersection_over_b_area(box, boxes[i]) >= 0.91)]
        print(duplicates)
        for i in set(duplicates).union(set(ious_50)):
            indexes.remove(i)
        return 

    labels = preds['labels'].detach().numpy()
    scores = preds['scores'].detach().numpy()
    boxes = preds['boxes'].detach().numpy()[(labels == label) & (scores >= 0.55)]
    
    indexes = list(np.arange(len(boxes)))
    result_boxes = []
# 
    while len(indexes) > 0:
        #
        box = boxes[indexes[0]]
        indexes.remove(indexes[0])
        # 
        suppress(box, boxes, indexes)
        result_boxes.append(box)

    nimg = cv2.UMat(numpy_img)
    for box in result_boxes:
        nimg = cv2.rectangle(nimg, 
            (box[0], box[1]),
            (box[2], box[3]), 
            color = color,
            thickness = 2)
    return (result_boxes, nimg.get())


def get_all_boxes(image, predictions):
    """ all boxes"""
    colors = [(255, 0, 0),
         (0, 255, 0),
         (0, 0, 255)]
    all_boxes = []
    counts = []
    color = 0
    for label in [3, 6, 8]:
        img_with_boxes = plot_non_max_suppression(image, predictions[0], label, colors[color])
        color += 1
        image = img_with_boxes[1]
        all_boxes.extend(img_with_boxes[0])
        counts.append(len(img_with_boxes[0]))
    print(all_boxes)
    return (all_boxes, image, counts)


def detect_all_autos(model, fname):
    img_numpy = cv2.imread(fname)[:,:,::-1]
    print("in count_cars: stage 1")
    predictions = detect_auto(model, img_numpy)
    print("stage 2")
    result = get_all_boxes(img_numpy, predictions)
    print("stage3")
    counts = result[2]
    msg = f"Общее количество машин на фото {len(result[0])} (Всего автомобилей {counts[0]}, всего автобусов {counts[1]}, всего грузовиков {counts[2]})"
    img_array = result[1].astype('uint8')
    im = Image.fromarray(img_array, 'RGB')
    out_file = fname.split('.')[0] + "_file.jpg"
    im.save(out_file)
    im.close()
    return (len(result[0]), msg, out_file)
