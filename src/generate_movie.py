import os
import cv2
import glob
import shutil
import pathlib
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from waymo_open_dataset import dataset_pb2 as open_dataset
from waymo_open_dataset.utils import  frame_utils

input_dir = 'data'
work_dir = 'images'
movie_dir = 'movies'
fps = 10.0

for input_filename in os.listdir(input_dir):
    print('\nProcess TFRecord: ' + input_filename)

    # Initialization
    if os.path.exists(work_dir):
        shutil.rmtree(work_dir)
    p_file = pathlib.Path(os.path.join(input_dir, input_filename))
    output_dir = os.path.join(movie_dir, p_file.stem)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read TFRecord
    dataset = tf.data.TFRecordDataset(os.path.join(input_dir, input_filename))

    # Get frame list
    frame_list = []
    ct = 0
    for data in dataset:
        frame_list.append(open_dataset.Frame())
        frame_list[ct].ParseFromString(bytearray(data.numpy()))
        ct = ct + 1
    
    print(input_filename + 'has ' + '{0:03d}'.format(ct) + ' frames')

    # Save jpg files
    print('Generate image files...')
    i = -1
    j = 0
    for frame in frame_list:
        i = i + 1
        j = 0
        for camera_image in frame.images:
            image_decoded = tf.image.decode_jpeg(camera_image.image)
            image_encoded = tf.io.encode_jpeg(image_decoded)
            out_fname = '{0:03d}'.format(i) + '.jpg'
            out_path = os.path.join(work_dir, '{0:02d}'.format(j), out_fname)
            tf.io.write_file(out_path, image_encoded)
            j = j + 1
    print('Image files have been successfully saved')

    # Save mp4 files
    for file_dir in os.listdir(work_dir):
        img_list = []
        for img_fname in glob.glob(os.path.join(work_dir, file_dir, '*.jpg')):
            img_list.append(cv2.imread(img_fname))

        frame_size = (img_list[0].shape[1], img_list[0].shape[0])
        out_file_path = os.path.join(output_dir, file_dir + '.mp4')
        out_video = cv2.VideoWriter(out_file_path, cv2.VideoWriter_fourcc(*'MP4V'), fps, frame_size)

        for img in img_list:
            out_video.write(img)
        
        out_video.release()
    
    print('Movie file: ', output_dir, ' has successfully saved')

# Clean up work directory
if os.path.exists(work_dir):
    shutil.rmtree(work_dir)
