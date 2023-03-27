#Import dependancies
import os
import uuid
import shutil

#Install dependencies

os.system("pip install --upgrade pip") #Install latest version of pip
os.system("pip install opencv-python") #Install opencv

#Define number of images to collect

image_labels = ['frontRegPlate', 'backRegPlate']

#Setup filepaths
RAW_IMAGE_DIRECTORY = os.path.join('Tensorflow', 'workspace', 'images', 'rawImages')
IMAGE_DIRECTORY = os.path.join('Tensorflow', 'workspace', 'images', 'collectedImages') #This is the directory to place images for training

#Create filepath if not already

if not os.path.exists(IMAGE_DIRECTORY):
    os.makedirs(IMAGE_DIRECTORY)

if not os.path.exists(RAW_IMAGE_DIRECTORY):
    os.makedirs(RAW_IMAGE_DIRECTORY)

#Create a subfolder for each label

for x in image_labels:
    path_to_create = os.path.join(RAW_IMAGE_DIRECTORY, x)

    if not os.path.exists(path_to_create):
        os.mkdir(path_to_create)


print("You should now place the images for sorting in the RAW IMAGES DIRECTORY directory")

### Uncomment the below code after placing in RAW IMAGES to start the renaming process


for x in image_labels:
    filepath = os.path.join(RAW_IMAGE_DIRECTORY, x)
    directory = os.listdir(filepath)
    destination = os.path.join(IMAGE_DIRECTORY, x)
    for file in directory:
        oldFile = os.path.join(filepath, file)
        name = x+"." + str(uuid.uuid1()) + ".jpg"
        newFile = os.path.join(filepath, name)

        os.renames(oldFile, newFile)
    shutil.move(filepath, destination)

print("The files have now been moved to the IMAGES DIRECTORY")
