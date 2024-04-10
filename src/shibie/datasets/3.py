import os
import cv2
import json
import random
import shutil

def get_polygon_annotations(txt_path, class_names):
    with open(txt_path, 'r') as file:
        lines = file.readlines()
    annotations = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) != 11:  # 每个对象应该有1个类别名和5个坐标（x, y），总共11个值
            continue
        # 类别名和多边形坐标
        class_id = class_names.index(parts[0]) + 1  # 类别ID
        polygon = [float(point) for point in parts[1:]]  # 转换为 [x1, y1, x2, y2, ..., x5, y5]
        annotations.append((polygon, class_id))
    return annotations

def generate_keypoints(polygon):
    # 生成COCO格式的关键点信息
    keypoints = []
    for i in range(0, len(polygon), 2):
        keypoints.extend([polygon[i], polygon[i+1], 2]) # 2表示该关键点是可见的
    return keypoints

data_path = 'data/'
output_dir = 'coco/'
jsons_path = os.path.join(output_dir, 'annotations/')
train_imgs_path = os.path.join(output_dir, 'images/')
val_imgs_path = train_imgs_path

if not os.path.exists(output_dir):
    os.makedirs(jsons_path)
    os.makedirs(train_imgs_path)

class_names = [line.rstrip('\n') for line in open(os.path.join(data_path, 'class_names.txt'))]
train_test_split = 0.8

train_data = {
    'info': {},
    'licenses': [],
    'images': [],
    'annotations': [],
    'categories': [{'supercategory': 'none', 'id': i+1, 'name': cls} for i, cls in enumerate(class_names)]
}

val_data = {
    'info': {},
    'licenses': [],
    'images': [],
    'annotations': [],
    'categories': [{'supercategory': 'none', 'id': i+1, 'name': cls} for i, cls in enumerate(class_names)]
}

imgs_list = sorted([file for file in os.listdir(data_path) if file.split('.')[-1] in ['jpg', 'png']])
random.shuffle(imgs_list)

img_id = 1
ann_id = 1

for img in imgs_list:
    img_path = os.path.join(data_path, img)
    w, h, _ = cv2.imread(img_path).shape
    txt_path = os.path.join(data_path, img.split('.')[0] + '.txt')
    annotations = get_polygon_annotations(txt_path, class_names)
    if random.random() > train_test_split:  # Assign to validation set
        out_img_path = os.path.join(val_imgs_path, img)
        shutil.copyfile(img_path, out_img_path)
        val_data['images'].append({'id': img_id, 'width': w, 'height': h, 'file_name': img})
        dataset = val_data
    else:  # Assign to training set
        out_img_path = os.path.join(train_imgs_path, img)
        shutil.copyfile(img_path, out_img_path)
        train_data['images'].append({'id': img_id, 'width': w, 'height': h, 'file_name': img})
        dataset = train_data

    for polygon, class_id in annotations:
        keypoints = generate_keypoints(polygon)
        dataset['annotations'].append({
            'id': ann_id,
            'image_id': img_id,
            'category_id': class_id,
            'segmentation': [polygon],
            'area': 0,  # Optionally calculate the actual area
            'bbox':[min(polygon[0::2]), min(polygon[1::2]), max(polygon[0::2]) - min(polygon[0::2]), max(polygon[1::2]) - min(polygon[1::2])],
            'iscrowd': 0,
            'keypoints': keypoints,
            'num_keypoints': len(keypoints) // 3
        })
        ann_id += 1
    img_id += 1

with open(os.path.join(jsons_path, 'instances_train2017.json'), 'w') as json_file:
    json.dump(train_data, json_file)

with open(os.path.join(jsons_path, 'instances_val2017.json'), 'w') as json_file:
    json.dump(val_data, json_file)