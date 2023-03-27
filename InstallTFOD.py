import os
import wget

#Define Paths
CUSTOM_MODEL_NAME = 'centernet_mobilenetv2_fpn_od'
PRETRAINED_MODEL_NAME = 'centernet_mobilenetv2_fpn_od'
PRETRAINED_MODEL_URL = 'http://download.tensorflow.org/models/object_detection/tf2/20210210/centernet_mobilenetv2fpn_512x512_coco17_od.tar.gz'
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

#Create paths if not already
for path in paths.values():
    if not os.path.exists(path):
        os.mkdir(path)

#Download Tensorflow Model Zoo
if not os.path.exists(os.path.join(paths['APIMODEL_PATH'], 'research', 'object_detection')):
    os.system(f"git clone https://github.com/tensorflow/models {paths['APIMODEL_PATH']}")

#Download protobuf
url="https://github.com/protocolbuffers/protobuf/releases/download/v3.15.6/protoc-3.15.6-win64.zip"  #Download
wget.download(url)
os.system(f"move protoc-3.15.6-win64.zip {paths['PROTOC_PATH']}") #Move
os.system(f"cd {paths['PROTOC_PATH']} && tar -xf protoc-3.15.6-win64.zip") #Extract
os.environ['PATH'] += os.pathsep + os.path.abspath(os.path.join(paths['PROTOC_PATH'], 'bin')) #Add Protoc bin path to virtual environment

#Install Object Detection
os.system("cd Tensorflow/models/research && protoc object_detection/protos/*.proto --python_out=. && copy object_detection\\packages\\tf2\\setup.py setup.py")
os.system("cd Tensorflow/models/research/slim && pip install -e .")
os.system("pip install object_detection")
#Install Tensorflow
os.system("pip install tensorflow --upgrade")
os.system("pip install tensorflow-gpu")
os.system("pip install tensorflow-io")

#Install scipy
os.system("pip install scipy")

#Install matplotlib
os.system("pip install matplotlib")

#Install official
os.system("pip install tf-models-official")
