import os
import cv2 as cv


def check_pixel_green(hsv_img, x, y, h_green_min, h_green_max, s_green_min, s_green_max, v_green_min, v_green_max):
    '''This function returns True, if h, s and v values of a pixel lie in a certain threshold'''

    # When checking, if the number lies in between thresholds, 2 is subtracted from the minimum values and 2 added to
    # the maximum values. This is a margin in order that not too little pixels are classified as green. Of course,
    # depending on the case, this margin could be changed
    if h_green_min - 2 <= hsv_img[y, x][0] <= h_green_max + 2 \
            and s_green_min - 2 <= hsv_img[y, x][1] <= s_green_max + 2 \
            and v_green_min - 2 <= hsv_img[y, x][2] <= v_green_max + 2:
        return True


def make_absolute_value(number):
    '''This function returns the absolute value of a number'''

    if number >= 0:
        return number
    elif number < 0:
        number = number * (-1)
        return number


def check_gradient(hvtp, hvnp):
    '''This function calculates the gradient of two neighbouring pixels and if a certain threshold is reached for it to
     be a valid to be a valid transition'''

    # Calculating the absolute value of the difference in pixel value for the neighbouring pixels for the h, s and v
    # values
    absolute_h_difference = make_absolute_value(int(hvtp[0]) - int(hvnp[0]))
    absolute_s_difference = make_absolute_value(int(hvtp[1]) - int(hvnp[1]))
    absolute_v_difference = make_absolute_value(int(hvtp[2]) - int(hvnp[2]))

    # If one or more of the transition values is larger then 100, it is a transition, else not. Depending on the tool,
    # these values can be changed.
    if absolute_h_difference > 100 or absolute_s_difference > 100 or absolute_v_difference > 100:
        return 'transition'
    else:
        return 'no_transition'


def find_transition(hsv_image, width, y, min_or_max):
    '''This function finds the x coordinate of the transition form green screen to tool'''

    # Checking min_or_max variable
    if min_or_max == 'min':
        # Setting x_transition to the maximum possible value, which is the width
        x_transition = width

        # Looping through all x coordinates
        for x in range(width - 1):
            # Checking the hsv_pixel of the current position and the one of one pixel further in the x-direction
            hsv_value_this_pixel = hsv_image[y, x]
            hsv_value_next_pixel = hsv_image[y, x + 1]
            # checking, if there is a transition from the green screen to the object or not
            transition_check = check_gradient(hsv_value_this_pixel, hsv_value_next_pixel)
            if transition_check == 'transition':
                # if this statement is true, the x-transition coordinate is the current x in the loop
                x_transition = x
                # We can break, because when we have the first transition, we don't have to check the other pixels
                break
    elif min_or_max == 'max':
        # Setting x_transition to the minimum possible value, which 0
        x_transition = 0

        # Looping through all x coordinates
        for x in range(1, width, 1):
            # Checking the hsv_pixel of the position width-x, because we loop through the negative x-direction
            hsv_value_this_pixel = hsv_image[y, width - x]
            # Checking the hsv_pixel of the position wdith-x-y
            hsv_value_next_pixel = hsv_image[y, width - x - 1]
            # checking, if there is a transition from the green screen to the object or not
            transition_check = check_gradient(hsv_value_this_pixel, hsv_value_next_pixel)
            if transition_check == 'transition':
                # if this statement is true, the x-transition coordinate is the current x in the loop
                x_transition = x
                # We can break, because when we have the first transition, we don't have to check the other pixels
                break

    return x_transition


def create_bounding_box(hsv_image, width, height):
    '''This function determines the minimum and maximum values in the x-direction from the tool'''

    # Setting the minimum value of x to the max possible value, which is the width of the image
    x_min = width
    # Setting the maximum value of x to the min possible value, which is 0
    x_max = 0

    # Looping through the whole y-axis of the image's coordinates system (in pixels) and finding the maximum and minimum
    # value of the tool in the x-direction over the whole image
    for y in range(height - 1):
        x_transition_min = find_transition(hsv_image, width, y, 'min')
        x_transition_max = find_transition(hsv_image, width, y, 'max')
        if x_transition_min < x_min:
            x_min = x_transition_min
        if x_transition_max > x_max:
            x_max = x_transition_max

    return x_min, x_max


def bounding_box_x_coordinates(x_min, x_max, width):
    '''This function makes an margin to x_min and x_max. If we get out of bounds, the offset is adjusted'''

    # Making and offset of -80 to x_min. If bounding_box_min gets out of bounds, set it to 20.
    # These values can be adjusted
    bounding_box_min = x_min - 80
    if bounding_box_min < 0:
        bounding_box_min = 20

    # Making and offset of +80 to x_max. If bounding_box_max gets out of bounds, set it to width - 20.
    # These values can be adjusted
    bounding_box_max = x_max + 80
    if bounding_box_max > width:
        bounding_box_max = width - 20

    return bounding_box_min, bounding_box_max


def check_hsv(hsv_pixel):
    '''This function return the h, s and v value of a pixel'''

    # order: h, s, v
    return hsv_pixel[0], hsv_pixel[1], hsv_pixel[2]


def get_min_max_hsv_out_of_bounding_box(bounding_box_min, bounding_box_max, width, height, hsv_image, image):
    '''Finding the max and min values of the h, s and v values outside of the bounding box and making the pixels outside
    of the bounding box black'''

    # Setting the min values to the maximum possible value 360
    h_min = 360
    s_min = 360
    v_min = 360
    # Setting the max values to the minimum possible value 0
    h_max = 0
    s_max = 0
    v_max = 0

    # Looping through all the y axis (pixels)
    for y in range(height):
        # Looping through all the pixels on the left side of the bounding box (0 to bounding_box_min)
        for x in range(bounding_box_min):
            # Get hsv values of pixels
            h, s, v = check_hsv(hsv_image[y, x])

            # Making pixel black
            image[y, x] = (0, 0, 0)

            # If h, s and v values larger than current max and min values, replace the max and min values with the
            # current h, s, v values
            if h > h_max:
                h_max = h
            if h < h_min:
                h_min = h
            if s > s_max:
                s_max = s
            if s < s_min:
                s_min = s
            if v > v_max:
                v_max = v
            if v < v_min:
                v_min = v

        # Looping through all the pixels on the right side of the bounding box (bounding_box_may to width)
        for x in range(bounding_box_max, width, 1):
            # Get hsv values of pixels
            h, s, v = check_hsv(hsv_image[y, x])

            # Making pixel black
            image[y, x] = (0, 0, 0)

            # If h, s and v values larger than current max and min values, replace the max and min values with the
            # current h, s, v values
            if h > h_max:
                h_max = h
            if h < h_min:
                h_min = h
            if s > s_max:
                s_max = s
            if s < s_min:
                s_min = s
            if v > v_max:
                v_max = v
            if v < v_min:
                v_min = v

    # Return the max and min h, s, v values of the all pixels, that are not in the bounding box
    return h_max, h_min, s_max, s_min, v_max, v_min


def making_green_pixels_in_bounding_box_black(height, bounding_box_min, bounding_box_max, hsv_image, h_min, h_max,
                                              s_min, s_max, v_min, v_max, image, pixel_value):
    '''This function uses the max and min h, s and v values of the pixels outside of the bounding box and uses them as a
     threshold the determine, if a pixel inside of the bounding box is classified as green or not. If the pixel is
     green, it is turned to black, else turn it to the label (pixel value)'''

    # Looping through all pixels inside of the bounding box
    for y in range(height):
        for x in range(bounding_box_min, bounding_box_max, 1):
            # Checking if pixel green or not
            if check_pixel_green(hsv_image, x, y, h_min, h_max, s_min, s_max, v_min, v_max):
                # Turning green pixel black
                image[y, x] = (0, 0, 0)
            else:
                # Make h, s, and va value the value of the label
                image[y, x] = (pixel_value, pixel_value, pixel_value)

    return image

def automated_masking(pixel_value):

    # Creating list of image names in folder 'images'
    image_names = os.listdir('images')

    # Looping through tha image_names list
    for image_name in image_names:
        # Path to the image
        image_path = 'images/' + image_name
        # Opening the image and getting its height and width
        image = cv.imread(image_path)
        height = image.shape[0]
        width = image.shape[1]
        # Converting the image from BGR to HSV color space
        hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)

        # Getting the objects min and max coordinates in the x-direction over the whole image
        x_min, x_max = create_bounding_box(hsv_image, width, height)

        # Making an offset to x_min and x_max as a safety, that the tool is not cut off
        bounding_box_min, bounding_box_max = bounding_box_x_coordinates(x_min, x_max, width)

        # Finding the min and max values of the h, s and v values outside of the bounding box and making all pixels
        # outside of the bounding box black
        h_max, h_min, s_max, s_min, v_max, v_min = get_min_max_hsv_out_of_bounding_box(bounding_box_min,
                                                                                       bounding_box_max, width, height,
                                                                                       hsv_image, image)

        # based on the min and max values of h, s and v, a threshold for green or non-green pixel is set. With this
        # threshold, the pixels inside of the bounding box are turned black, if they are green.
        image = making_green_pixels_in_bounding_box_black(height, bounding_box_min, bounding_box_max, hsv_image, h_min,
                                                          h_max, s_min, s_max, v_min, v_max, image, pixel_value)

        # Resizing the image and saving it to the founder masks and masks_copy
        image = cv.resize(image, (760, 428))
        saving_path = 'masks/' + image_name
        saving_path_2 = 'masks_copy/' + image_name
        cv.imwrite(saving_path, image)
        cv.imwrite(saving_path_2, image)

        # Creating a window that displays the masks live during the process of the automated masking. This is
        # convenient, because one can check if the result is good or not. Of course it can be turned of by commenting.
        windowname = 'Mask'
        cv.namedWindow(windowname)
        cv.moveWindow(windowname, 0, 0)
        newsize = (int(width*2), int(height*2))
        mask_green_black_hsv = cv.resize(image, newsize)
        cv.imshow(windowname, mask_green_black_hsv)
        cv.waitKey(10)
