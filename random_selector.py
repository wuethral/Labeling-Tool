import cv2 as cv
import os

image_names = os.listdir('images')
number_of_images = len(image_names)
images_selection_step = int(number_of_images/30 - 1)
for i in range(30):
    image_name = image_names[i * images_selection_step]
    image_path = 'images/' + image_name
    mask_path = 'bounding_boxes/' + image_name
    image = cv.imread(image_path)
    mask = cv.imread(mask_path)
    saving_path_image = 'DataSet/images/' + image_name
    saving_path_masks = 'DataSet/masks/' + image_name
    cv.imwrite(saving_path_image, image)
    cv.imwrite(saving_path_masks, mask)
