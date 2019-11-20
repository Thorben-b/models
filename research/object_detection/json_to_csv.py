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
        for item in data["shapes"]:
            box = item['points']
            if item['label']!='None':
                name=item['label']
                labels.append(name)
                xmin=box[0][0]
                ymin=box[0][1]
                xmax=box[1][0]
                ymax=box[1][1]
                value = (fjpg[n],
                         width,
                         height,
                         name,
                         round(xmin),
                         round(ymin),
                         round(xmax),
                         round(ymax)
                         )
                csv_list.append(value)
        n=n+1
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    csv_df = pd.DataFrame(csv_list, columns=column_name)
    labels_train=list(set(labels))
    return csv_df

def main():
    for directory in ['train', 'test']:
        image_path = os.path.join(os.getcwd(), ('images/' + directory))
        csv_df = json_to_csv(image_path)
        csv_df.to_csv('images/'+directory+'_labels.csv', index=None)
        print('Successfully converted json to csv.')

main()