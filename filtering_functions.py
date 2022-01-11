import cv2 as cv
import numpy as np
from PIL import Image
from numpy import unique
from numpy import where
from sklearn.datasets import make_classification
from sklearn.cluster import DBSCAN
from matplotlib import pyplot
import msvcrt as m


def canny_edge_det(filename, img):
    # Convert to graycsale
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Blur the image for better edge detection
    img_blur = cv.GaussianBlur(img_gray, (3, 3), 0)

    # Sobel Edge Detection
    # sobelx = cv.Sobel(src=img_blur, ddepth=cv.CV_64F, dx=1, dy=0, ksize=5)  # Sobel Edge Detection on the X axis
    # sobely = cv.Sobel(src=img_blur, ddepth=cv.CV_64F, dx=0, dy=1, ksize=5)  # Sobel Edge Detection on the Y axis
    # sobelxy = cv.Sobel(src=img_blur, ddepth=cv.CV_64F, dx=1, dy=1, ksize=5)  # Combined X and Y Sobel Edge Detection
    # Display Sobel Edge Detection Images
    # cv.imshow('Sobel X', sobelx)
    # cv.waitKey(0)
    # cv.imshow('Sobel Y', sobely)
    # cv.waitKey(0)
    # cv.imshow('Sobel X Y using Sobel() function', sobelxy)
    # cv.waitKey(0)

    # Canny Edge Detection
    edges = cv.Canny(image=img_blur, threshold1=100, threshold2=200)  # Canny Edge Detection
    path = 'D:/masks/tools_with_hands(allvideos)/canny_edge_images/canny_edge_mask_' + filename +'_mask.png'
    cv.imwrite(path, edges)

    # Display Canny Edge Detection Image
    # cv.imshow('Canny Edge Detection', edges)
    # cv.waitKey(0)
    # cv.destroyAllWindows()


# img = cv.imread('C:/Users/wuethral/Desktop/colorfilter_2/14.9.21_try_2/Example_4/pliers.png')
# canny_edge_det(img)

def switch_pixel_row(row_array_hsv_filter, width):

    new_row_image_matrix = [0] * width

    for pixel_value in range(width):
        if row_array_hsv_filter[pixel_value] == 0:
            new_row_image_matrix[pixel_value] = 249
    new_row_image_matrix = np.array(new_row_image_matrix)
    return new_row_image_matrix

class SwitchingBlackWhite():

    def __init__(self, img_nr, mask_hsv_filter, height, width):
        self.img_nr = img_nr
        self.mask_hsv_filter = mask_hsv_filter
        self.height = height
        self.width = width
        self.switch_pixel()

    def switch_pixel(self):
        array_hsv_filter = np.array(self.mask_hsv_filter)
        mask_matrix = np.zeros((self.height, self.width))

        for i in range(self.height):
            new_row = switch_pixel_row(array_hsv_filter[i], self.width)
            mask_matrix[i, :] = new_row

        matrix_to_array = np.squeeze(np.asarray(mask_matrix))
        matrix_to_array = np.reshape(matrix_to_array, (self.height, self.width)).astype(np.uint8)
        switch_pixel_mask = Image.fromarray(matrix_to_array)

        path = "D:/masks/hands/hsv_switch_bw/hsv_switch_bw_" + str(self.img_nr) + '.png'
        switch_pixel_mask.save(path)

def check_pixel_green(hsv_img, x, y, h_green_min, h_green_max, s_green_min, s_green_max, v_green_min, v_green_max):

    if hsv_img[y, x][0] > h_green_min-1 and hsv_img[y, x][0] < h_green_max+1 and hsv_img[y, x][1] > s_green_min-1 and hsv_img[y, x][1] < s_green_max+1 and hsv_img[y, x][2] > v_green_min-1 and hsv_img[y, x][2] < v_green_max+1:  # checking, if pixel is green
        return True

def hsv_filter(filename_image, hsv, height, width, h_low, s_low, v_low, h_high, s_high, v_high):
    print('thresholds:', h_low, s_low, v_low, h_high, s_high, v_high)
    ''' 
    green_black_lower_hsv = np.array([40, 90, 80])
    green_black_higher_hsv = np.array([90, 255, 255])
    mask_green_black_hsv = cv.inRange(hsv, green_black_lower_hsv, green_black_higher_hsv)
    
    '''
    for x in range(width):
        for y in range(height):
            if check_pixel_green(hsv, x, y):
                hsv[y, x] = 0


    path_mask = 'Masks/' + filename_image + '_mask' + '.png'
    cv.imwrite(path_mask, hsv)
    winname = 'mask'
    cv.namedWindow(winname)
    cv.moveWindow(winname, 900, 600)
    newsize = (int(width/5), int(height/5))
    mask_green_black_hsv = cv.resize(hsv, newsize)
    cv.imshow(winname, mask_green_black_hsv)
    cv.waitKey()

    #m.getch()
    #cv.destroyAllWindows()
def hsv_filter_direct(filename_image, hsv, height, width, h_green_min, h_green_max, s_green_min, s_green_max, v_green_min, v_green_max):

    for x in range(width):
        for y in range(height):
            if check_pixel_green(hsv, x, y, h_green_min, h_green_max, s_green_min, s_green_max, v_green_min, v_green_max):
                hsv[y, x] = 0

    path_mask = 'Masks/' + filename_image + '_mask' + '.png'
    cv.imwrite(path_mask, hsv)
    winname = 'mask'
    cv.namedWindow(winname)
    cv.moveWindow(winname, 900, 600)
    newsize = (int(width), int(height))
    mask_green_black_hsv = cv.resize(hsv, newsize)
    cv.imshow(winname, mask_green_black_hsv)
    cv.waitKey()


def adding_pixel_values(row_canny_edge_det, row_array_hsv_filter, width):

    new_row_image_matrix = [0] * width

    for pixel_value in range(width):
        if row_array_hsv_filter[pixel_value] == 0 or row_canny_edge_det[pixel_value] == 249:
            new_row_image_matrix[pixel_value] = 249
    new_row_image_matrix = np.array(new_row_image_matrix)
    return new_row_image_matrix


class MergingMasks():

    def __init__(self, img_nr, mask_canny_edge_detection, mask_hsv_filter, height, width):
        self.img_nr = img_nr
        self.mask_canny_edge_detection = mask_canny_edge_detection
        self.mask_hsv_filter = mask_hsv_filter
        self.height = height
        self.width = width
        self.merging_masks()


    def merging_masks(self):
        array_canny_edge_det = np.array(self.mask_canny_edge_detection)
        array_hsv_filter = np.array(self.mask_hsv_filter)
        mask_matrix = np.zeros((self.height, self.width))

        for i in range(self.height):
            new_row = adding_pixel_values(array_canny_edge_det[i], array_hsv_filter[i], self.width)
            mask_matrix[i, :] = new_row

        matrix_to_array = np.squeeze(np.asarray(mask_matrix))
        matrix_to_array = np.reshape(matrix_to_array, (self.height, self.width)).astype(np.uint8)
        final_mask_no_morph = Image.fromarray(matrix_to_array)
        path = "D:/masks/tools_with_hands(allvideos)/merged_masks/hands_with_tools_merged_mask_" + str(self.img_nr) +'.png'
        final_mask_no_morph.save(path)

            # cv.waitKey(0)


def morphological_operation(img_nr, source_path, destination_path):
        mask_to_morph = cv.imread(source_path)

        # Taking a matrix of size 5 as the kernel
        kernel = np.ones((5, 5), np.uint8)

        # The first parameter is the original image,
        # kernel is the matrix with which image is
        # convolved and third parameter is the number
        # of iterations, which will determine how much
        # you want to erode/dilate a given image.
        # img_erosion = cv.erode(img, kernel, iterations=1)
        img_dilation = cv.dilate(mask_to_morph, kernel, iterations=2)

        cv.imwrite(destination_path,
                   img_dilation)

        # cv.imshow('Input', img)
        # cv.imshow('Erosion', img_erosion)


class DbScan():

    def __init__(self, img_nr, path, input_img_with_canny):
        self.img_nr = img_nr
        self.path_to_image = path
        self.input_img_with_canny = input_img_with_canny
        self.dbscan()
    # define dataset
    # X, _ = make_classification(n_samples=1000, n_features=2, n_informative=2, n_redundant=0, n_clusters_per_class=1, random_state=4)
    def dbscan(self):

        img = cv.imread(self.path_to_image)
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        coordinates_of_white_pixels = []
        rows, cols = img.shape[:2]

        for i in range(rows):
            for j in range(cols):
                if img[i, j] == 249:
                    coordinates_of_white_pixels.append([i, j])
        X = np.asarray(coordinates_of_white_pixels)

        # print(coordinates_of_white_pixels)
        # define the model
        # print(X)
        model = DBSCAN(eps=2, min_samples=9)
        # fit model and predict clusters
        yhat = model.fit_predict(X)
        # retrieve unique clusters
        clusters = unique(yhat)

        # create scatter plot for samples from each cluster
        for cluster in clusters:
            # get row indexes for samples with this cluster
            row_ix = where(yhat == cluster)
            # create scatter of these samples
            pyplot.scatter(X[row_ix, 1], X[row_ix, 0])
        # show the plot
        path_cluster = 'D:/masks/hands/cluster_plots/clusterplot_' + str(self.img_nr)
        pyplot.savefig(path_cluster)
        pyplot.clf()

        size_of_biggest_cluster = 0
        index_of_biggest_cluster = 0
        for cluster in clusters:
            row_ix = where(yhat == cluster)
            if row_ix[0].size > size_of_biggest_cluster:

                if max(X[row_ix, 0][0]) == 1079 or max(X[row_ix, 1][0]) == 1919 or min(X[row_ix, 0][0]) == 0 or min(
                        X[row_ix, 1][0]) == 0:
                    continue
                else:
                    size_of_biggest_cluster = row_ix[0].size
                    index_of_biggest_cluster = cluster


        for cluster in clusters:
            if cluster == index_of_biggest_cluster:
                continue

            else:
                row_ix = where(yhat == cluster)
                x_coord_to_delete_mask = X[row_ix, 0]
                y_coord_to_delete_mask = X[row_ix, 1]
                for i in range(len(x_coord_to_delete_mask[0])):
                    img[x_coord_to_delete_mask[0][i], y_coord_to_delete_mask[0][i]] = 0

        if self.input_img_with_canny:
            path = "D:/masks/hands/hsv_canny_dbscan/mask_hsv_canny_dbscan_" + str(self.img_nr) +'.png'
            cv.imwrite(path, img)

        else:
            path = "D:/masks/hands/hsv_dbscan(no_canny)/mask_hsv_dbscan_" + str(
                self.img_nr) + '.png'
            cv.imwrite(path, img)


def fill_hole(mask):
    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    len_contour = len(contours)
    contour_list = []
    for i in range(len_contour):
        drawing = np.zeros_like(mask, np.uint8)  # create a black image
        img_contour = cv.drawContours(drawing, contours, i, (249,249,249), -1)
        contour_list.append(img_contour)

    out = sum(contour_list)
    return out
