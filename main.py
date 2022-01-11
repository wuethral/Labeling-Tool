from tkinter import *
from IPython.display import display, Image
from PIL import Image, ImageTk
from create_mask import mask_creation
from list_of_colors import colors
import os, os.path
import glob
from create_json import CreateJsonPolygonLabels
import cv2
from automated_masking_file import automated_masking
from automated_masking_file_2 import automated_masking_2
from filtering_functions import hsv_filter_direct
from automated_masking import automated_masking
import numpy as np
from sklearn.cluster import DBSCAN

canvas = 0
canvas_2 = 0
label_buttons = []
rectangle_coordinates_one_label = []
select_area_coordinates_one_label = []
big_global_label_dict_rectangle = {}
big_global_label_dict_select_area = {}
image_list = []
hsv_image_list = []
#hsv_image_list_original_size =[]
img_nr = 0
start_x = 0
start_y = 0
first_line = True
green_hsv_pixel_values = []
object_hsv_pixel_values = []
cv2_image_list = []
show_mask_mode = False
w= 0
h=0
mask_list = []
redo_mask_list = False
mask_image_merge_list = []
get_pixel_flag = False
blabla = 0
images = 0


class TKButtonWrapper:
    def __init__(self, root, which_column, callback_arg, callback, counting, nr_of_labels, w, h, color, label_state):
        self.root = root
        self.which_column = which_column
        self.callback_arg = callback_arg
        self.callback = callback
        self.counting = counting
        self.nr_of_labels = nr_of_labels
        self.w = w
        self.h = h
        self.color = color
        self.label_state = label_state
        self.create_button()

    def create_button(self):
        self.button = Button(self.root, text=self.callback_arg, fg = self.color, state=self.label_state,
                             command=lambda: self.callback(self.root, self.callback_arg,
                                                           self.w, self.h, self.color), width=10,
                             height=int(20 / self.nr_of_labels))
        self.button.grid(column=self.which_column, row=self.counting)


def standard_button_callback(root, lab, w, h, color):

    root.bind('r', lambda x: draw_rectangle_outside(root, lab, color))
    root.bind('s', lambda x: area_selection(root, w, h, lab, color))
    root.bind('d', lambda x: clearing_of_label(root, lab))



def toggle_label_buttons(lab):
    global label_buttons
    for button_wrapper in label_buttons:
        if button_wrapper.button['text'] == lab:
            button_wrapper.button['fg'] = 'green'
        else:
            button_wrapper.button['fg'] = 'black'




def draw_rectangle_outside(root, lab, color):
    global canvas
    def draw_rectangle(event):
        if event.state == 8:
            canvas.old_cords = event.x, event.y
        if event.state == 264:
            global rectangle_coordinates_one_label
            x, y = event.x, event.y
            x1, y1 = canvas.old_cords
            canvas.create_rectangle(x1, y1, x, y, outline=color, width = 1,
                                    tags="rect")  # Frage: Spielt Anordnung von x1,y1,x,y eine rolle?

            root.unbind('<ButtonPress-1>')
            root.unbind('<ButtonRelease-1>')

            rectangle_coordinates_one_label = [(x1, y1), (x, y)]
            saving_corner_coordinates('rect', rectangle_coordinates_one_label, lab)

    root.bind('<ButtonPress-1>', draw_rectangle)
    root.bind("<ButtonRelease-1>", draw_rectangle)


def area_selection(root, w, h, lab, color):
    global canvas
    def start_line(event):
        global select_area_coordinates_one_label
        global start_x
        global start_y
        select_area_coordinates_one_label = []
        canvas.old_cords = event.x, event.y
        root.unbind('<ButtonPress-1>')
        start_x = event.x
        start_y = event.y
        select_area_coordinates_one_label.append((start_x, start_y))

    def mouse_move(event):
        canvas.delete('line')
        x_live, y_live = canvas.old_cords
        canvas.create_line(x_live, y_live, event.x, event.y, width=1, fill=color, tags='line')


    def draw_line(event):

        global first_line
        x, y = event.x, event.y
        x1, y1 = canvas.old_cords
        end_x = x
        end_y = y
        distance_end_start = (((end_y - start_y) ** 2) + ((end_x - start_x) ** 2)) ** (1 / 2)

        if distance_end_start < 5 and first_line == False:
            canvas.create_line(x1, y1, x, y, width=1, fill=color)
            canvas.create_line(end_x, end_y, start_x, start_y, width=1,
                               fill=color)  # Frage: Spielt Anordnung von x1,y1,x,y eine rolle?
            root.unbind('<ButtonRelease-1>')
            root.unbind("<B1-Motion>")
            select_area_coordinates_one_label.append((end_x, end_y))

            saving_corner_coordinates('sel_area', select_area_coordinates_one_label, lab)

        else:
            canvas.create_line(x1, y1, x, y, width=1, fill=color)  # Frage: Spielt Anordnung von x1,y1,x,y eine rolle?
            canvas.old_cords = x, y
            first_line = False
            select_area_coordinates_one_label.append((x, y))

    root.bind('<ButtonPress-1>', start_line)
    root.bind("<B1-Motion>", mouse_move)
    root.bind('<ButtonRelease-1>', draw_line)


def saving_corner_coordinates(modus, coordinates, lab):
    global big_global_label_dict_rectangle
    global big_global_label_dict_select_area
    if modus == 'rect':
        if not img_nr in big_global_label_dict_rectangle.keys():
            big_global_label_dict_rectangle[img_nr] = {}
            big_global_label_dict_rectangle[img_nr][lab] = [coordinates]
        elif img_nr in big_global_label_dict_rectangle.keys():
            if not lab in big_global_label_dict_rectangle[img_nr].keys():
                big_global_label_dict_rectangle[img_nr][lab] = [coordinates]
            elif lab in big_global_label_dict_rectangle[img_nr].keys():
                big_global_label_dict_rectangle[img_nr][lab].append(coordinates)
    elif modus == 'sel_area':
        if not img_nr in big_global_label_dict_select_area.keys():

            big_global_label_dict_select_area[img_nr] = {}
            big_global_label_dict_select_area[img_nr][lab] = [coordinates]
        elif img_nr in big_global_label_dict_select_area.keys():

            if not lab in big_global_label_dict_select_area[img_nr].keys():
                big_global_label_dict_select_area[img_nr][lab] = [
                    coordinates]
            elif lab in big_global_label_dict_select_area[img_nr].keys():
                big_global_label_dict_select_area[img_nr][lab].append(
                    coordinates)

def clearing_of_label(root, lab):
    global canvas


    if img_nr in big_global_label_dict_rectangle:
        current_page_rectangle = big_global_label_dict_rectangle[img_nr]
        if lab in current_page_rectangle:
            del big_global_label_dict_rectangle[img_nr][lab]
        else:
            pass
    else:
        pass

    if img_nr in big_global_label_dict_select_area:
        current_page_select_area = big_global_label_dict_select_area[img_nr]
        if lab in current_page_select_area:
            del big_global_label_dict_select_area[img_nr][lab]
        else:
            pass
    else:
        pass

    displaying_current_image()


def displaying_current_image():

    global image_list
    global mask_list
    global mask_image_merge_list
    global canvas
    global label_buttons
    global canvas_2
    global canvas_3
    global redo_mask_list
    global images
    global img_nr
    current_color = 0
    print('len:', len(image_list))
    #canvas = Canvas(sub_root, width=int(w), height=int(h))
    #canvas.grid(column=0, row=0, rowspan=15)
    print('rml',redo_mask_list)

    print('img_nr_in_disp:', img_nr)
    if redo_mask_list:
        images = os.listdir('images')
        print('img',images)
        mask_names = os.listdir('bounding_boxes')
        mask_merge_names = os.listdir('image_mask_merge')
        mask_list = []
        mask_image_merge_list = []
        image_list = []

        for mask_name in mask_names:
            mask_path = 'bounding_boxes/' + mask_name
            mask = Image.open(mask_path)
            h = int(mask.height)
            w = int(mask.width)
            w = 760
            h = 428
            mask = ImageTk.PhotoImage(mask.resize((int(0.8 * w), int(0.8 * h))))
            mask_list.append(mask)

        for mask_merge_name in mask_merge_names:
            mask_merge_path = 'image_mask_merge/' + mask_merge_name
            mask_merge = Image.open(mask_merge_path)

            w = 760
            h = 428
            mask_merge = ImageTk.PhotoImage(mask_merge.resize((int(0.8 * w), int(0.8 * h))))
            mask_image_merge_list.append(mask_merge)

        rspan = 15  # rowspan of image
        path = 'images'
        images = os.listdir(path)
        for f in images:
            imagePath = os.path.join(path, f)
            if imagePath != path + '\\.DS_Store':
                picture = Image.open(imagePath)
                h = int(picture.height)
                w = int(picture.width)
                w = 760
                h= 428
                img = ImageTk.PhotoImage(picture.resize((w, h)))
                image_list.append(img)

    redo_mask_list = False

    canvas.create_image(0, 0, anchor=NW, image=image_list[img_nr])
    canvas_2.create_image(0, 0, anchor=NW, image=mask_list[img_nr])
    canvas_3.create_image(0, 0, anchor=NW, image=mask_image_merge_list[img_nr])

    if img_nr in big_global_label_dict_rectangle.keys():
        for rect_labels in big_global_label_dict_rectangle[img_nr].keys():
            for button_wrapper in label_buttons:
                if button_wrapper.button['text'] == rect_labels:
                    current_color = button_wrapper.button['fg']
            for rect_coordinates in range(len(big_global_label_dict_rectangle[img_nr][rect_labels])):
                x_one = big_global_label_dict_rectangle[img_nr][rect_labels][rect_coordinates][0][0]
                y_one = big_global_label_dict_rectangle[img_nr][rect_labels][rect_coordinates][0][1]
                x_two = big_global_label_dict_rectangle[img_nr][rect_labels][rect_coordinates][1][0]
                y_two = big_global_label_dict_rectangle[img_nr][rect_labels][rect_coordinates][1][1]
                canvas.create_rectangle(x_one, y_one, x_two, y_two, width = 1, outline=current_color)

    if img_nr in big_global_label_dict_select_area.keys():
        for select_area_labels in big_global_label_dict_select_area[img_nr].keys():
            for button_wrapper in label_buttons:
                if button_wrapper.button['text'] == select_area_labels:
                    current_color = button_wrapper.button['fg']
            for area_corner_coords in range(len(big_global_label_dict_select_area[img_nr][select_area_labels])):

                for i in range(len(
                        big_global_label_dict_select_area[img_nr][select_area_labels][area_corner_coords]) - 1):
                    corner1 = big_global_label_dict_select_area[img_nr][select_area_labels][area_corner_coords][i]
                    corner2 = big_global_label_dict_select_area[img_nr][select_area_labels][area_corner_coords][
                        i + 1]
                    canvas.create_line(corner1, corner2, width=1, fill=current_color)
                first_corner = big_global_label_dict_select_area[img_nr][select_area_labels][area_corner_coords][
                    0]
                last_corner = big_global_label_dict_select_area[img_nr][select_area_labels][area_corner_coords][
                    -1]
                canvas.create_line(last_corner, first_corner, width=1, fill=current_color)
    if get_pixel_flag == False and blabla == 1:
        stop_get_pixels()
    print('')


def next_image(root, sub_root, labels_we_want, w, h):
    global img_nr
    global label_buttons
    global get_pixel_flag
    global image_list
    get_pixel_flag = False
    img_nr += 1


    print('img_n',img_nr)
    print(len(image_list))


    if img_nr == (len(image_list) - 1):
        # button_next_image = Button(root, text='>>', state=DISABLED,
        #                           command=lambda: next_image(root, image_list, img_nr, w, h))
        # button_next_image.grid(column=2, row=8)
        root.unbind("<Right>")
    else:
        # button_next_image = Button(root, text='>>', command=lambda: next_image(root, image_list, img_nr, w, h))
        # button_next_image.grid(column=2, row=8)
        root.bind("<Right>", lambda x: next_image(root, sub_root, labels_we_want, w, h))

    if img_nr == 0:
        # button_last_image = Button(root, text='<<', state=DISABLED,
        #                           command=lambda: last_image(root, image_list, img_nr, w, h))
        # button_last_image.grid(column=1, row=8)
        root.unbind("<Left>")
    else:
        # button_last_image = Button(root, text='<<', command=lambda: last_image(root, image_list, img_nr, w, h))
        # button_last_image.grid(column=1, row=8)
        root.bind("<Left>", lambda x: last_image(root, sub_root, labels_we_want, w, h))

    #labeling_image_page = 'Image ' + str(img_nr) + '/' + str(len(image_list) - 1)
    #image_nr = Label(sub_root, text=labeling_image_page)
    #image_nr.grid(column=4, row=10)

    displaying_current_image()

def last_image(root, sub_root, labels_we_want, w, h):
    global img_nr
    global get_pixel_flag
    global image_list
    get_pixel_flag = False
    img_nr -= 1
    if img_nr == -1:
        img_nr = 0
    print('img_nr',img_nr)
    print(len(image_list))

    if img_nr == (len(image_list) - 1):
        # button_next_image = Button(root, text='>>', state=DISABLED,
        #                           command=lambda: next_image(root, image_list, img_nr, w, h))
        # button_next_image.grid(column=2, row=8)
        root.unbind("<Right>")
    else:
        # button_next_image = Button(root, text='>>', command=lambda: next_image(root, image_list, img_nr, w, h))
        # button_next_image.grid(column=2, row=8)
        root.bind("<Right>", lambda x: next_image(root, sub_root, labels_we_want, w, h))

    if img_nr == 0:
        # button_last_image = Button(root, text='<<', state=DISABLED,
        #                           command=lambda: last_image(root, image_list, img_nr, w, h))
        # button_last_image.grid(column=1, row=8)
        root.unbind("<Left>")
    else:
        # button_last_image = Button(root, text='<<', command=lambda: last_image(root, image_list, img_nr, w, h))
        # button_last_image.grid(column=1, row=8)
        root.bind("<Left>", lambda x: last_image(root, sub_root, labels_we_want, w, h))

    displaying_current_image()




def read_hsv(root, green_or_object, image_nr):
    this_hsv_img = hsv_image_list[img_nr]

    def save_pixels(event):
        x, y = event.x, event.y
        height = this_hsv_img.shape[0]
        width = this_hsv_img.shape[1]
        #print(width, height)
        #print(x,y)
        if x < width or y < height:
            pixel = this_hsv_img[y][x]
            #print(pixel)
            if green_or_object == 'green':
                green_hsv_pixel_values.append(pixel)
            elif green_or_object == 'object':
                object_hsv_pixel_values.append(pixel)

    def show_mask(event):
        if len(green_hsv_pixel_values) != 0:
            automated_masking_2(green_hsv_pixel_values)

    root.bind("<B1-Motion>", save_pixels)
    root.bind('<ButtonRelease-1>', show_mask)

def print_hsv_values():
    print('green_screen_hsv:', green_hsv_pixel_values)
    print('object_hsv:', object_hsv_pixel_values)

def show_masks_mode():
    show_mask_mode = True

def mask_over_image(image_name, path):
    image_path = path + '/' + image_name
    mask_path = 'bounding_boxes/' + image_name
    image = cv2.imread(image_path)
    mask = cv2.imread(mask_path)
    background = cv2.imread('black.png')
    background = cv2.resize(background, (760, 428))
    overlay = np.where(mask == 0, background, image)

    overlay_path = 'mask_over_image/' + image_name
    cv2.imwrite(overlay_path, overlay)
    winname2 = 'mask_over_image'
    cv2.namedWindow(winname2)
    cv2.moveWindow(winname2, 800, 500)
    cv2.imshow(winname2, overlay)
    cv2.waitKey()
    cv2.destroyWindow(winname2)




def erosion(x, w, h):

    image_name = images[img_nr]
    mask_path = 'bounding_boxes/' + image_name
    mask = cv2.imread(mask_path)
    kernel = np.ones((x, x), np.uint8)
    img_erosion = cv2.erode(mask, kernel, iterations=1)
    os.remove(mask_path)
    cv2.imwrite(mask_path, img_erosion)

    mask = Image.open(mask_path)
    mask = ImageTk.PhotoImage(mask.resize((int(0.8*w), int(0.8*h))))
    mask_list[img_nr] = mask

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
    mask_image_merge_list[img_nr] = pillow_mask_image_merge


    displaying_current_image()
    #winname = 'mask'
    #cv2.namedWindow(winname)
    #cv2.moveWindow(winname, 800, 0)
    #cv2.imshow(winname, img_erosion)
    #mask_over_image(image_name, path)
    #cv2.waitKey()
    #cv2.destroyWindow(winname)


def dilation(x, w, h):
    image_name = images[img_nr]
    mask_path = 'bounding_boxes/' + image_name
    mask = cv2.imread(mask_path)
    kernel = np.ones((x, x), np.uint8)
    img_dilation = cv2.dilate(mask, kernel, iterations=1)
    os.remove(mask_path)
    cv2.imwrite(mask_path, img_dilation)
    mask = Image.open(mask_path)
    mask = ImageTk.PhotoImage(mask.resize((int(0.8*w), int(0.8*h))))
    mask_list[img_nr] = mask


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
    mask_image_merge_list[img_nr] = pillow_mask_image_merge

    displaying_current_image()
    #winname = 'mask'
    #cv2.namedWindow(winname)
    #cv2.moveWindow(winname, 800, 0)
    #cv2.imshow(winname, img_dilation)
    #mask_over_image(image_name, path)
    #cv2.waitKey()
    #cv2.destroyWindow(winname)

def show_masks(root, image, width, height, path):
    root.bind('e3', lambda x: erosion(3, image, width, height, path))
    root.bind('d3', lambda x: dilation(3, image, width, height, path))
    root.bind('e5', lambda x: erosion(5, image, width, height, path))
    root.bind('d5', lambda x: dilation(5, image, width, height, path))
    root.bind('e7', lambda x: erosion(7, image, width, height, path))
    root.bind('d7', lambda x: dilation(7, image, width, height, path))
    root.bind('e9', lambda x: erosion(7, image, width, height, path))
    root.bind('d9', lambda x: dilation(7, image, width, height, path))

    mask_path = 'bounding_boxes/' + image
    mask = cv2.imread(mask_path)
    #mask = cv2.resize(mask, (int(width*3/4), int(height*3/4)))
    winname = 'mask'
    cv2.namedWindow(winname)
    cv2.moveWindow(winname, 800, 0)
    cv2.imshow(winname, mask)
    mask_over_image(image, path)
    cv2.waitKey()
    cv2.destroyWindow(winname)

def delete_image(black):
    global redo_mask_list
    global img_nr
    image_name = images[img_nr]
    print('del img:',image_name)
    #print(type(img_nr))
    image_list.remove(image_list[img_nr])
    mask_list.remove(mask_list[img_nr])
    mask_image_merge_list.remove(mask_image_merge_list[img_nr])
    image_path = 'images/' + image_name
    path_mask = 'bounding_boxes/' + image_name
    path_mask_img_merge = 'image_mask_merge/' + image_name
    os.remove(path_mask)
    os.remove(image_path)
    os.remove(path_mask_img_merge)
    redo_mask_list = True
    if img_nr != 0:
        img_nr -= 1
    displaying_current_image()

def keep_image(img_nr, image_name, black):
    image_list.remove(image_list[img_nr])
    mask_list.remove(mask_list[img_nr])
    displaying_current_image()

def restore():
    global redo_mask_list
    image_name = images[img_nr]
    old_mask_path = 'bounding_boxes/' + image_name
    new_mask_path = 'bounding_boxes_copy/' + image_name
    old_mask_image_merge_path = 'image_mask_merge/' + image_name
    new_mask_image_merge_path = 'image_mask_merge_copy/' + image_name
    new_mask = cv2.imread(new_mask_path)
    os.remove(old_mask_path)
    new_image_merge = cv2.imread(new_mask_image_merge_path)
    os.remove(old_mask_image_merge_path)
    cv2.imwrite(old_mask_path, new_mask)
    cv2.imwrite(old_mask_image_merge_path, new_image_merge)
    mask = Image.open(old_mask_path)
    mask = ImageTk.PhotoImage(mask.resize((int(0.8*w), int(0.8*h))))
    mask_image_merge = Image.open(old_mask_image_merge_path)
    mask_image_merge = ImageTk.PhotoImage(mask_image_merge.resize((int(0.8*w), int(0.8*h))))
    mask_list[img_nr] = mask
    mask_image_merge_list[img_nr] = mask_image_merge
    redo_mask_list = True
    displaying_current_image()

def get_pixel():

    global get_pixel_flag
    get_pixel_flag = True

    def get_pixel_value(event):
        coordinates = event.x, event.y
        pixel_value = current_mask[coordinates[1]][coordinates[0]][0]
        display_text = 'Mask Pixel Value: ' + str(pixel_value)
        canvas.create_text(5, 0, anchor = NW, fill="darkblue",
                            text=display_text, font = 'Times 16')

    def stop_get_pixel_value(event):
        displaying_current_image()

    current_mask_path = 'bounding_boxes/' + images[img_nr]
    current_mask = cv2.imread(current_mask_path)
    root.bind("<ButtonPress-1>", get_pixel_value)
    root.bind("<ButtonRelease-1>", stop_get_pixel_value)

def stop_get_pixels():
    global get_pixel_flag
    global blabla

    blabla = 1
    get_pixel_flag = False

    root.unbind("<ButtonPress-1>")
    root.unbing("<ButtonRelease-1>")

def mask_update():
    global images
    global big_global_label_dict_select_area
    global redo_mask_list
    mask_creation(w, h, 10, list_of_labels, big_global_label_dict_select_area, images)
    big_global_label_dict_select_area = {}
    redo_mask_list = True
    displaying_current_image()

def make_blank():
    global images
    mask_path = 'bounding_boxes/' + images[img_nr]
    mask_merge_path = 'image_mask_merge/' + images[img_nr]
    os.remove(mask_path)
    os.remove(mask_merge_path)
    black = cv2.imread('black.png')
    black = cv2.resize(black, (760,428))
    cv2.imwrite(mask_path, black)
    cv2.imwrite(mask_merge_path, black)
    displaying_current_image()

def dbscan():
    mask_path = 'bounding_boxes/' + images[img_nr]
    mask = cv2.imread(mask_path)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    coordinates_of_white_pixels = []
    rows, cols = mask.shape[:2]

    for i in range(rows):
        for j in range(cols):
            if mask[i, j] == 251:
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
    mask_list[img_nr] = mask_pillow
    black = cv2.imread('black.png')
    black = cv2.resize(black, (760, 428))
    image_path = 'images/' + images[img_nr]
    image = cv2.imread(image_path)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    image_merge = np.where(mask == 0, black, image)
    mask_image_merge_path = 'image_mask_merge/' + images[img_nr]
    os.remove(mask_image_merge_path)
    cv2.imwrite(mask_image_merge_path, image_merge)
    mask_merge_pillow = Image.open(mask_image_merge_path)
    mask_merge_pillow = ImageTk.PhotoImage(mask_merge_pillow.resize((int(0.8 * w), int(0.8 * h))))
    mask_image_merge_list[img_nr] = mask_merge_pillow

    displaying_current_image()


def button_control(status, root, standard_button_callback, list_of_labels, w, h, colors):
    count = 1
    label_title = Label(root, text='Labels:')
    label_title.grid(column=10, row=0)


    if status == 'normal':
        label_state = 'disabled'

    else:
        label_state = 'normal'

    for label in list_of_labels:
        label_buttons.append(TKButtonWrapper(root, 10, label, standard_button_callback, count, len(list_of_labels), w, h, colors[count], label_state))
        count += 1

    button_height = int(20 / len(list_of_labels))

    hand_labeling_button = Button(root, state = status, text='Start Hand Labeling', width=20, height=button_height,
                                  command=lambda: button_control('disabled', root, standard_button_callback, list_of_labels, w, h, colors))
    hand_labeling_button.grid(column=12, row=0)

    stop_hand_labeling_button = Button(root,state = 'normal', text='Stop Hand Labeling', width=20, height=button_height,
                                       command=lambda: button_control('normal', root, standard_button_callback, list_of_labels, w, h, colors))
    stop_hand_labeling_button.grid(column=12, row=1)

    create_mask_button = Button(root,state = status, text='Create Mask', width=20, height=button_height,
                                command=lambda: mask_update())
    create_mask_button.grid(column=12, row=2)

    #json_creator = CreateJsonPolygonLabels(big_global_label_dict_select_area, list_of_labels)
    #create_json_file = Button(root, state = status,text='Create Json', width=20, height=button_height,
    #                          command=lambda: json_creator.createjson())
    #create_json_file.grid(column=12, row=1)

    #automated_masking_button = Button(root, state = status,text='Automated Masking', width=20, height=button_height,
    #                                  command=lambda: automated_masking())
    #automated_masking_button.grid(column=12, row=2)

    #show_masks_button = Button(root, state = status,text='Finetune masks', width=20, height=button_height,
    #                           command=lambda: show_masks(root, w, h, path))
    #show_masks_button.grid(column=12, row=3)

    restore_button = Button(root, state = status,text='Restore Image', width=20, height=button_height,
                            command=lambda: restore())
    restore_button.grid(column=13, row=2)

    erosion_kernel_3_mal_3_Button = Button(root,state = status, text='Errosion 3x3', width=20, height=button_height,
                                           command=lambda: erosion(3, w, h))
    erosion_kernel_3_mal_3_Button.grid(column=12, row=4)

    erosion_kernel_5_mal_5_Button = Button(root,state = status, text='Errosion 5x5', width=20, height=button_height,
                                           command=lambda: erosion(5, w, h))
    erosion_kernel_5_mal_5_Button.grid(column=12, row=5)

    erosion_kernel_7_mal_7_Button = Button(root,state = status, text='Errosion 7x7', width=20, height=button_height,
                                           command=lambda: erosion(7, w, h))
    erosion_kernel_7_mal_7_Button.grid(column=12, row=6)

    erosion_kernel_9_mal_9_Button = Button(root,state = status, text='Errosion 9x9', width=20, height=button_height,
                                           command=lambda: erosion(9, w, h))
    erosion_kernel_9_mal_9_Button.grid(column=12, row=7)

    dilation_kernel_3_mal_3_Button = Button(root,state = status, text='Dilation 3x3', width=20, height=button_height,
                                            command=lambda: dilation(3, w, h))
    dilation_kernel_3_mal_3_Button.grid(column=13, row=4)

    dilation_kernel_5_mal_5_Button = Button(root, state = status,text='Dilation 5x5', width=20, height=button_height,
                                            command=lambda: dilation(5, w, h))
    dilation_kernel_5_mal_5_Button.grid(column=13, row=5)

    dilation_kernel_7_mal_7_Button = Button(root,state = status, text='Dilation 7x7', width=20, height=button_height,
                                            command=lambda: dilation(7, w, h))
    dilation_kernel_7_mal_7_Button.grid(column=13, row=6)

    dilation_kernel_9_mal_9_Button = Button(root, state = status,text='Dilation 9x9', width=20, height=button_height,
                                            command=lambda: dilation(9, w, h))
    dilation_kernel_9_mal_9_Button.grid(column=13, row=7)

    delete_image_Button = Button(root,state = status, text='Delete', width=20, height=button_height,
                                 command=lambda: delete_image(black))
    delete_image_Button.grid(column=12, row=3)

    #keep_image_Button = Button(root,state = status, text='Keep', width=20, height=button_height,
    #                           command=lambda: keep_image(img_nr, black))
    #keep_image_Button.grid(column=13, row=4)

    get_pixels_button = Button(root,state = status, text='Get Pixel Value', width=20, height=button_height,
                               command=lambda: get_pixel())
    get_pixels_button.grid(column=13, row=0)

    stop_get_pixels_button = Button(root, state = status, text = 'Stop Get PV', width = 20, height = button_height, command=lambda: stop_get_pixels())
    stop_get_pixels_button.grid(column=13, row=1)

    make_blank_button = Button(root, state = status, text = 'Make blank', width = 20, height = button_height, command=lambda: make_blank())
    make_blank_button.grid(column=13, row=3)

    dbscan_button = Button(root, state = status, text = 'dbscan', width = 20, height = button_height, command = lambda: dbscan())
    dbscan_button.grid(column = 12, row = 8)


if __name__ == '__main__':

    # Defining the tkinter root
    root = Tk()
    # Defining the gemotery of the root (with*height+coordinate of upper left corner)
    root.geometry('1400x1300+0+0')
    # Reading the images into a list
    mask_names = os.listdir('bounding_boxes')

    h = 428
    w = 760

    rspan = 15  # rowspan of image
    path = 'images'
    images = os.listdir(path)
    for f in images:
        imagePath = os.path.join(path, f)
        if imagePath != path + '\\.DS_Store':
            picture = Image.open(imagePath)
            img = ImageTk.PhotoImage(picture.resize((w, h)))
            image_list.append(img)
            cv2_image = cv2.imread(imagePath)
            cv2_image_list.append(cv2_image)
            cv2_image = cv2.resize(cv2_image, (w,h))
            hsv_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2HSV)
            hsv_image_list.append(hsv_image)
    '''
    if len(mask_names) == 0:

        automated_masking()
        black = Image.open('black.png')
        black = ImageTk.PhotoImage(black.resize((int(0.8*w), int(0.8*h))))
        for mask_name in mask_names:
            mask_path = 'bounding_boxes/' + mask_name
            mask = Image.open(mask_path)
            h = int(mask.height)
            h = 428
            w = int(mask.width)
            w = 760
            mask = ImageTk.PhotoImage(mask.resize((int(0.8*w), int(0.8*h))))
            mask_list.append(mask)
            image_path = 'images/' + mask_name
            image = Image.open(image_path)
            image = ImageTk.PhotoImage(image.resize((int(0.8*w), int(0.8*h))))
            mask_image_merge = np.where(mask==0, black, image)
            mask_image_merge_list.append(mask_image_merge)
    '''
    if len(mask_names) == 0:
        automated_masking()


    black = Image.open('black.png')
    black = ImageTk.PhotoImage(black.resize((int(0.8 * w), int(0.8 * h))))
    for mask_name in mask_names:
        mask_path = 'bounding_boxes/' + mask_name
        mask = Image.open(mask_path)
        h = int(mask.height)
        h = 428
        w = int(mask.width)
        w = 760
        mask = ImageTk.PhotoImage(mask.resize((int(0.8*w), int(0.8*h))))
        mask_list.append(mask)
        image_path = 'images/' + mask_name
        #image = Image.open(image_path)
        #image = ImageTk.PhotoImage(image.resize((int(0.8*w), int(0.8*h))))
        image = cv2.imread(image_path)
        image = cv2.resize(image, (int(0.8*w), int(0.8*h)))
        black = cv2.imread('black.png')
        black = cv2.resize(black, (int(0.8 * w), int(0.8 * h)))
        mask = cv2.imread(mask_path)
        mask = cv2.resize(mask, (int(0.8 * w), int(0.8 * h)))
        mask_image_merge = np.where(mask==0, black, image)
        mask_image_merge_path = 'image_mask_merge/' + mask_name
        mask_image_merge_path_copy = 'image_mask_merge_copy/' + mask_name
        cv2.imwrite(mask_image_merge_path, mask_image_merge)
        cv2.imwrite(mask_image_merge_path_copy, mask_image_merge)
        mask_image_merge = Image.open(mask_image_merge_path)
        mask_image_merge = ImageTk.PhotoImage(mask_image_merge.resize((int(0.8*w), int(0.8*h))))
        mask_image_merge_list.append(mask_image_merge)



    black = Image.open('black.png')
    h = int(picture.height)
    w = int(picture.width)
    h = 428
    w = 760

    black = ImageTk.PhotoImage(black.resize((w, h)))
    list_of_labels = ['249', '250', '251', '248', '253', '254', '255']


    sub_root = Frame(root)
    sub_root.grid(column = 0, row = 0, rowspan = rspan, columnspan = 10)
    canvas = Canvas(sub_root, width=w, height=h)
    canvas.grid(column=0, row=0, rowspan=15)
    canvas.create_image(0, 0, anchor=NW, image=image_list[0])
    labeling_image_page = 'Image ' + str(img_nr) + '/' + str(len(image_list) - 1)
    image_nr = Label(sub_root, text=labeling_image_page)
    #image_nr.grid(column=16, row=10)

    if len(os.listdir('bounding_boxes')) != 0:
        mask_path = 'bounding_boxes/' + images[img_nr]
        mask = Image.open(mask_path)

    else:
        mask = Image.open('black.png')

    mask = ImageTk.PhotoImage(mask.resize((int(w*0.8), int(h*0.8))))

    sub_root_2 = Frame(root)
    sub_root_2.grid(column = 0, row = h, rowspan = int(rspan/2), columnspan = 8)
    canvas_2 = Canvas(sub_root_2, width = int(w*0.8), height = int(h*0.8))
    canvas_2.grid(column=0, row=0)
    canvas_2.create_image(0, 0, anchor=NW, image=mask)


    sub_root_3 = Frame(root)
    sub_root_3.grid(column = 9, row = h, rowspan = int(rspan/2), columnspan = 8)
    canvas_3 = Canvas(sub_root_3, width = int(w*0.8), height = int(h*0.8))
    canvas_3.grid(column=0, row=0, rowspan = 15)
    canvas_3.create_image(0, 0, anchor=NW, image=mask_image_merge_list[0])

    root.bind("<Right>", lambda x: next_image(root, sub_root, list_of_labels, w, h))
    #root.bind("<Left>", lambda x: last_image(root, sub_root, image_list, list_of_labels, w, h))

    button_control('normal', root, standard_button_callback, list_of_labels, w, h, colors)







    mainloop()

