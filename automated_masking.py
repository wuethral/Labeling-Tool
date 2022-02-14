import os
import cv2 as cv


pixel_value = -1



def check_pixel_green(hsv_img, x, y, h_green_min, h_green_max, s_green_min, s_green_max, v_green_min, v_green_max):
    if hsv_img[y, x][0] >= h_green_min - 2 and hsv_img[y, x][0] <= h_green_max + 2 and hsv_img[y, x][
        1] >= s_green_min - 2 and hsv_img[y, x][1] <= s_green_max + 2 and hsv_img[y, x][2] >= v_green_min - 2 and \
            hsv_img[y, x][2] <= v_green_max + 2:  # checking, if pixel is green
        return True


def make_absolute_value(number):
    if number >= 0:
        return number
    elif number < 0:
        number = number * (-1)
        return number


def check_gradient(hvtp, hvnp):
    absolute_h_difference = make_absolute_value(int(hvtp[0]) - int(hvnp[0]))
    absolute_s_difference = make_absolute_value(int(hvtp[1]) - int(hvnp[1]))
    absolute_v_difference = make_absolute_value(int(hvtp[2]) - int(hvnp[2]))
    # print(hvtp[0])
    # print(hvnp[0])
    # print(absolute_h_difference)
    # print('')

    if absolute_h_difference > 100 or absolute_s_difference > 100 or absolute_v_difference > 100:
        return 'transition'
    else:
        return 'no_transition'


def find_transition(hsv_image, width, y, min_or_max):
    if min_or_max == 'min':
        x_transition = width
        for x in range(width - 1):
            hsv_value_this_pixel = hsv_image[y, x]
            hsv_value_next_pixel = hsv_image[y, x + 1]
            transition_check = check_gradient(hsv_value_this_pixel, hsv_value_next_pixel)
            if transition_check == 'transition':
                x_transition = x
                break
    if min_or_max == 'max':
        x_transition = 0
        for x in range(1, width, 1):
            hsv_value_this_pixel = hsv_image[y, width - x]
            hsv_value_next_pixel = hsv_image[y, width - x - 1]
            transition_check = check_gradient(hsv_value_this_pixel, hsv_value_next_pixel)
            if transition_check == 'transition':
                x_transition = x
                break

    return x_transition


def create_bounding_box(hsv_image, width, height):
    x_min = width
    x_max = 0
    for y in range(height - 1):
        x_transition_min = find_transition(hsv_image, width, y, 'min')
        x_transition_max = find_transition(hsv_image, width, y, 'max')
        if x_transition_min < x_min:
            x_min = x_transition_min
        if x_transition_max > x_max:
            x_max = x_transition_max

    return x_min, x_max


def check_hsv(hsv_pixel):
    return hsv_pixel[0], hsv_pixel[1], hsv_pixel[2]

def automated_masking(pixel_value):

    image_names = os.listdir('images')
    for image_name in image_names:

        image_path = 'images/' + image_name

        image_0 = cv.imread(image_path)
        height = image_0.shape[0]
        width = image_0.shape[1]

        print(image_name)
        image = cv.imread(image_path)
        hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        x_min, x_max = create_bounding_box(hsv_image, width, height)


        if (x_min - 80) < -60:
            x_min = 0
        elif (x_min - 80) < -40:
            x_min = 100
        elif (x_min - 40) < -20:
            x_min = 120
        elif (x_min - 20) < -10:
            x_min = 140
        elif (x_min - 80) < 0:
            x_min = 150


        if (x_max + 80) > width:
            x_max = width-80
        print('xxxxx')
        print(x_min, x_max)
        print(width, height)
        print('xxxxx')
        h_min = 360
        h_max = 0
        s_min = 360
        s_max = 0
        v_min = 360
        v_max = 0


        for y in range(height):

            for x in range(x_min - 80):
                h, s, v = check_hsv(hsv_image[y, x])
                image[y, x] = (0, 0, 0)
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


            for x in range(x_max + 80, width, 1):
                h, s, v = check_hsv(hsv_image[y, x])
                image[y, x] = (0, 0, 0)
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

            for x in range(x_min - 80, x_max + 80, 1):

                if check_pixel_green(hsv_image, x, y, h_min, h_max, s_min, s_max, v_min, v_max):
                    image[y, x] = (0, 0, 0)
                else:
                    image[y, x] = (pixel_value, pixel_value, pixel_value)



        image = cv.resize(image, (760,428))
        print(image.size)
        saving_path = 'bounding_boxes/' + image_name
        saving_path_2 = 'bounding_boxes_copy/' + image_name
        cv.imwrite(saving_path, image)
        cv.imwrite(saving_path_2, image)

        winname = 'Mask'
        cv.namedWindow(winname)
        cv.moveWindow(winname, 0, 0)
        newsize = (int(width*2), int(height*2))
        mask_green_black_hsv = cv.resize(image, newsize)
        cv.imshow(winname, mask_green_black_hsv)
        cv.waitKey(10)
