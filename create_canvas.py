#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
import numpy as np
import shutil
import random
import cv2
import os
import PIL
import random
from PIL import Image
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')

df2 = pd.read_csv('raylaynet_dataframe.csv')

def smart_plot(data, counter, index = []):
    df = data[:].copy(deep=True)
    df = df.drop(df.index[index])
    df.reset_index(inplace=True)

    lower_gap = []
    max_count = {'text':5, 'title':3, 'figure':1, 'table':1, 'list':1}

    height, completed = 700, 0
    sampleList = ['text', 'title', 'figure', 'table', 'list']

    position = []
    while True:
        temp_max = 0
        if completed >= 26: break
        if height < 12: break
        width = 700

        if height < 50:
            df = df[df['bbox_height'] <= height[0]].reset_index(drop=True)

        temp_position = []
        gap_row_gen = random.randint(8, 12)

        while True:
            random_choice = random.choice(sampleList)
            sampleList = list(df['label'].unique())
            temp_df = df[df['label'] == random_choice]

            if max_count[random_choice] > 0 and counter[random_choice] > 0 and temp_df.shape[0] > 0:
                sample = temp_df.sample()
                gap_gen = random.randint(8, 12)

                label_width, label_height = sample['bbox_width'].values, sample['bbox_height'].values
                label = sample['label'].values

                if width > gap_gen + label_width and index.count(sample.index[0]) <= 0:
                    if temp_max < label_height: 
                        if label_height + gap_row_gen < height: temp_max = label_height
                        else: continue

                    else: continue

                    width -= gap_gen
                    width -= label_width

                    temp_position.append(sample)
                    temp_position.append(gap_gen)
                    index.append(sample.index[0])

                    max_count[random_choice] -= 1
                    counter[random_choice] -= 1
                    completed += 1

                else: break
            else: break

        temp_position.append(temp_max)
        position.append(temp_position)
        lower_gap.append(gap_row_gen)

        height -= temp_max
        height -= gap_row_gen

    return position, counter, index, lower_gap

def crop(data):
    img = Image.open(data['file_name'].values[0])
    image = img.crop((data['bbox_x'].values[0], data['bbox_y'].values[0], data['xmax'].values[0], data['ymax'].values[0]))
    return image


def plot(df, counter, index = []):
    label = pd.DataFrame(columns=['label', 'xmin', 'ymin', 'xmax', 'ymax'])
    store, counter, index, lower_gap = smart_plot(df, counter, index)

    if store != -1:
        im = PIL.Image.new(mode = "RGB", size = (700, 700), color = (255, 255, 255))
        top = [12.0, 12.0]

        for row in range(len(store)):
            for col in range(int((len(store[row])-1)/2)):
                data = store[row][col*2]

                if np.isnan(data['bbox_x'].values[0]) == False:
                    im.paste(crop(data), (int(top[0]), int(top[1])))

                    xmin = top[0]
                    xmax = top[0] + float(data['bbox_width'].values[0])

                    ymin = top[1]
                    ymax = top[1] + float(data['bbox_height'].values[0])

                    label.loc[len(label)] = {'xmin': xmin, 'ymin': ymin, 'xmax':xmax, 'ymax':ymax, 'label': data['label'].values[0]}
                else:
                    im.paste(Image.open(data['file_name'].values[0]), (int(top[0]), int(top[1])))
                    
                top[0] += float(data['bbox_width'].values[0]) + float(store[row][col*2+1])
            try:
                top[0] = 12.0
                top[1] = top[1] + float(store[row][col*2+2]) + lower_gap[row]

            except Exception as e:
                pass
                # print(e)
                # print(len(store[row]))
                # print(store[row])

        return im, counter, label, index
    
    else:
        plot(df, counter, index)


def bb_plot(image, label):
    image = cv2.imread(image)

    for i in range(label.shape[0]):
        l = label.loc[[i]]

        start_point = (int(l['xmin'].values[0]), int(l['ymax'].values[0]))
        end_point = (int(l['xmax'].values[0]), int(l['ymin'].values[0]))

        color = (0, 0, 0)
        thickness = 2
        image = cv2.rectangle(image, start_point, end_point, color, thickness)

    return image


def create_raylaynet_dataset(df):
    counter = {'text':95227, 'title':45306, 'figure':23493, 'table':22146, 'list':23090}
    image_count = 0

    while True:
        # if image_count == 3600: break
        if all(value == 0 for value in counter.values()): break

        canvas_image, counter, canvas_df, _ = plot(df, counter, [])

        area = 0.0
        for i in range(canvas_df.shape[0]):
            area += (canvas_df['xmax'][i] - canvas_df['xmin'][i]) * (canvas_df['ymax'][i] - canvas_df['ymin'][i])

        if (700*700*0.30) > area: continue

        print('{} Image Started!!'.format(image_count+1))
        image_count += 1
        canvas_image.save('images/canvas_{}.jpg'.format(str(image_count)))
        
        bounding_box_canvas = bb_plot('images/canvas_{}.jpg'.format(str(image_count)), canvas_df)
        cv2.imwrite('images_with_bb/canvas_{}.jpg'.format(str(image_count)), bounding_box_canvas)

        canvas_df.to_csv('labels/canvas_{}.txt'.format(str(image_count)), index=False, sep='\t')

    print("{} Number of Canvas Created".format(str(image_count)))


if __name__ == '__main__':
    create_raylaynet_dataset(df2)

