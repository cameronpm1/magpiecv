import os
import torch
import pathlib
import argparse
import numpy as np
from PIL import Image
from PIL import ImageGrab
import matplotlib.pyplot as plt
from torchvision import transforms
import matplotlib.patches as patches


parser = argparse.ArgumentParser()
parser.add_argument("--model_dir", help="location of folder with model weights")
parser.add_argument("--image_dir", help="location of folder with images to be tested")

def load_model(args):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=args.model_dir)#, force_reload=True) 
    return model

def test_model(args):
    model = load_model(args)
    with torch.no_grad():
        model.eval()
        dir = args.image_dir
        files = os.listdir(path=dir)
        result = None
        image = None
        for i,file in enumerate(files):
            image_dir = pathlib.Path(dir+file)
            image = Image.open(image_dir)#np.expand_dims(Image.open(image_dir), axis=0)
            result = model([image], size=640).xyxy[0].numpy()
            if len(result) == 0:
                continue
            else:
                save_visual_result(image,'',result,num=i)

def save_visual_result(image,file,results,num=0):
    fig, ax = plt.subplots()
    ax.imshow(image)
    rect = patches.Rectangle((results[0][0], results[0][1]), abs(results[0][0]-results[0][2]), abs(results[0][1]-results[0][3]), linewidth=1, edgecolor='r', facecolor='none')
    ax.add_patch(rect)  
    plt.savefig('results/result'+str(num)+'.png')

'''
def predict(image, model):
    x = transforms.ToTensor()(image)
    x = torch.unsqueeze(x, dim=0)
    pred = model(x)
    pred = pred.detach().numpy()
    return pred
'''

if __name__ == "__main__":
    args = parser.parse_args()
    test_model(args)