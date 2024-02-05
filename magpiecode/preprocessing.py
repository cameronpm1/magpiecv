import os
import re
import argparse
import numpy as np
from PIL import Image

# train script:  python train.py --img 1280 --rect --epochs 15 --data /home/cameron/magpiecv/datasets/data.yaml --weights yolov5s.pt

parser = argparse.ArgumentParser()
parser.add_argument("--dir", help="location of folder with data labels")

def check_data_labels(args):
    '''
    parse through all label files and check for bad labels
    '''
    dir = args.dir + 'labels/'
    pic_dir = args.dir + 'images/'
    files = os.listdir(path=dir)
    for file in files:
        f = open(dir+file, 'r')
        file_contents = f.read()
        nlines = np.array([m.start() for m in re.finditer('\n', file_contents)]) + 1
        if '0.3777' in file_contents:
            print(file)
        #if len(nlines) > 0:
        #print(file_contents)
        #file_contents = '1'+file_contents[1:] #rename label as 1
        '''
        if len(file_contents) < 4:
            print('label file',file,'is empty, now purging')
            picture_file = file[:-4] + '.jpg'
            os.remove(dir+file)#print(file)
            os.remove(pic_dir+picture_file)#print(picture_file)
        else:
            with open((dir+file), 'w') as file: 
                file.write(file_contents)
        '''

def convert_images(args, index_start='00000', name='', convert_type='.jpg'):
    dir = args.dir
    files = os.listdir(path=dir)
    index = int(index_start)
    format_index = '{:0' + str(len(index_start)) + 'd}'
    index_len = len(index_start)
    #"{:05d}".format(10)

    for file in files:
        image_dir = dir+file
        im = Image.open(image_dir)
        converted_im = im.convert("RGB")
        name_num = format_index.format(index)
        convert_name = name_num+name+convert_type
        converted_im.save(dir+convert_name)
        index += 1
        print('Converting image', file, 'to', convert_name)
        os.remove(image_dir)
        print('Deleting image', file)

def reformat_image_size(args, image_size=[640,640]):
    dir = args.dir
    files = os.listdir(path=dir)

    for file in files:
        image_dir = dir+file
        image = Image.open(image_dir)
        resized_image = image.resize((image_size[0], image_size[1]))
        os.remove(image_dir)
        resized_image.save(image_dir)


def change_data_labels(args):
    '''
    parse through all label files and rewrite their label (first string in the txt document)
    for drone dataset, however, should be compatable with any roboflow yolov5 datasets
    '''
    dir = args.dir + 'labels/'
    pic_dir = args.dir + 'images/'
    files = os.listdir(path=dir)
    for file in files:
        f = open(dir+file, 'r')
        file_contents = f.read()
        if file_contents[0] != str(1):
            file_contents = '1'+file_contents[1:] #rename label as 1
        nlines = np.array([m.start() for m in re.finditer('\n', file_contents)]) + 1
        if len(nlines) > 0:
            temp_file_contents = list(file_contents)
            for nline in nlines:
                temp_file_contents[nline] = 1
            file_contents = ''.join(map(str,temp_file_contents))
        if len(file_contents) < 4:
            '''
            if label is empty, 
            '''
            print('label file',file,'is empty, now purging')
            picture_file = file[:-4] + '.jpg'
            os.remove(dir+file)#print(file)
            os.remove(pic_dir+picture_file)#print(picture_file)
        else:
            '''
            if label is not empty, relabel the drone as 1
            '''
            with open((dir+file), 'w') as file: 
                file.write(file_contents)


if __name__ == "__main__":
    args = parser.parse_args()
    reformat_image_size(args)