#Import Dependencies
import os                                                               #Import system library for defining filepaths
import tensorflow as tf                                                 #Import TensorFlow
from object_detection.utils import label_map_util                       #Import all object detection dependencies
from object_detection.utils import visualization_utils as viz_utils     
from object_detection.builders import model_builder
from object_detection.utils import config_util
import cv2                                                              #Import OpenCV Python to be able to view the output
import numpy as np                                                      #Import NumPy math library to analyse the detection array

customModelName = 'myssdmobnet'                                         #Name of the custom object detection model folder 
labelMapName = 'label_map.pbtxt'                                        #Name of the labelmap file                                   

paths = {                                                                               #Define all neccesary filepaths using os library
    'annotationPath': os.path.join('Tensorflow', 'workspace','annotations'),
    'checkpointPath': os.path.join('Tensorflow', 'workspace','myModels',customModelName)
 }

files = {                                                                               #Define filepaths for important files 
    'pipelineConfigPath':os.path.join('Tensorflow', 'workspace','myModels', customModelName, 'pipeline.config'),
    'labelmap': os.path.join(paths['annotationPath'], labelMapName)
}

# Load pipeline config and build a detection model
configs = config_util.get_configs_from_pipeline_file(files['pipelineConfigPath'])          #Import model configuration according to pipeline.config file
detection_model = model_builder.build(model_config=configs['model'], is_training=False)    #Build model

# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)                                #Define type of checkpoint to import
ckpt.restore(os.path.join(paths['checkpointPath'], 'ckpt-15')).expect_partial()            #Import training data from checkpoint file

#Function to return raw detection coordinates from model
@tf.function
def detect_fn(image):                                                       #Pass image array as parameter
    image, shapes = detection_model.preprocess(image)                       #Process the image array
    prediction_dict = detection_model.predict(image, shapes)                #Make a prediction according to the detection model
    detections = detection_model.postprocess(prediction_dict, shapes)       #Store detection output array in variable
    return detections                                                       #Return detectoins array

category_index = label_map_util.create_category_index_from_labelmap(files['labelmap'])     #Create a category index file from labelmap 

cap = cv2.VideoCapture(0)                                                   #Define video source for live detections

while cap.isOpened():                                                       #Keep detecting until told to exit
    ret, frame = cap.read()                                                 #Capture a frame from the image source
    image_np = np.array(frame)                                              #Convert frame to an array using numPy
    image_np_expanded = np.expand_dims(frame, axis=0)                       #Expand the frame
    input_tensor = tf.convert_to_tensor(image_np_expanded, dtype=tf.float32)    #Convert the expanded frame into a tensor
    detections = detect_fn(input_tensor)                                    #Make a detection using the detection function defined above

    num_detections = int(detections.pop('num_detections'))                  #Get number of detections made
    detections = {key: value[0, :num_detections].numpy()                    #Loop through number of detections and save them in variable
                  for key, value in detections.items()}
    detections['num_detections'] = num_detections
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)  #Covert number of detection classes all to integers

    label_id_offset = 1
    image_np_with_detections = image_np.copy()                              #Copy the numPy array containing the image detections

    viz_utils.visualize_boxes_and_labels_on_image_array(                    #Function to visualise detections onscreen by drawing boxes
        image_np_with_detections,                                           #Detection array
        detections['detection_boxes'],                                      #Detection box coordinates
        detections['detection_classes'] + label_id_offset,                  #Detection classes (items)
        detections['detection_scores'],                                     #Detection scores
        category_index,                                                     #Category index generated
        use_normalized_coordinates=True,                                    
        max_boxes_to_draw=5,                                                #Maximum detections to display
        min_score_thresh=.8,                                                #Minimum score threshold for a detection to be displayed
        agnostic_mode=False)

    cv2.imshow('Object Detection', cv2.resize(image_np_with_detections, (800, 600))) #Display detection output in a OpenCV window with dimensions 800x600

    if cv2.waitKey(10) & 0xFF == ord('q'):          #If 'q' is pressed on keyboard then exit
        cap.release()                               #Stop video source input
        cv2.destroyAllWindows()                     #Destroy OpenCV window
        break                                       #Break


