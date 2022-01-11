import os

import cv2 as cv

from filtering_functions import hsv_filter


def change_from_array_to_list(array_to_change):
    new_list = []

    for i in range(len(array_to_change)):
        list = array_to_change[i].tolist()
        new_list.append(list)

    return new_list

def list_h_values(pixel_list):
    h_list = []
    for i in range(len(pixel_list)):
        h_list.append(pixel_list[i][0])
    return h_list

def list_s_values(pixel_list):
    s_list = []
    for i in range(len(pixel_list)):
        s_list.append(pixel_list[i][1])
    return s_list

def list_v_values(pixel_list):
    v_list = []
    for i in range(len(pixel_list)):
        v_list.append(pixel_list[i][2])
    return v_list


def automated_masking(green_hsv_pixel_values, object_hsv_pixel_values):
    green_hsv_pixel_values = change_from_array_to_list(green_hsv_pixel_values)
    object_hsv_pixel_values = change_from_array_to_list(object_hsv_pixel_values)
    list_h_green = list_h_values(green_hsv_pixel_values)
    list_h_object = list_h_values(object_hsv_pixel_values)
    list_s_green = list_s_values(green_hsv_pixel_values)
    list_s_object = list_s_values(object_hsv_pixel_values)
    list_v_green = list_v_values(green_hsv_pixel_values)
    list_v_object =list_v_values(object_hsv_pixel_values)
    h_green_max = max(list_h_green)
    h_green_min = min(list_h_green)
    s_green_max = max(list_s_green)
    s_green_min = min(list_s_green)
    v_green_max = max(list_v_green)
    v_green_min = min(list_v_green)
    h_object_max = max(list_h_object)
    h_object_min = min(list_h_object)
    s_object_max = max(list_s_object)
    s_object_min = min(list_s_object)
    v_object_max = max(list_v_object)
    v_object_min = min(list_v_object)

    print('list_green_hsv:',green_hsv_pixel_values)
    print('list_object_hsv:',object_hsv_pixel_values)
    print('h_green:', list_h_green)
    print('s_green:', list_s_green)
    print('v_green:', list_v_green)
    print('h_object:', list_h_object)
    print('s_object:', list_s_object)
    print('v_object:', list_v_object)

    directory_images = 'images'
    directory_masks = 'Masks'
    images = os.listdir(directory_images)
    filename_image = images[0]
    path_original_image = directory_images + '/' + filename_image
    img = cv.imread(path_original_image)
    height = img.shape[0]
    width = img.shape[1]

    if h_green_max > h_object_max:
        h_high = h_object_max
    else:
        h_high = h_green_max
    if h_green_min < h_object_min:
        h_low = h_object_min
    else:
        h_low = h_green_min

    if s_green_max > s_object_max:
        s_high = s_object_max
    else:
        s_high = s_green_max
    if s_green_min < s_object_min:
        s_low = s_object_min
    else:
        s_low = s_green_min

    if v_green_max > v_object_max:
        v_high = v_object_max
    else:
        v_high = v_green_max
    if v_green_min < v_object_min:
        v_low = v_object_min
    else:
        v_low = v_green_min



    for i in range(len(images)):
        filename_image = images[i]
        path_original_image = directory_images + '/' + filename_image
        img = cv.imread(path_original_image)
        hsv_filter(filename_image, img, height, width, h_low, s_low, v_low, h_high, s_high, v_high)



