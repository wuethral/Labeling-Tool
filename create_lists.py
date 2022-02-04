import os
from PIL import Image, ImageTk
import cv2
import numpy as np


class CreateImageList:

    def __init__(self, path, images, w, h):
        self.path = path
        self.images = images
        self.w = w
        self.h = h
        self.image_list = []
        self.cv2_rgb_image_list = []
        self.cv2_hsv_image_list = []
        self.mask_list = []
        self.mask_image_merge_list = []
        self.length = 0
        self.create_image_list()
        self.len()
        self.creating_masks_list()




    def create_image_list(self):
        for f in self.images:
            imagePath = os.path.join(self.path, f)
            if imagePath != self.path + '\\.DS_Store':
                picture = Image.open(imagePath)
                img = ImageTk.PhotoImage(picture.resize((self.w, self.h)))
                self.image_list.append(img)
                cv2_image = cv2.imread(imagePath)
                self.cv2_rgb_image_list.append(cv2_image)
                cv2_image = cv2.resize(cv2_image, (self.w, self.h))
                hsv_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2HSV)
                self.cv2_hsv_image_list.append(hsv_image)
    def len(self):
        self.length = len(self.image_list)

    def creating_masks_list(self):

        mask_names = os.listdir('bounding_boxes')
        black = Image.open('black.png')
        black = ImageTk.PhotoImage(black.resize((int(0.8 * self.w), int(0.8 * self.h))))
        for mask_name in mask_names:
            mask_path = 'bounding_boxes/' + mask_name
            mask = Image.open(mask_path)
            mask = ImageTk.PhotoImage(mask.resize((int(0.8*self.w), int(0.8*self.h))))
            self.mask_list.append(mask)
            image_path = 'images/' + mask_name
            image = cv2.imread(image_path)
            image = cv2.resize(image, (int(0.8*self.w), int(0.8*self.h)))
            black = cv2.imread('black.png')
            black = cv2.resize(black, (int(0.8 * self.w), int(0.8 * self.h)))
            mask = cv2.imread(mask_path)
            mask = cv2.resize(mask, (int(0.8 * self.w), int(0.8 * self.h)))
            mask_image_merge = np.where(mask==0, black, image)
            mask_image_merge_path = 'image_mask_merge/' + mask_name
            mask_image_merge_path_copy = 'image_mask_merge_copy/' + mask_name
            cv2.imwrite(mask_image_merge_path, mask_image_merge)
            cv2.imwrite(mask_image_merge_path_copy, mask_image_merge)
            mask_image_merge = Image.open(mask_image_merge_path)
            mask_image_merge = ImageTk.PhotoImage(mask_image_merge.resize((int(0.8*self.w), int(0.8*self.h))))
            self.mask_image_merge_list.append(mask_image_merge)
        print('xxxx',len(self.mask_image_merge_list))
        print('yyyy',len(self.mask_list))


