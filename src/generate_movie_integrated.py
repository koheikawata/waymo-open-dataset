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
comp_scale = 3

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

    # Get image size information for a new instance of VideoWriter
    i = 0
    for camera_image in frame_list[0].images:
        image_decoded = tf.image.decode_jpeg(camera_image.image)
        image_encoded = tf.io.encode_jpeg(image_decoded)
        out_fname = '{0:02d}'.format(i) + '.jpg'
        out_path = os.path.join(work_dir, out_fname)
        tf.io.write_file(out_path, image_encoded)
        i = i + 1

    img_list = []
    for img_fname in glob.glob(os.path.join(work_dir, '*.jpg')):
        img_tmp = cv2.imread(img_fname)
        img_resized = cv2.resize(img_tmp, 
                            (int(img_tmp.shape[1] / comp_scale), int(img_tmp.shape[0] / comp_scale)), 
                            interpolation = cv2.INTER_LINEAR)
        img_list.append(img_resized)
    
    y1 = img_list[0].shape[0]
    y2 = y1 + img_list[4].shape[0]
    x1 = img_list[0].shape[1]
    x2 = x1 + img_list[1].shape[1]
    x3 = x2 + img_list[2].shape[1]

    frame_size = (x3, y2)
    out_file_path = os.path.join(output_dir, p_file.stem + '.mp4')
    out_video = cv2.VideoWriter(out_file_path, cv2.VideoWriter_fourcc(*'MP4V'), fps, frame_size)

    # Image integration and video geneation
    frame_ct = 0
    for frame in frame_list:    
        i = 0
        for camera_image in frame.images:
            image_decoded = tf.image.decode_jpeg(camera_image.image)
            image_encoded = tf.io.encode_jpeg(image_decoded)
            out_fname = '{0:02d}'.format(i) + '.jpg'
            out_path = os.path.join(work_dir, out_fname)
            tf.io.write_file(out_path, image_encoded)
            i = i + 1

        # Save mp4 files
        img_list = []
        for img_fname in glob.glob(os.path.join(work_dir, '*.jpg')):
            img_tmp = cv2.imread(img_fname)
            img_resized = cv2.resize(img_tmp, 
                             (int(img_tmp.shape[1] / comp_scale), int(img_tmp.shape[0] / comp_scale)), 
                             interpolation = cv2.INTER_LINEAR)
            img_list.append(img_resized)
        
        img_base = np.tile(np.uint8([0,0,0]), (y2, x3, 1))
        img_base[0:y1, 0:x1] = img_list[1]
        img_base[0:y1, x1:x2] = img_list[0]
        img_base[0:y1, x2:x3] = img_list[3]
        img_base[y1:y2, 0:x1] = img_list[2]
        img_base[y1:y2, x2:x3] = img_list[4]
        out_video.write(img_base)

        frame_ct = frame_ct + 1
        print('A video frame ' + '{0:03d}'.format(frame_ct) + ' has been writtern')
        
    out_video.release()
    print('Movie file ', p_file.stem, '.mp4 has successfully saved')

# Clean up work directory
if os.path.exists(work_dir):
    shutil.rmtree(work_dir)
