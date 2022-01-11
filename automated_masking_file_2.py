import os

import cv2 as cv

from filtering_functions import hsv_filter, hsv_filter_direct


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


def automated_masking_2(green_hsv_pixel_values):
    green_hsv_pixel_values = change_from_array_to_list(green_hsv_pixel_values)
    list_h_green = list_h_values(green_hsv_pixel_values)
    list_s_green = list_s_values(green_hsv_pixel_values)
    list_v_green = list_v_values(green_hsv_pixel_values)
    print(green_hsv_pixel_values)
    h_green_max = max(list_h_green)
    h_green_min = min(list_h_green)
    s_green_max = max(list_s_green)
    s_green_min = min(list_s_green)
    v_green_max = max(list_v_green)
    v_green_min = min(list_v_green)


    directory_images = 'D:/Hololens_recordings/Project_Balgrist/angle_for_new_automated_masking/renamed_images'
    directory_masks = 'Masks'
    images = os.listdir(directory_images)
    filename_image = images[0]
    path_original_image = directory_images + '/' + filename_image
    img = cv.imread(path_original_image)
    height = img.shape[0]
    width = img.shape[1]



    for i in range(len(images)):
        filename_image = images[i]
        path_original_image = directory_images + '/' + filename_image
        img = cv.imread(path_original_image)
        hsv_image = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        hsv_filter_direct(filename_image, hsv_image, height, width, h_green_min, h_green_max, s_green_min, s_green_max, v_green_min, v_green_max)



