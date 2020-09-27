#import necessary modules
import csv
with open('/home/hoang/datasets/ekobot/Object_Detection/data/train-annotations-bbox.csv','rt')as f:
  data = csv.reader(f)
  for inx, row in enumerate(data):
        print(inx)
        print(row)