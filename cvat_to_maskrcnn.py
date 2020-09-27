import os
import csv
import json
import cv2
import xml.etree.ElementTree as ET 
from shutil import copyfile  

test_data = {}
val_data = {}
train_data = {}

def add2data(data, regions, img_name, batch):
    obj_name = img_name
    data[obj_name] = {}
    data[obj_name]['fileref'] = ""
    data[obj_name]['size'] = 1024
    data[obj_name]['filename'] = os.path.join(batch, 'images',img_name)
    data[obj_name]['base64_img_data'] = ""
    data[obj_name]['file_attributes'] = {}
    data[obj_name]['regions'] = regions

def parseXML(data_dir, batch, save_dir): 
    batch_dir = os.path.join(data_dir, batch)
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
        regions = {}
        
        for ind, polygon in enumerate(image.findall('./polygon')):
            region = {}
            region['region_attributes'] = {}
            region['shape_attributes'] = {}

            edges_x = []
            edges_y = []

            point_str = polygon.get('points')
            list_point = list(point_str.split(";"))
            for point in list_point:
                pos = list(point.split(","))
                x = int(float(pos[0])) 
                x = x if x<img.shape[1] else x-1
                y = int(float(pos[1]))
                y = y if y<img.shape[0] else y-1
                edges_x.append(x)
                edges_y.append(y)

            edges_x.append(edges_x[0])
            edges_y.append(edges_y[0])

            label = polygon.get('label')
            if label=='Onion':
                class_id = 1
            if label=='Weed':
                class_id = 2
            if label=='Weed_Root':
                class_id = 3

            region['shape_attributes']["name"] = "polygon"
            region['shape_attributes']["all_points_x"] = edges_x
            region['shape_attributes']["all_points_y"] = edges_y
            region['shape_attributes']["class_id"] = class_id

            regions[str(ind)] = region

        img_name = image.get('name')

        if inx%15 == 0:
            add2data(test_data, regions, img_name, batch)
            dst_img = os.path.join(save_dir, 'test', image.get('name'))
            copyfile(src_img, dst_img)          
        elif inx%8 == 0:
            add2data(val_data, regions, img_name, batch)
        else:
            add2data(train_data, regions, img_name, batch)

def main():   
    data_dir = '/home/hoang/datasets/ekobot/Semantic_Segmentation'

    save_dir = os.path.join(data_dir, 'data')
    json_test_dir = os.path.join(data_dir, 'data', 'via_region_data_test.json')
    json_val_dir = os.path.join(data_dir, 'data', 'via_region_data_val.json')
    json_train_dir = os.path.join(data_dir, 'data', 'via_region_data_train.json')

    for i in range (1, 7):
        print('batch', i)
        batch = 'batch' + str(i)
        parseXML(data_dir, batch, save_dir, )
    
    with open(json_test_dir, 'w') as outfile:  
        json.dump(test_data, outfile, sort_keys=True)

    with open(json_val_dir, 'w') as outfile:  
        json.dump(val_data, outfile, sort_keys=True)

    with open(json_train_dir, 'w') as outfile:  
        json.dump(train_data, outfile, sort_keys=True)

if __name__ == "__main__": 
  
    # calling main function 
    main() 