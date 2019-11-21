import os
import glob
import pandas as pd
import json
import pickle

def json_to_csv(file_path):
    json_files = [pos_json for pos_json in os.listdir(file_path) if pos_json.endswith('.json')]
    jpg_files = [pos_jpg for pos_jpg in os.listdir(file_path) if pos_jpg.endswith('.jpg')]
    fjpg=(list(reversed(jpg_files)))
    n=0
    csv_list = []
    labels=[]
    for j in json_files:
        data_file=open(file_path+'/{}'.format(j))   
        data = json.load(data_file)
        width,height=data['imageWidth'],data['imageHeight']
        name = data['imagePath']
        for item in data["shapes"]:
            box = item['points']
            if item['label']!='None':
                class_name=item['label']
                xmin=box[0][0]
                ymin=box[0][1]
                xmax=box[2][0]
                ymax=box[2][1]
                value = (name,
                         width,
                         height,
                         class_name,
                         round(xmin, 3),
                         round(ymin, 3),
                         round(xmax, 3),
                         round(ymax, 3)
                         )
                csv_list.append(value)
        n=n+1
    
    #print(csv_list)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    csv_df = pd.DataFrame(csv_list, columns=column_name)
    return csv_df

def main():
    for directory in ['train', 'test']:
        image_path = os.path.join(os.getcwd(), ('images/' + directory))
        csv_df = json_to_csv(image_path)
        csv_df.to_csv('images/'+directory+'_labels.csv', index=None)
        print('Successfully converted json to csv.')

main()
