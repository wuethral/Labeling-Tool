import os
import cv2
import numpy as np
import tkinter as tk
from displaying import displaying_current_image
from PIL import Image, ImageTk
from sklearn.cluster import DBSCAN


def delete_image(images, lists, all_canvas, label_dict_select_area, label_buttons, img_nr):
    '''This function deletes the image, mask and mask_image_merge at the current img_nr in the attributes image_list,
    mask_list and mask_image_merge_list of the object lists. They area also deleted in the folders images,
    bounding_boxes and image_mask_merge'''

    # Removing the images, masks, mask_image_merge from the attributes image_list, mask_list, mask_image_merge_list in
    # the object lists at the current img_nr
    lists.image_list.remove(lists.image_list[img_nr.img_number])
    lists.mask_list.remove(lists.mask_list[img_nr.img_number])
    lists.mask_image_merge_list.remove(lists.mask_image_merge_list[img_nr.img_number])

    # Name of the image at the current image number
    image_name = images[img_nr.img_number]
    # Paths to the images, masks and mask_image_merges
    image_path = 'images/' + image_name
    path_mask = 'bounding_boxes/' + image_name
    path_mask_img_merge = 'image_mask_merge/' + image_name
    # Removing the images, masks and mask_image_merges from the according folders
    os.remove(path_mask)
    os.remove(image_path)
    os.remove(path_mask_img_merge)

    # Delete the image name in the image name list at the current image number
    del lists.images[img_nr.img_number]
    # If the deleted image is not the first image, subtract 1 from the image number
    if img_nr != 0:
        img_nr.minus()

    redo_mask_list = True
    displaying_current_image(lists, all_canvas, label_dict_select_area, img_nr, redo_mask_list, label_buttons)

def restore(images, lists, img_nr, w, h, all_canvas, label_dict_select_area, label_buttons):
    '''This function restores the masks, and mask_image_merge to it's starting state'''

    # Name of the image at the current image number
    image_name = images[img_nr.img_number]
    # Paths to the mask mask_image_merge in the folder bounding_boxes, bounding_boxes_copy, images_mask_merge and
    # images_mask_merge_copy
    old_mask_path = 'bounding_boxes/' + image_name
    new_mask_path = 'bounding_boxes_copy/' + image_name
    old_mask_image_merge_path = 'image_mask_merge/' + image_name
    new_mask_image_merge_path = 'image_mask_merge_copy/' + image_name
    # Loading masks and mask_image_merge from bounding_boxes_copy and image_mask_merge_copy folders
    # Removing masks and mask_image_merge form bounding_boxes and image_mask_merge folders
    new_mask = cv2.imread(new_mask_path)
    os.remove(old_mask_path)
    new_image_merge = cv2.imread(new_mask_image_merge_path)
    os.remove(old_mask_image_merge_path)
    # Writing the newly loaded images and masks to the folder bounding_boxes and mask_image_merge_folder
    cv2.imwrite(old_mask_path, new_mask)
    cv2.imwrite(old_mask_image_merge_path, new_image_merge)
    # Opening the mask and mask_image_merge and resizing them
    mask = Image.open(old_mask_path)
    mask = ImageTk.PhotoImage(mask.resize((int(0.8*w), int(0.8*h))))
    mask_image_merge = Image.open(old_mask_image_merge_path)
    mask_image_merge = ImageTk.PhotoImage(mask_image_merge.resize((int(0.8*w), int(0.8*h))))
    # Adding the mask and mask_image_merge to to the attributes mask_list and mask_image_merge_list at the current image
    # number.
    lists.mask_list[img_nr.img_number] = mask
    lists.mask_image_merge_list[img_nr.img_number] = mask_image_merge

    # redo_mask_list needs to be True, because we made changes in the image folder
    redo_mask_list = True
    displaying_current_image(lists, all_canvas, label_dict_select_area, img_nr, redo_mask_list, label_buttons)

def erosion(x, w, h, images, lists, all_canvas, label_dict_select_area, img_nr, label_buttons):

    image_name = images[img_nr.img_number]
    mask_path = 'bounding_boxes/' + image_name
    mask = cv2.imread(mask_path)
    kernel = np.ones((x, x), np.uint8)
    img_erosion = cv2.erode(mask, kernel, iterations=1)
    os.remove(mask_path)
    cv2.imwrite(mask_path, img_erosion)

    mask = Image.open(mask_path)
    mask = ImageTk.PhotoImage(mask.resize((int(0.8*w), int(0.8*h))))
    lists.mask_list[img_nr.img_number] = mask

    black = cv2.imread('black.png')
    black = cv2.resize(black, (760, 428))
    img_erosion = cv2.resize(img_erosion, (760, 428))
    image_path = 'images/' + image_name
    image = cv2.imread(image_path)
    image = cv2.resize(image, (760, 428))
    mask_image_merge = np.where(img_erosion==0, black, image)
    mask_image_merge_path = 'image_mask_merge/' + image_name
    os.remove(mask_image_merge_path)
    cv2.imwrite(mask_image_merge_path, mask_image_merge)
    pillow_mask_image_merge = Image.open(mask_image_merge_path)
    pillow_mask_image_merge = ImageTk.PhotoImage(pillow_mask_image_merge.resize((int(0.8 * w), int(0.8 * h))))
    lists.mask_image_merge_list[img_nr.img_number] = pillow_mask_image_merge

    redo_mask_list = True
    displaying_current_image(lists, all_canvas, label_dict_select_area, img_nr, redo_mask_list, label_buttons)

def dilation(x, w, h, images, lists, all_canvas, label_dict_select_area, img_nr, label_buttons):
    image_name = images[img_nr.img_number]
    mask_path = 'bounding_boxes/' + image_name
    mask = cv2.imread(mask_path)
    kernel = np.ones((x, x), np.uint8)
    img_dilation = cv2.dilate(mask, kernel, iterations=1)
    os.remove(mask_path)
    cv2.imwrite(mask_path, img_dilation)
    mask = Image.open(mask_path)
    mask = ImageTk.PhotoImage(mask.resize((int(0.8*w), int(0.8*h))))
    lists.mask_list[img_nr.img_number] = mask


    black = cv2.imread('black.png')
    black = cv2.resize(black, (760, 428))
    img_dilation = cv2.resize(img_dilation, (760, 428))
    image_path = 'images/' + image_name
    image = cv2.imread(image_path)
    image = cv2.resize(image, (760, 428))
    mask_image_merge = np.where(img_dilation==0, black, image)
    mask_image_merge_path = 'image_mask_merge/' + image_name
    os.remove(mask_image_merge_path)
    cv2.imwrite(mask_image_merge_path, mask_image_merge)
    pillow_mask_image_merge = Image.open(mask_image_merge_path)
    pillow_mask_image_merge = ImageTk.PhotoImage(pillow_mask_image_merge.resize((int(0.8 * w), int(0.8 * h))))
    lists.mask_image_merge_list[img_nr.img_number] = pillow_mask_image_merge
    redo_mask_list = True
    displaying_current_image(lists, all_canvas, label_dict_select_area, img_nr, redo_mask_list, label_buttons)

def get_pixel(root, all_canvas, lists, label_dict_select_area, img_nr, label_buttons, images):

    global get_pixel_flag
    get_pixel_flag = True

    def get_pixel_value(event):
        coordinates = event.x, event.y
        pixel_value = current_mask[coordinates[1]][coordinates[0]][0]
        display_text = 'Mask Pixel Value: ' + str(pixel_value)
        all_canvas.canvas.create_text(5, 0, anchor = tk.NW, fill="darkblue",
                            text=display_text, font = 'Times 16', tag = 'text')

    def stop_get_pixel_value(event):
        redo_mask_list = False
        all_canvas.canvas.delete('text')

    current_mask_path = 'bounding_boxes/' + images[img_nr.img_number]
    current_mask = cv2.imread(current_mask_path)
    root.bind("<ButtonPress-1>", get_pixel_value)
    root.bind("<ButtonRelease-1>", stop_get_pixel_value)

def make_blank(images, img_nr, lists, all_canvas, label_dict_select_area, label_buttons):
    mask_path = 'bounding_boxes/' + images[img_nr.img_number]
    mask_merge_path = 'image_mask_merge/' + images[img_nr.img_number]
    os.remove(mask_path)
    os.remove(mask_merge_path)
    black = cv2.imread('black.png')
    black = cv2.resize(black, (760,428))
    cv2.imwrite(mask_path, black)
    cv2.imwrite(mask_merge_path, black)
    redo_mask_list = True
    displaying_current_image(lists, all_canvas, label_dict_select_area, img_nr, redo_mask_list, label_buttons)

def dbscan(images, img_nr, lists, w, h, all_canvas, label_dict_select_area, label_buttons, pixel_value):
    mask_path = 'bounding_boxes/' + images[img_nr.img_number]
    mask = cv2.imread(mask_path)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    coordinates_of_white_pixels = []
    rows, cols = mask.shape[:2]

    for i in range(rows):
        for j in range(cols):
            if mask[i, j] == pixel_value:
                coordinates_of_white_pixels.append([i, j])
    X = np.asarray(coordinates_of_white_pixels)
    model = DBSCAN(eps=2, min_samples=9)
    yhat = model.fit_predict(X)
    clusters = np.unique(yhat)
    size_of_biggest_cluster = 0
    index_od_biggest_cluster = 0
    for cluster in clusters:
        row_ix = np.where(yhat == cluster)
        if row_ix[0].size > size_of_biggest_cluster:
            size_of_biggest_cluster = row_ix[0].size
            index_od_biggest_cluster = cluster

    for cluster in clusters:
        if cluster == index_od_biggest_cluster:
            continue
        else:
            row_ix = np.where(yhat == cluster)
            x_coord_to_delete_mask = X[row_ix, 0]
            y_coord_to_delete_mask = X[row_ix, 1]
            for i in range(len(x_coord_to_delete_mask[0])):
                mask[x_coord_to_delete_mask[0][i], y_coord_to_delete_mask[0][i]] = 0
    os.remove(mask_path)
    cv2.imwrite(mask_path, mask)
    mask_pillow = Image.open(mask_path)
    mask_pillow = ImageTk.PhotoImage(mask_pillow.resize((int(0.8 * w), int(0.8 * h))))
    lists.mask_list[img_nr.img_number] = mask_pillow
    black = cv2.imread('black.png')
    black = cv2.resize(black, (760, 428))
    image_path = 'images/' + images[img_nr.img_number]
    image = cv2.imread(image_path)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    image_merge = np.where(mask == 0, black, image)
    mask_image_merge_path = 'image_mask_merge/' + images[img_nr.img_number]
    os.remove(mask_image_merge_path)
    cv2.imwrite(mask_image_merge_path, image_merge)
    mask_merge_pillow = Image.open(mask_image_merge_path)
    mask_merge_pillow = ImageTk.PhotoImage(mask_merge_pillow.resize((int(0.8 * w), int(0.8 * h))))
    lists.mask_image_merge_list[img_nr.img_number] = mask_merge_pillow
    redo_mask_list = True
    displaying_current_image(lists, all_canvas, label_dict_select_area, img_nr, redo_mask_list, label_buttons)
