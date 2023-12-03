
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image
import numpy as np
import torch
import cv2


@st.cache_resource
def load_model():
    model = torch.hub.load(
        'ultralytics/yolov5', 
        'custom', 
        path='/raid/home/rajivratn/avinash/Raj/best.pt'
    )
    return model
model = load_model()


def make_prediction(img_path):
    img = Image.open(img_path).convert('RGB')
    open_cv_image = np.array(img)
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    results = model([open_cv_image])
    return open_cv_image, results


def show_bounding_boxes(img, results, cls):
    df = results.pandas().xyxy[0]
    df = df[df['name'] == cls]
    list_of_rows = [list(row) for row in df.values]

    for each_row in list_of_rows:
        cv2.rectangle(img, 
            (int(each_row[0]), int(each_row[1])), 
            (int(each_row[2]), int(each_row[3])), 
            (255, 0, 0), 2
        )
    return img


st.title("Object Detection :tea: :coffee:")
upload = st.file_uploader(label= "Upload an image : ", type = ["png","jpg","jpeg"])

if upload:
    print(upload)
    img, results = make_prediction(upload)
    bounded_img = show_bounding_boxes(img, results, 'Table')
    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot(111)
    plt.imshow(bounded_img)
    plt.xticks([],[])
    plt.yticks([],[])
    ax.spines[["top","bottom","right","left"]].set_visible(False)

    st.pyplot(fig,use_container_width=True)

