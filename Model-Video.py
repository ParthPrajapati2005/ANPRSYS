import os

import matplotlib
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util
import cv2
from matplotlib import pyplot as plt
import numpy as np
import easyocr
import OCRNEW
import csv
import uuid

CUSTOM_MODEL_NAME = 'myssdmobnet'
#CUSTOM_MODEL_NAME = 'myssdmobnet'
#PRETRAINED_MODEL_NAME = 'ssd_mobilenet_v2_fpnlite_640x640_coco17_tpu-8'
#PRETRAINED_EXTRACT_NAME = 'ssd_mobilenet_v2_fpnlite_640x640_coco17_tpu-8'
#PRETRAINED_MODEL_URL = 'http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_mobilenet_v2_fpnlite_640x640_coco17_tpu-8.tar.gz'
CUSTOM_MODEL_NAME = 'mymobnetssd'
PRETRAINED_MODEL_NAME = 'ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8'
PRETRAINED_EXTRACT_NAME = 'ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8'
PRETRAINED_MODEL_URL = 'http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8.tar.gz'
TF_RECORD_SCRIPT_NAME = 'generate_tfrecord.py'
LABEL_MAP_NAME = 'label_map.pbtxt'

paths = {
    'WORKSPACE_PATH': os.path.join('Tensorflow', 'workspace'),
    'SCRIPTS_PATH': os.path.join('Tensorflow','scripts'),
    'APIMODEL_PATH': os.path.join('Tensorflow','models'),
    'ANNOTATION_PATH': os.path.join('Tensorflow', 'workspace','annotations'),
    'IMAGE_PATH': os.path.join('Tensorflow', 'workspace','images'),
    'MODEL_PATH': os.path.join('Tensorflow', 'workspace','models'),
    'PRETRAINED_MODEL_PATH': os.path.join('Tensorflow', 'workspace','pre-trained-models'),
    'CHECKPOINT_PATH': os.path.join('Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME),
    'OUTPUT_PATH': os.path.join('Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME, 'export'),
    'TFJS_PATH':os.path.join('Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME, 'tfjsexport'),
    'TFLITE_PATH':os.path.join('Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME, 'tfliteexport'),
    'PROTOC_PATH':os.path.join('Tensorflow','protoc')
 }

files = {
    'PIPELINE_CONFIG':os.path.join('Tensorflow', 'workspace','models', CUSTOM_MODEL_NAME, 'pipeline.config'),
    'TF_RECORD_SCRIPT': os.path.join(paths['SCRIPTS_PATH'], TF_RECORD_SCRIPT_NAME),
    'LABELMAP': os.path.join(paths['ANNOTATION_PATH'], LABEL_MAP_NAME)
}

#Limit GPU Memory
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
       tf.config.experimental.set_virtual_device_configuration(
            gpus[0], [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=2000)])
    except RuntimeError as e:
       print(e)

# Load pipeline config and build a detection model
configs = config_util.get_configs_from_pipeline_file(files['PIPELINE_CONFIG'])
detection_model = model_builder.build(model_config=configs['model'], is_training=False)

# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join(paths['CHECKPOINT_PATH'], 'ckpt-16')).expect_partial()

##################################################

#Easy OCR Function
def detect_text(image):
    detection_threshold = 0.7 #Only OCR detections above this threshold will be outputted

    scores = list(filter(lambda x: x> detection_threshold, detections['detection_scores'])) #Filters through the detections array for values that are only above threshold
    boxes = detections['detection_boxes'][:len(scores)] #Filter through the amount of detected boxes by the amount of scores that have passed the threshold
    classes = detections['detection_classes'][:len(scores)] #Filter classes by amount of scores that passed threshold
                                                            # Class 0 = frontRegistrationPlate
                                                            # Class 1 = backRegistrationPlate

    #Note : The variable image is the WHOLE image NOT the Region of Interest- NumPlate

    height = image.shape[0]  #Get height of whole image
    width = image.shape[1]   #Get width of whole image


    # Apply Region of Interest filtering - Crop the image into the Number Plate section

    for idx, box in enumerate(boxes): #Loop through every box
        roi = box * [height, width, height, width]    # Box coordinates are not with respect to actual size of image so multipy to get actual coords
        region = image[int(roi[0]):int(roi[2]),int(roi[1]):int(roi[3])] # Plot ROI Coords onto whole image - Crop
        #reader = easyocr.Reader(['en'])                                 # Read text from extracted region

        #Save Image to directory

        img_name = '{}.jpg'.format(uuid.uuid1())
        folder_path = 'OutputImages'
        cv2.imwrite(os.path.join(folder_path, img_name), region)
        ocr_result = OCRNEW.ocr_space_file(filename=os.path.join(folder_path, img_name), language='eng')
        parsed = (ocr_result.split(',')[5])[14:22]
        #plt.imshow(cv2.cvtColor(region, cv2.COLOR_BGR2RGB))
        #matplotlib.use('TkAgg')
        #plt.show()
        return parsed



#Function to return raw detection coordinates from model
@tf.function
def detect_fn(image):
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections

category_index = label_map_util.create_category_index_from_labelmap(files['LABELMAP'])

cap = cv2.VideoCapture(0)
#width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

while cap.isOpened():
    ret, frame = cap.read()
    image_np = np.array(frame)
    image_np_expanded = np.expand_dims(frame, axis=0)

    input_tensor = tf.convert_to_tensor(image_np_expanded, dtype=tf.float32)
    detections = detect_fn(input_tensor)

    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy()
                  for key, value in detections.items()}
    detections['num_detections'] = num_detections

    # detection_classes should be ints.
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

    label_id_offset = 1
    image_np_with_detections = image_np.copy()

    viz_utils.visualize_boxes_and_labels_on_image_array(
        image_np_with_detections,
        detections['detection_boxes'],
        detections['detection_classes'] + label_id_offset,
        detections['detection_scores'],
        category_index,
        use_normalized_coordinates=True,
        max_boxes_to_draw=5,
        min_score_thresh=.8,
        agnostic_mode=False)

    output = detect_text(image_np_with_detections)
    cv2.imshow('object detection', cv2.resize(image_np_with_detections, (800, 600)))

    if output != None:
        print(output)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break