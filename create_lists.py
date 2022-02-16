import os
from PIL import Image, ImageTk
import cv2
import numpy as np


class CreateImageList:
    '''this class creates the lists of images, mask and mask with images merged that are displayed in the different
    canvases.'''

    def __init__(self, path, images, w, h):
        self.path = path
        self.images = images
        self.w = w
        self.h = h
        self.image_list = []
        self.mask_list = []
        self.mask_image_merge_list = []
        self.length = 0

    def create_image_list(self):
        '''Appending the images to the list self.image_list'''

        # Looping through the images_names in self.images
        for f in self.images:
            # Creating the path to the images
            imagePath = os.path.join(self.path, f)
            # Checking that only files with right format are loaded
            if imagePath != self.path + '\\.DS_Store':
                # Reading image with PIL function 'Image', resizing it and appending it to self.image_list
                picture = Image.open(imagePath)
                img = ImageTk.PhotoImage(picture.resize((self.w, self.h)))
                self.image_list.append(img)

    def creating_masks_list(self):
        '''Appending the masks to the list self.image_list. Creating the images mask_image_merge and appending them
        to the list self.mask_image_merge_list.'''

        # Creating a list of the names in the folder bounding_boxes
        mask_names = os.listdir('bounding_boxes')

        # Looping through the names in the list mask_names
        for mask_name in mask_names:
            # Creating path to masks, opening and resizing masks, and appending it to the list self.mask_list
            mask_path = 'bounding_boxes/' + mask_name
            mask = Image.open(mask_path)
            mask = ImageTk.PhotoImage(mask.resize((int(0.8*self.w), int(0.8*self.h))))
            self.mask_list.append(mask)

            # Reading and resizing images with open-cv
            image_path = 'images/' + mask_name
            image = cv2.imread(image_path)
            image = cv2.resize(image, (int(0.8*self.w), int(0.8*self.h)))

            # Reading black image form path 'black.png' and resizing it
            black = cv2.imread('black.png')
            black = cv2.resize(black, (int(0.8 * self.w), int(0.8 * self.h)))

            # Reading and resizing mask with open-cv
            mask = cv2.imread(mask_path)
            mask = cv2.resize(mask, (int(0.8 * self.w), int(0.8 * self.h)))

            # With np.where, The image pixel is set to black, where the mask pixel is black, and the image pixel stays
            # as it is, where the mask pixel is not black.
            mask_image_merge = np.where(mask==0, black, image)
            # Path where these mask_image_merge will be written to
            mask_image_merge_path = 'image_mask_merge/' + mask_name
            # Path for duplicate
            mask_image_merge_path_copy = 'image_mask_merge_copy/' + mask_name
            # Writing mask_image_merge both pathes
            cv2.imwrite(mask_image_merge_path, mask_image_merge)
            cv2.imwrite(mask_image_merge_path_copy, mask_image_merge)
            mask_image_merge = Image.open(mask_image_merge_path)
            # Opening the images from mask_image_merge_path with Image from the library PIL. Resizing it and appending
            # it to the mask_image_merge_list
            mask_image_merge = ImageTk.PhotoImage(mask_image_merge.resize((int(0.8*self.w), int(0.8*self.h))))
            self.mask_image_merge_list.append(mask_image_merge)

    def len(self):
        '''This function calculates the length of the attribute self.image_list'''

        self.length = len(self.image_list)

    def update_lists(self):
        '''This function updates the attributes self.image_list, self.mask_list and self.mask_image_merge_list'''

        # Making the lists empty
        self.image_list = []
        self.mask_list = []
        self.mask_image_merge_list = []

        # Call these functions to refill self.image_list, self.mask_list and self.mask_image_merge_list
        self.create_image_list()
        self.creating_masks_list()


class DictCoordinates():
    '''In this class the coorner coordinates of the polygon in the hand labeling are saved and deleted'''

    def __init__(self):
        self.dict = {}

    def delete(self, img_nr, lab):
        '''Deleting an element in self.dict at specific image number and label'''

        del self.dict[img_nr][lab]


