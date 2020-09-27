import os
import csv 
import xml.etree.ElementTree as ET 
from shutil import copyfile  
 
def parseXML(batch_dir, save_dir): 
    xmlfile = os.path.join(batch_dir, 'annotations.xml')
    # create element tree object 
    tree = ET.parse(xmlfile) 
  
    # get root element 
    root = tree.getroot() 
  
    # create empty list for news items 
    testitems = []
    valitems = []
    trainitems = []

    # iterate news items 
    for inx, image in enumerate(root.findall('./image')): 
        src_img = os.path.join(batch_dir, 'images', image.get('name'))

        if len(image.findall('./box'))==0:
            continue
        for box in image.findall('./box'):
            news = {}
            news['ImageID'] = image.get('name')[:-4]
            news['XMin'] = float(box.get('xtl')) / float(image.get('width'))
            news['XMax'] = float(box.get('xbr')) / float(image.get('width'))
            news['YMin'] = float(box.get('ytl')) / float(image.get('height'))
            news['YMax'] = float(box.get('ybr')) / float(image.get('height'))
            news['ClassName'] = box.get('label')
            if(news['ClassName'] != 'Weed_Root'):
                continue

            if inx%15 == 0:
                testitems.append(news)
            elif inx%8 == 0:
                valitems.append(news)
            else:
                trainitems.append(news)

        if inx%15 == 0:
            dst_img = os.path.join(save_dir, 'test', image.get('name'))
        elif inx%8 == 0:
            dst_img = os.path.join(save_dir, 'validation', image.get('name'))
        else:
            dst_img = os.path.join(save_dir, 'train', image.get('name'))


        copyfile(src_img, dst_img)          

    return testitems, valitems, trainitems
        
def main():   
    data_dir = '/home/hoang/datasets/ekobot/Object_Detection'

    save_dir = os.path.join(data_dir, 'data')
    csv_test_dir = os.path.join(data_dir, 'data', 'test-annotations-bbox.csv')
    csv_val_dir = os.path.join(data_dir, 'data', 'validation-annotations-bbox.csv')
    csv_train_dir = os.path.join(data_dir, 'data', 'train-annotations-bbox.csv')
    
    # specifying the fields for csv file 
    fields = ['ImageID', 'XMin', 'XMax', 'YMin', 'YMax', 'ClassName']
  
    # writing to csv file 
    csv_test_file = open(csv_test_dir, 'w') 
    csv_val_file = open(csv_val_dir, 'w') 
    csv_train_file = open(csv_train_dir, 'w') 

    # creating a csv dict writer object 
    test_writer = csv.DictWriter(csv_test_file, fieldnames = fields) 
    val_writer = csv.DictWriter(csv_val_file, fieldnames = fields) 
    train_writer = csv.DictWriter(csv_train_file, fieldnames = fields) 

    # writing headers (field names) 
    test_writer.writeheader() 
    val_writer.writeheader() 
    train_writer.writeheader() 

    for i in range (1, 8):
        batch = 'batch' + str(i)
        batch_dir = os.path.join(data_dir, batch)
        test_items, val_items, train_items = parseXML(batch_dir, save_dir)
    
        # writing data rows 
        test_writer.writerows(test_items)
        val_writer.writerows(val_items) 
        train_writer.writerows(train_items) 

    csv_test_file.close()
    csv_val_file.close()
    csv_train_file.close()
      
if __name__ == "__main__": 
  
    # calling main function 
    main() 