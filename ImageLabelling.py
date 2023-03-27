#IMport dependancies
import os

#Define the filepath to store the program

LABELIMAGE_PATH = os.path.join('Tensorflow', 'labelImg')

#Install the program in the directory if not already

if not os.path.exists(LABELIMAGE_PATH):
    os.mkdir(LABELIMAGE_PATH)
    os.system("git clone https://github.com/tzutalin/labelImg {}".format(LABELIMAGE_PATH))

#Initialise Program

os.system(f"cd {LABELIMAGE_PATH} && pyrcc5 -o libs/resources.py resources.qrc")

#Launch Program

os.system(f"cd {LABELIMAGE_PATH} && python labelImg.py")