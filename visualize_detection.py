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

        if len(image.findall('./box'))==0:
            continue
        for box in image.findall('./box'):
            XMin = float(box.get('xtl'))
            XMin = int(round(XMin))
            XMax = float(box.get('xbr'))
            XMax = int(round(XMax))
            YMin = float(box.get('ytl'))
            YMin = int(round(YMin))
            YMax = float(box.get('ybr'))
            YMax = int(round(YMax))
            label = box.get('label')
            cv2.rectangle(img, (XMin, YMin), (XMax, YMax), (255, 255, 0), 1)
            cv2.putText(img, label, (XMin + 20, YMin + 40),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,255),2)
        dst_img = os.path.join(save_dir, 'visualization', image.get('name'))
        cv2.imwrite(dst_img, img)        

def main():   
    data_dir = '/home/hoang/datasets/ekobot/Object_Detection'

    save_dir = os.path.join(data_dir, 'data')

    for i in range (1, 8):
        batch = 'batch' + str(i)
        batch_dir = os.path.join(data_dir, batch)
        parseXML(batch_dir, save_dir)

if __name__ == "__main__": 
  
    # calling main function 
    main() 