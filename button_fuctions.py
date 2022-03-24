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
    masks and image_mask_merge'''

    # Removing the images, masks, mask_image_merge from the attributes image_list, mask_list, mask_image_merge_list in
    # the object lists at the current img_nr
    lists.image_list.remove(lists.image_list[img_nr.img_number])
    lists.mask_list.remove(lists.mask_list[img_nr.img_number])
    lists.mask_image_merge_list.remove(lists.mask_image_merge_list[img_nr.img_number])

    # Name of the image at the current image number
    image_name = images[img_nr.img_number]
    # Paths to the images, masks and mask_image_merges
    image_path = 'images/' + image_name
    path_mask = 'masks/' + image_name
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
    # Paths to the mask mask_image_merge in the folder masks, masks_copy, images_mask_merge and
    # images_mask_merge_copy
    old_mask_path = 'masks/' + image_name
    new_mask_path = 'masks_copy/' + image_name
    old_mask_image_merge_path = 'image_mask_merge/' + image_name
    new_mask_image_merge_path = 'image_mask_merge_copy/' + image_name
    # Loading masks and mask_image_merge from masks_copy and image_mask_merge_copy folders
    # Removing masks and mask_image_merge form masks and image_mask_merge folders
    new_mask = cv2.imread(new_mask_path)
    os.remove(old_mask_path)
    new_image_merge = cv2.imread(new_mask_image_merge_path)
    os.remove(old_mask_image_merge_path)
    # Writing the newly loaded images and masks to the folder masks and mask_image_merge_folder
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
    '''Function responsible for the erosion of the masks with different kernel sizes'''

    # Opening the mask
    image_name = images[img_nr.img_number]
    mask_path = 'masks/' + image_name
    mask = cv2.imread(mask_path)

    # Creating eroded image of mask with kernel size (x,x)
    kernel = np.ones((x, x), np.uint8)
    img_erosion = cv2.erode(mask, kernel, iterations=1)

    # Removing the original mask from the folder and writing the eroded mask to it
    os.remove(mask_path)
    cv2.imwrite(mask_path, img_erosion)

    # Opening and resizing the eroded mask fill the attribute mask_list from the object lists with that mask at the
    # current image number
    mask = Image.open(mask_path)
    mask = ImageTk.PhotoImage(mask.resize((int(0.8*w), int(0.8*h))))
    lists.mask_list[img_nr.img_number] = mask

    # Opening and resizing black image
    black = cv2.imread('black.png')
    black = cv2.resize(black, (760, 428))

    # Resizing the eroded mask
    img_erosion = cv2.resize(img_erosion, (760, 428))

    # Opening and resizing the image
    image_path = 'images/' + image_name
    image = cv2.imread(image_path)
    image = cv2.resize(image, (760, 428))

    # Creating the new mask_image_merge and replacing the old one in the folder
    mask_image_merge = np.where(img_erosion==0, black, image)
    mask_image_merge_path = 'image_mask_merge/' + image_name
    os.remove(mask_image_merge_path)
    cv2.imwrite(mask_image_merge_path, mask_image_merge)

    # Opening mask_image_merge with pillow and changing the attribute mask_image_merge_list from the object lists at the
    # current image number to the new mask_image_merge
    pillow_mask_image_merge = Image.open(mask_image_merge_path)
    pillow_mask_image_merge = ImageTk.PhotoImage(pillow_mask_image_merge.resize((int(0.8 * w), int(0.8 * h))))
    lists.mask_image_merge_list[img_nr.img_number] = pillow_mask_image_merge

    redo_mask_list = False
    displaying_current_image(lists, all_canvas, label_dict_select_area, img_nr, redo_mask_list, label_buttons)

def dilation(x, w, h, images, lists, all_canvas, label_dict_select_area, img_nr, label_buttons):
    '''Function responsible for the dilation of the masks with different kernel sizes'''

    # Opening the mask
    image_name = images[img_nr.img_number]
    mask_path = 'masks/' + image_name
    mask = cv2.imread(mask_path)

    # Creating dilated image of mask with kernel size (x,x)
    kernel = np.ones((x, x), np.uint8)
    img_dilation = cv2.dilate(mask, kernel, iterations=1)

    # Removing the original mask from the folder and writing the dilated mask to it
    os.remove(mask_path)
    cv2.imwrite(mask_path, img_dilation)
    mask = Image.open(mask_path)
    mask = ImageTk.PhotoImage(mask.resize((int(0.8*w), int(0.8*h))))
    lists.mask_list[img_nr.img_number] = mask

    # Opening and resizing black image
    black = cv2.imread('black.png')
    black = cv2.resize(black, (760, 428))

    # Resizing the eroded mask
    img_dilation = cv2.resize(img_dilation, (760, 428))

    # Opening and resizing the image
    image_path = 'images/' + image_name
    image = cv2.imread(image_path)
    image = cv2.resize(image, (760, 428))

    # Creating the new mask_image_merge and replacing the old one in the folder
    mask_image_merge = np.where(img_dilation==0, black, image)
    mask_image_merge_path = 'image_mask_merge/' + image_name
    os.remove(mask_image_merge_path)
    cv2.imwrite(mask_image_merge_path, mask_image_merge)

    # Opening mask_image_merge with pillow and changing the attribute mask_image_merge_list from the object lists at the
    # current image number to the new mask_image_merge
    pillow_mask_image_merge = Image.open(mask_image_merge_path)
    pillow_mask_image_merge = ImageTk.PhotoImage(pillow_mask_image_merge.resize((int(0.8 * w), int(0.8 * h))))
    lists.mask_image_merge_list[img_nr.img_number] = pillow_mask_image_merge

    redo_mask_list = False
    displaying_current_image(lists, all_canvas, label_dict_select_area, img_nr, redo_mask_list, label_buttons)

def get_pixel(root, all_canvas, img_nr, images):
    '''This function gets the pixel value of the mask at the position we click the mouse on the image. It displays the
    value on canvas, but deletes it also'''

    def get_pixel_value(event):
        '''This function gets the pixel value of the mask at the coordinates of the mouse press. It displays the
        coordinates on the canvas.'''

        # Getting the coordinates of the event "mouse press".
        coordinates = event.x, event.y

        # Getting the pixel value of the mask
        pixel_value = current_mask[coordinates[1]][coordinates[0]][0]

        # Displaying the pixel values on canvas at position (5,0).
        display_text = 'Mask Pixel Value: ' + str(pixel_value)
        all_canvas.canvas.create_text(5, 0, anchor = tk.NW, fill="darkblue",
                            text=display_text, font = 'Times 16', tag = 'text')

    def stop_get_pixel_value(event):
        '''This function deletes the text created on the canvas in the function get_pixel_value again'''

        # Deleting the item with tag 'text' (see line 189 in get_pixel_value) on the canvas
        all_canvas.canvas.delete('text')

    # Opening the mask at the current image number
    current_mask_path = 'masks/' + images[img_nr.img_number]
    current_mask = cv2.imread(current_mask_path)

    # Binding the mouse press to the function get_pixel_value
    root.bind("<ButtonPress-1>", get_pixel_value)
    # Binding the mouse release to the function stop_get_pixel_value
    root.bind("<ButtonRelease-1>", stop_get_pixel_value)

def make_blank(images, img_nr, lists, all_canvas, label_dict_select_area, label_buttons):
    '''This function replaces the masks and the mask_image_merges with black images'''

    # Removing the masks and mask_image_merge at the current image number from the folders
    mask_path = 'masks/' + images[img_nr.img_number]
    mask_merge_path = 'image_mask_merge/' + images[img_nr.img_number]
    os.remove(mask_path)
    os.remove(mask_merge_path)

    # Opening and resizing the black image
    black = cv2.imread('black.png')
    black = cv2.resize(black, (760,428))

    # Writing the black image to the
    cv2.imwrite(mask_path, black)
    cv2.imwrite(mask_merge_path, black)

    # redo_mask_list = True, because we have not updated the attributes masks, mask_image_merge in the object lists.
    # One could implement this in the code and the tool would be faster. But this button will probabely not be used
    # often.
    redo_mask_list = True
    displaying_current_image(lists, all_canvas, label_dict_select_area, img_nr, redo_mask_list, label_buttons)

def dbscan(images, img_nr, lists, w, h, all_canvas, label_dict_select_area, label_buttons, pixel_value):
    '''This function executes the dbscan algorithm on the mask'''

    # Opening the mask at the current image number
    mask_path = 'masks/' + images[img_nr.img_number]
    mask = cv2.imread(mask_path)

    # Converting the mask from the BGR to the GRAY colorspace
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    # Creating an empty list, where the coordinates of the white pixels (value larger than 0) will be saved
    coordinates_of_white_pixels = []

    # Getting the mask's number of rows and columns (pixels in height and width)
    rows, cols = mask.shape[:2]

    # Looping through all the pixels and checking if the pixel value is equal to our label, or the pixel value of in
    # other words, the mask. If this is the case, append it to the list coordinates_of_white_pixels
    for i in range(rows):
        for j in range(cols):
            if mask[i, j] == pixel_value:
                coordinates_of_white_pixels.append([i, j])

    # Create a numpy array of the list coordinates_of_white_pixels
    X = np.asarray(coordinates_of_white_pixels)
    # Initiating a dbscan model 'model' with two epochs and a 9 minimum number of samples
    model = DBSCAN(eps=2, min_samples=9)
    # Predict the clusters
    yhat = model.fit_predict(X)
    # Create list of clusters
    clusters = np.unique(yhat)

    # Initializing two variables for the size and index of the cluster in the list 'clusters' as zero.
    size_of_biggest_cluster = 0
    index_od_biggest_cluster = 0
    # Looping through all the clusters in the list 'clusters'
    for cluster in clusters:
        # List of pixels in the current cluster
        row_ix = np.where(yhat == cluster)
        # In this if statement, we check if the size of the current cluster is larger then the variable
        # size_of_biggest_cluster. If that is the case, size_of_biggest_cluster gets overwritten with the size of the
        # current cluster and the index_of_the_current cluster gets overwritten with the index of the current cluster
        # (cluster)
        if row_ix[0].size > size_of_biggest_cluster:
            size_of_biggest_cluster = row_ix[0].size
            index_od_biggest_cluster = cluster

    # Looping through all clusters in the list of cluster again
    for cluster in clusters:
        # If it is the biggest cluster, do nothing
        if cluster == index_od_biggest_cluster:
            continue
        # If it is not the biggest cluster, save the coordinates of the cluster as lists x_coord_to_delete_mask and
        # y_coord_to_delete_mask. Loop through the lists and set all pixels values to 0 (black)
        else:
            row_ix = np.where(yhat == cluster)
            x_coord_to_delete_mask = X[row_ix, 0]
            y_coord_to_delete_mask = X[row_ix, 1]
            for i in range(len(x_coord_to_delete_mask[0])):
                mask[x_coord_to_delete_mask[0][i], y_coord_to_delete_mask[0][i]] = 0

    # Delete the mask from the folder and write the new mask to it
    os.remove(mask_path)
    cv2.imwrite(mask_path, mask)

    # Opening and resizing the mask add it to the attribute mask_list in the objects lists at the current image number
    mask_pillow = Image.open(mask_path)
    mask_pillow = ImageTk.PhotoImage(mask_pillow.resize((int(0.8 * w), int(0.8 * h))))
    lists.mask_list[img_nr.img_number] = mask_pillow

    # Opening and resizing the black image
    black = cv2.imread('black.png')
    black = cv2.resize(black, (760, 428))

    # Opening the image at the current image number
    image_path = 'images/' + images[img_nr.img_number]
    image = cv2.imread(image_path)

    # converting the mask from gray to bgr colorspace
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    # Merging the image and mask, so that image pixels stay the same, where the mask pixels are white and the image
    # pixels become black where the mask pixels are black
    image_merge = np.where(mask == 0, black, image)
    # Path to mask_image_merge
    mask_image_merge_path = 'image_mask_merge/' + images[img_nr.img_number]
    # Removing the old mask_image_merge from the folder
    os.remove(mask_image_merge_path)
    # Writing the new mask_image_merge into the folder
    cv2.imwrite(mask_image_merge_path, image_merge)

    # Opening and resizing mask_image_merge
    mask_merge_pillow = Image.open(mask_image_merge_path)
    mask_merge_pillow = ImageTk.PhotoImage(mask_merge_pillow.resize((int(0.8 * w), int(0.8 * h))))
    # Add mask_image_merge to attribute mask_image_merge_list in object lists at the current image number
    lists.mask_image_merge_list[img_nr.img_number] = mask_merge_pillow

    redo_mask_list = False
    displaying_current_image(lists, all_canvas, label_dict_select_area, img_nr, redo_mask_list, label_buttons)
