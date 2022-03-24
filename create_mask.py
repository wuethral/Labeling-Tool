from IPython.display import Image
from PIL import Image
import os
import cv2 as cv
import numpy as np


class ListOfPixelValues():
    '''Class for list of pixel values'''

    def __init__(self):

        # Initializing object list_of_pixel_values as an empty dictionary
        self.list_of_pixel_values = []

    def append_one(self):
        '''This function appends 1 to self.list_of_pixel_values'''

        self.list_of_pixel_values.append(1)

    def append_zero(self):
        '''This function appends 0 to self.list_of_pixel_values'''

        self.list_of_pixel_values.append(0)

    def make_empty(self):
        '''This function deletes all elements in the list self.list_of_pixel_values (Making dictionary empty)'''

        self.list_of_pixel_values = []


def stacking_masks(old_mask, pix, w, h, label, image_name):
    '''this function stacks the initial mask without the newly created mask from the polygon and the newly created mask
    from the polygon together'''

    # Looping through all pixels
    for x in range(w):
        for y in range(h):
            # If the pixel is part of the new mask, add the label pixel to the old, initial mask
            if pix[x, y] != 0:
                old_mask[y, x] = int(label)

    # Writing the changed mask to the folder at the current image
    saving_path = 'masks/' + image_name
    cv.imwrite(saving_path, old_mask)

    # Convert the newly created mask from Gray to BGR
    old_mask = cv.cvtColor(old_mask, cv.COLOR_GRAY2BGR)
    # Open and resize the image (corresponding to mask)
    image_path = 'images/' + image_name
    image = cv.imread(image_path)
    image = cv.resize(image,(int(w),int(h)))
    # Open and resize the black image
    black = cv.imread('black.png')
    black = cv.resize(black, (int(w),int(h)))

    # Merging the image and mask, so that image pixels stay the same, where the mask pixels are white and the image
    # pixels become black where the mask pixels are black
    image_merge = np.where(old_mask == 0, black, image)
    image_merge_path = 'image_mask_merge/' + image_name
    # Removing old image_mask_merge from folder and saving new one the the same path
    os.remove(image_merge_path)
    cv.imwrite(image_merge_path, image_merge)


def create_final_mask(w, h, image_number, label, images, image_name, list_of_pixels):
    '''This function creates the mask of the drawn polygon'''

    # Creating a new image in RGB color mode and with width w and height h
    im = Image.new("RGB", (w, h))
    # Converting im to a grayscale image
    gray = im.convert('L')
    # Making the pixels from gray 0 and saving the image as bw
    bw = gray.point(lambda x: 0, '1')
    # Accessing the pixel of bw
    pix = bw.load()
    # Initializing the variable pixel value with 0
    pixel_position = 0

    # Accessing and reading the mask from the folder
    old_mask_path = 'masks/' + images[image_number]
    old_mask = cv.imread(old_mask_path)
    # Converting the mask from colorspace BGR to GRAY and resizing the mask
    old_mask = cv.cvtColor(old_mask, cv.COLOR_BGR2GRAY)
    old_mask = cv.resize(old_mask, (int(w), int(h)))

    # Looping through all pixels
    for x in range(w):
        for y in range(h):
            # If the pixel at position pixel_position in the attribute list_of_pixel_values in the object list_of_pixels
            # is 1, the pixel value becomes the value of the label (Because the point lies inside of polygon and becomes
            # part of mask)
            if list_of_pixels.list_of_pixel_values[pixel_position] == 1:
                pix[x, y] = int(label)
            # Else, the pixel is not part of the mask and becomes 0
            else:
                pix[x, y] = 0
            # Adding 1 to pixel_position to be one position further in list_of_pixels.list_of_pixel_values
            pixel_position += 1

    # Stacking the initial mask with the newly created mask (polygon)
    stacking_masks(old_mask, pix, w, h, label, image_name)

    # Making list_of_pixels empty for the creation of the next mask
    list_of_pixels.make_empty()


def is_left_or_right(x_coord_pt_1,  y_coord_pt_1,  x_coord_pt_2, y_coord_pt_2, x, y):
    '''Checking if point lies to the left or right of the line by calculating their cross product'''

    # Calculating cross product to check if the point lies on the right or left side of the line
    cross_product = (y_coord_pt_2 - y) * (x_coord_pt_2 - x_coord_pt_1) - (x_coord_pt_2 - x) * \
                    (y_coord_pt_2 - y_coord_pt_1)

    return cross_product

def check_winding_number_2(coord_pt_1, coord_pt_2, x, y):
    '''Checking for valid upward and downward crossings, in order to evaluate if there was a winding around the point'''

    # x and y coordinates of the first and second point of the line
    x_coord_pt_1 = coord_pt_1[0]
    y_coord_pt_1 = coord_pt_1[1]
    x_coord_pt_2 = coord_pt_2[0]
    y_coord_pt_2 = coord_pt_2[1]

    # Checking if y coordinate of point is smaller or equal to the y coordinate of the first point of the line
    if y_coord_pt_1 >= y:
        # Checking if y coordinate of point is larger then the y coordinate of the second point of the line
        if y_coord_pt_2 < y:
            # Checking if the point lies on the left or right side of the line
            if is_left_or_right(x_coord_pt_1,  y_coord_pt_1,  x_coord_pt_2, y_coord_pt_2, x, y) < 0:
                # Pixel lies on left side of line
                return 1
            else:
                # Pixel lies on right side of line
                return 0
        # If y coordinate of point is smaller the the y coordinate of the second point of the line, return 0
        else:
            return 0
    # Checking if y coordinate of point is larger then the y coordinate of the first point of the line
    elif y_coord_pt_1 < y:
        # Checking if y coordinate of point is smaller or equal to the y coordinate of the first point of the line
        if y_coord_pt_2 >= y:
            # Checking if the point lies on the left or right side of the line
            if is_left_or_right(x_coord_pt_1,  y_coord_pt_1,  x_coord_pt_2, y_coord_pt_2, x, y) > 0:
                # Lies on the right side of line
                return -1
            # pixel lies on line. Return 5, so that winding in check_winding_number is nonzero for sure
            elif is_left_or_right(x_coord_pt_1, y_coord_pt_1, x_coord_pt_2, y_coord_pt_2, x, y) == 0:
                return 5
            # Pixel lies on the left side of line
            else:
                return 0
        # If y coordinate of point is larger to the y coordinate of the first point
        else:
            return 0
    # If y coordinate of point is something else, return 0
    else:
        return 0


def check_winding_number(x, y, coordinates_of_one_label, list_of_pixels):
    '''Checking for every pixel, if it lies inside or outside of the polygon'''

    # Setting a variable winding to 0, which will be used to count the windings
    winding = 0

    # Looping through the coordinate points of the polygon, except the last one
    for coord_pt in range(len(coordinates_of_one_label)-1):
        # Calling check_winding_number_2, that checks for every line, if there was an upward or downward crossing for
        # the point, meaning that the line crosses the axis paralleL to x through the point of interest
        wind_count = check_winding_number_2(coordinates_of_one_label[coord_pt], coordinates_of_one_label[coord_pt+1],
                                            x, y)
        # Summing the wind_counts (for the lines of the polygon)
        winding += wind_count

    # Doing the same as in line 118-224 for the last line (second last to last corner coordinate)
    wind_count_2 = check_winding_number_2(coordinates_of_one_label[-1], coordinates_of_one_label[0],x,y)
    winding += wind_count_2

    # If the winding number is 0, the pixel is outside of the polygon. Therefore zero is appended to list_of_pixels.
    if winding == 0:
        list_of_pixels.append_zero()
    # If the winding number is nonzero, the pixel is inside of the polygon. Therefore one is appended to list_of_pixels.
    else:
        list_of_pixels.append_one()


def mask_creation_per_label(w, h, coordinates_of_one_label, image_number, label, images):
    '''This function loops through every pixel in the image and calls function to check if point lies inside or outside
    of the poygon'''

    # Create object from the class ListOfPixelValues which will later be filled with 0 or the label pixel
    list_of_pixels = ListOfPixelValues()

    # Looping through every pixel in the image
    for x in range(w):
        for y in range(h):
            # Calling the function check_winding_number, which will check if the pixel lies inside or outside of the
            # polygon
            check_winding_number(x, y, coordinates_of_one_label, list_of_pixels)

    # After deciding for every point, if it part of the mask or not, the final mask can be created
    create_final_mask(w, h, image_number, label, images, images[image_number], list_of_pixels)


def mask_creation_per_image(w, h, labels_on_this_image_number, list_of_labels, image_number, images):
    '''This function accesses every polygon with its corresponding coordinates in laels_on_this_image_number and
     passes them into the function mask_creation_per_label'''

    # Looping through every label in list_of_label (All labels are in this list)
    for label in list_of_labels:
        # Checking if the current label is a key of labels_on_this_image_number
        if label in labels_on_this_image_number.keys():
            # Accessing label in labels_on_this_image_number (Access to polygons with corner coordinates)
            corner_coordinates_of_labels_on_image_number = labels_on_this_image_number[label]
            # Looping through all all polygons in corner_coordinates_of_labels_on_image_number
            for coordinates_of_one_label in corner_coordinates_of_labels_on_image_number:
                # Calling the function mask_creation_per_label
                mask_creation_per_label(w, h, coordinates_of_one_label, image_number, label, images)


def mask_creation(w, h, number_of_images, list_of_labels, dict_label_dict_select_area, images):
    '''This function loops through the single images. We take hold of one image and we call the function mask_creation_per_image
    where we pass the labels on this page, the list of labels and the image number. also the image width and height'''
    # Looping through every image
    for image_number in range(number_of_images):
        # Checking if the image is a key in the dict_label_dict_select_area
        if image_number in dict_label_dict_select_area.keys():
            # Accessing dict_label_dict_select_area at the specific image number
            labels_on_this_image_number = dict_label_dict_select_area[image_number]
            # Call the function mask_create_per_image
            mask_creation_per_image(w, h, labels_on_this_image_number, list_of_labels, image_number, images)

