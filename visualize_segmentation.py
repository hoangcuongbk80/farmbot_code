import os
import cv2
import csv 
import xml.etree.ElementTree as ET 
from shutil import copyfile  

def parseXML(batch_dir, save_dir): 
    xmlfile = os.path.join(batch_dir, 'annotations.xml')
    # create element tree object 
    tree = ET.parse(xmlfile) 
  
    # get root element 
    root = tree.getroot() 
  
    # iterate news items 
    for inx, image in enumerate(root.findall('./image')): 
        src_img = os.path.join(batch_dir, 'images', image.get('name'))
        orig_image = cv2.imread(src_img)
        img = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)

        if len(image.findall('./polygon'))==0:
            continue
        for polygon in image.findall('./polygon'):
            point_str = polygon.get('points')
            list_point = list(point_str.split(";"))
            for point in list_point:
                pos = list(point.split(","))
                x = int(float(pos[0])) 
                x = x if x<img.shape[1] else x-1
                y = int(float(pos[1]))
                y = y if y<img.shape[0] else y-1
                img[y,x] = [0, 0, 255]
        dst_img = os.path.join(save_dir, 'visualization', image.get('name'))
        cv2.imwrite(dst_img, img)   

def main():   
    data_dir = '/home/hoang/datasets/ekobot/Semantic_Segmentation'

    save_dir = os.path.join(data_dir, 'data')

    for i in range (1, 7):
        batch = 'batch' + str(i)
        batch_dir = os.path.join(data_dir, batch)
        parseXML(batch_dir, save_dir)
        print('batch', i)

if __name__ == "__main__": 
  
    # calling main function 
    main() 