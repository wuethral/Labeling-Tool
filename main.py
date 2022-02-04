import tkinter as tk
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
from tkinter import messagebox
from create_lists import CreateImageList


canvas = 0
canvas_2 = 0
label_buttons = []
rectangle_coordinates_one_label = []
select_area_coordinates_one_label = []
big_global_label_dict_rectangle = {}
big_global_label_dict_select_area = {}
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
canvas_2_image = 0
canvas_3_image = 0

class TKButtonWrapper:
    def __init__(self, root, which_column, callback_arg, callback, counting, nr_of_labels, w, h, color, label_state, all_canvas):
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
        self.all_canvas = all_canvas
        self.create_button()

    def create_button(self):
        self.button = tk.Button(self.root, text=self.callback_arg, fg = self.color, state=self.label_state,
                             command=lambda: self.callback(self.root, self.callback_arg,
                                                           self.w, self.h, self.color, self.all_canvas), width=10,
                             height=int(20 / self.nr_of_labels))
        self.button.grid(column=self.which_column, row=self.counting)


def standard_button_callback(root, lab, w, h, color, all_canvas):

    root.bind('r', lambda x: draw_rectangle_outside(root, lab, color))
    root.bind('s', lambda x: area_selection(root, w, h, lab, color, all_canvas))
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


def area_selection(root, w, h, lab, color, all_canvas):
    global canvas
    def start_line(event):
        global select_area_coordinates_one_label
        global start_x
        global start_y
        select_area_coordinates_one_label = []
        all_canvas.canvas.old_cords = event.x, event.y
        root.unbind('<ButtonPress-1>')
        start_x = event.x
        start_y = event.y
        select_area_coordinates_one_label.append((start_x, start_y))

    def mouse_move(event):
        all_canvas.canvas.delete('line')
        x_live, y_live = all_canvas.canvas.old_cords
        all_canvas.canvas.create_line(x_live, y_live, event.x, event.y, width=1, fill=color, tags='line')


    def draw_line(event):

        global first_line
        x, y = event.x, event.y
        x1, y1 = all_canvas.canvas.old_cords
        end_x = x
        end_y = y
        distance_end_start = (((end_y - start_y) ** 2) + ((end_x - start_x) ** 2)) ** (1 / 2)

        if distance_end_start < 5 and first_line == False:
            all_canvas.canvas.create_line(x1, y1, x, y, width=1, fill=color)
            all_canvas.canvas.create_line(end_x, end_y, start_x, start_y, width=1,
                               fill=color)  # Frage: Spielt Anordnung von x1,y1,x,y eine rolle?
            root.unbind('<ButtonRelease-1>')
            root.unbind("<B1-Motion>")
            select_area_coordinates_one_label.append((end_x, end_y))

            saving_corner_coordinates('sel_area', select_area_coordinates_one_label, lab)

        else:
            all_canvas.canvas.create_line(x1, y1, x, y, width=1, fill=color)  # Frage: Spielt Anordnung von x1,y1,x,y eine rolle?
            all_canvas.canvas.old_cords = x, y
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


def displaying_current_image(lists, all_canvas):
    global mask_image_merge_list
    global canvas
    global label_buttons
    global canvas_2
    global canvas_3
    global redo_mask_list
    global images
    global img_nr
    global root
    current_color = 0
    print('update', img_nr)

    if redo_mask_list:

        path = 'images'
        images = os.listdir(path)
        w = 760
        h = 428

        del lists
        lists = CreateImageList(path, images, w, h)

    AllCanvas.update_canvas(all_canvas, lists)
    AllCanvas.draw_forms(all_canvas)


    redo_mask_list = False



def next_image(root, labels_we_want, w, h, lists, all_canvas):
    global img_nr
    global label_buttons
    global get_pixel_flag
    get_pixel_flag = False
    img_nr += 1



    if img_nr == (lists.length - 1):
        # button_next_image = Button(root, text='>>', state=DISABLED,
        #                           command=lambda: next_image(root, image_list, img_nr, w, h))
        # button_next_image.grid(column=2, row=8)
        root.unbind("<Right>")
    else:
        # button_next_image = Button(root, text='>>', command=lambda: next_image(root, image_list, img_nr, w, h))
        # button_next_image.grid(column=2, row=8)
        root.bind("<Right>", lambda x: next_image(root, labels_we_want, w, h, lists, all_canvas))

    if img_nr == 0:
        # button_last_image = Button(root, text='<<', state=DISABLED,
        #                           command=lambda: last_image(root, image_list, img_nr, w, h))
        # button_last_image.grid(column=1, row=8)
        root.unbind("<Left>")
    else:
        # button_last_image = Button(root, text='<<', command=lambda: last_image(root, image_list, img_nr, w, h))
        # button_last_image.grid(column=1, row=8)
        root.bind("<Left>", lambda x: last_image(root, labels_we_want, w, h, lists, all_canvas))

    #labeling_image_page = 'Image ' + str(img_nr) + '/' + str(len(image_list) - 1)
    #image_nr = Label(sub_root, text=labeling_image_page)
    #image_nr.grid(column=4, row=10)

    displaying_current_image(lists, all_canvas)

def last_image(root, labels_we_want, w, h, image_list, all_canvas):
    global img_nr
    global get_pixel_flag
    get_pixel_flag = False
    img_nr -= 1
    if img_nr == -1:
        img_nr = 0
    print('img_nr',img_nr)

    if img_nr == (image_list.length - 1):
        # button_next_image = Button(root, text='>>', state=DISABLED,
        #                           command=lambda: next_image(root, image_list, img_nr, w, h))
        # button_next_image.grid(column=2, row=8)
        root.unbind("<Right>")
    else:
        # button_next_image = Button(root, text='>>', command=lambda: next_image(root, image_list, img_nr, w, h))
        # button_next_image.grid(column=2, row=8)
        root.bind("<Right>", lambda x: next_image(root, labels_we_want, w, h, image_list, all_canvas))

    if img_nr == 0:
        # button_last_image = Button(root, text='<<', state=DISABLED,
        #                           command=lambda: last_image(root, image_list, img_nr, w, h))
        # button_last_image.grid(column=1, row=8)
        root.unbind("<Left>")
    else:
        # button_last_image = Button(root, text='<<', command=lambda: last_image(root, image_list, img_nr, w, h))
        # button_last_image.grid(column=1, row=8)
        root.bind("<Left>", lambda x: last_image(root, labels_we_want, w, h, image_list, all_canvas))

    displaying_current_image(image_list, all_canvas)




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

def mask_update(w, h, list_of_labels, lists,all_canvas):
    global images
    global big_global_label_dict_select_area
    global redo_mask_list
    print(w, h)
    mask_creation(w, h, 10, list_of_labels, big_global_label_dict_select_area, images)
    big_global_label_dict_select_area = {}
    redo_mask_list = True
    displaying_current_image(lists, all_canvas)

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


def button_control(status, root, standard_button_callback, list_of_labels, w, h, colors, lists, all_canvas):
    count = 1
    label_title = tk.Label(root, text='Labels:')
    label_title.grid(column=10, row=0)


    if status == 'normal':
        label_state = 'disabled'

    else:
        label_state = 'normal'

    for label in list_of_labels:
        label_buttons.append(TKButtonWrapper(root, 10, label, standard_button_callback, count, len(list_of_labels), w, h, colors[count], label_state, all_canvas))
        count += 1

    button_height = int(20 / len(list_of_labels))

    hand_labeling_button = tk.Button(root, state = status, text='Start Hand Labeling', width=20, height=button_height,
                                  command=lambda: button_control('disabled', root, standard_button_callback, list_of_labels, w, h, colors, lists, all_canvas))
    hand_labeling_button.grid(column=12, row=0)

    stop_hand_labeling_button = tk.Button(root,state = 'normal', text='Stop Hand Labeling', width=20, height=button_height,
                                       command=lambda: button_control('normal', root, standard_button_callback, list_of_labels, w, h, colors, lists, all_canvas))
    stop_hand_labeling_button.grid(column=12, row=1)

    create_mask_button = tk.Button(root,state = status, text='Create Mask', width=20, height=button_height,
                                command=lambda: mask_update(w, h, list_of_labels, lists, all_canvas))
    create_mask_button.grid(column=12, row=2)

    restore_button = tk.Button(root, state = status,text='Restore Image', width=20, height=button_height,
                            command=lambda: restore())
    restore_button.grid(column=13, row=2)

    erosion_kernel_3_mal_3_Button = tk.Button(root,state = status, text='Errosion 3x3', width=20, height=button_height,
                                           command=lambda: erosion(3, w, h))
    erosion_kernel_3_mal_3_Button.grid(column=12, row=4)

    erosion_kernel_5_mal_5_Button = tk.Button(root,state = status, text='Errosion 5x5', width=20, height=button_height,
                                           command=lambda: erosion(5, w, h))
    erosion_kernel_5_mal_5_Button.grid(column=12, row=5)

    erosion_kernel_7_mal_7_Button = tk.Button(root,state = status, text='Errosion 7x7', width=20, height=button_height,
                                           command=lambda: erosion(7, w, h))
    erosion_kernel_7_mal_7_Button.grid(column=12, row=6)

    erosion_kernel_9_mal_9_Button = tk.Button(root,state = status, text='Errosion 9x9', width=20, height=button_height,
                                           command=lambda: erosion(9, w, h))
    erosion_kernel_9_mal_9_Button.grid(column=12, row=7)

    dilation_kernel_3_mal_3_Button = tk.Button(root,state = status, text='Dilation 3x3', width=20, height=button_height,
                                            command=lambda: dilation(3, w, h))
    dilation_kernel_3_mal_3_Button.grid(column=13, row=4)

    dilation_kernel_5_mal_5_Button = tk.Button(root, state = status,text='Dilation 5x5', width=20, height=button_height,
                                            command=lambda: dilation(5, w, h))
    dilation_kernel_5_mal_5_Button.grid(column=13, row=5)

    dilation_kernel_7_mal_7_Button = tk.Button(root,state = status, text='Dilation 7x7', width=20, height=button_height,
                                            command=lambda: dilation(7, w, h))
    dilation_kernel_7_mal_7_Button.grid(column=13, row=6)

    dilation_kernel_9_mal_9_Button = tk.Button(root, state = status,text='Dilation 9x9', width=20, height=button_height,
                                            command=lambda: dilation(9, w, h))
    dilation_kernel_9_mal_9_Button.grid(column=13, row=7)

    delete_image_Button = tk.Button(root,state = status, text='Delete', width=20, height=button_height,
                                 command=lambda: delete_image(black))
    delete_image_Button.grid(column=12, row=3)

    get_pixels_button = tk.Button(root,state = status, text='Get Pixel Value', width=20, height=button_height,
                               command=lambda: get_pixel())
    get_pixels_button.grid(column=13, row=0)

    stop_get_pixels_button = tk.Button(root, state = status, text = 'Stop Get PV', width = 20, height = button_height, command=lambda: stop_get_pixels())
    stop_get_pixels_button.grid(column=13, row=1)

    make_blank_button = tk.Button(root, state = status, text = 'Make blank', width = 20, height = button_height, command=lambda: make_blank())
    make_blank_button.grid(column=13, row=3)

    dbscan_button = tk.Button(root, state = status, text = 'dbscan', width = 20, height = button_height, command = lambda: dbscan())
    dbscan_button.grid(column = 12, row = 8)

class Ok():

    def __init__(self, window, t1):
        self.window = window
        self.t1 = t1
        self.pixel_value = 0

    def ok(self):
        self.pixel_value = int(self.t1.get())
        if self.pixel_value >= 1 and self.pixel_value <= 255:
            messagebox.showinfo(title='Pixel Assingment', message='Successful pixel assignment')
            self.window.destroy()
        else:
            messagebox.showerror(title='Pixel Assingment', message='Pixel out of range')

    def already_assigned(self):
        self.pixel_value = 9999999999
        self.window.destroy()

def window_pixel_assignement():

    window = tk.Tk()
    window.title('Assign pixel value to mask (Label):')
    window.geometry('400x500')

    l1 = tk.Label(window, text='Choose for 1-255:', font=(14))
    l1.grid(row=0, column=0, padx=5, pady=5)
    entry_pixel = tk.StringVar()
    t1 = tk.Entry(window, textvariable=entry_pixel, font=(14))
    t1.grid(row=0, column=1)
    get_pixel_value = Ok(window, t1)
    b1 = tk.Button(window, command=lambda: get_pixel_value.ok(), text='Ok', font=(14))
    b1.grid(row=2, column=1)
    b2 = tk.Button(window, command = lambda: get_pixel_value.already_assigned(), text = 'Already Done', font=(14))
    b2.grid(row=3, column=1)

    window.mainloop()
    return get_pixel_value

class AllCanvas():

    def __init__(self, root, lists, rspan, w, h):
        self.w = w
        self.h = h
        self.sub_root = tk.Frame(root)
        self.sub_root.grid(column=0, row=0, rowspan=rspan, columnspan=10)
        self.canvas = tk.Canvas(self.sub_root, width=self.w, height=self.h)
        self.canvas.grid(column=0, row=0, rowspan=15)
        self.canvas_image = self.canvas.create_image(0, 0, anchor=tk.NW, image=lists.image_list[0])

        self.sub_root_2 = tk.Frame(root)
        self.sub_root_2.grid(column=0, row=self.h, rowspan=int(rspan / 2), columnspan=8)
        self.canvas_2 = tk.Canvas(self.sub_root_2, width=int(self.w * 0.8), height=int(self.h * 0.8))
        self.canvas_2.grid(column=0, row=0)
        self.canvas_2_image = self.canvas_2.create_image(0, 0, anchor=tk.NW, image=lists.mask_list[0])

        self.sub_root_3 = tk.Frame(root)
        self.sub_root_3.grid(column=9, row=self.h, rowspan=int(rspan / 2), columnspan=8)
        self.canvas_3 = tk.Canvas(self.sub_root_3, width=int(self.w * 0.8), height=int(self.h * 0.8))
        self.canvas_3.grid(column=0, row=0, rowspan=15)
        self.canvas_3_image = self.canvas_3.create_image(0, 0, anchor=tk.NW, image=lists.mask_image_merge_list[0])

    def update_canvas(self, lists):

        print('image_nr:', img_nr)
        print(len(lists.mask_image_merge_list))
        self.canvas.imgref = lists.image_list[img_nr]
        self.canvas_2.imgref = lists.mask_list[img_nr]
        self.canvas_3.imgref = lists.mask_image_merge_list[img_nr]
        self.canvas.itemconfig(self.canvas_image, image=lists.image_list[img_nr])
        self.canvas_2.itemconfig(self.canvas_2_image, image=lists.mask_list[img_nr])
        self.canvas_3.itemconfig(self.canvas_3_image, image=lists.mask_image_merge_list[img_nr])

    def draw_forms(self):

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
                    self.canvas.create_rectangle(x_one, y_one, x_two, y_two, width=1, outline=current_color)

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
                    self.canvas.create_line(last_corner, fill = current_color)

def window_labeling_tool():

    global canvas
    global canvas_2
    global canvas_3
    global images
    global root
    global canvas_2_image, canvas_3_image
    root = tk.Tk()
    root.geometry('1400x1300+0+0')
    path = 'images'

    h = 428
    w = 760
    rspan = 15  # rowspan of image

    images = os.listdir(path)
    lists = CreateImageList(path, images, w, h)



    list_of_labels = ['249', '250', '251', '248', '253', '254', '255']

    if len(os.listdir('bounding_boxes')) != 0:
        mask_path = 'bounding_boxes/' + images[img_nr]
        mask = Image.open(mask_path)

    else:
        mask = Image.open('black.png')

    mask = ImageTk.PhotoImage(mask.resize((int(w * 0.8), int(h * 0.8))))

    all_canvas = AllCanvas(root,lists,rspan,w,h)


    root.bind("<Right>", lambda x: next_image(root, list_of_labels, w, h, lists, all_canvas))

    button_control('normal', root, standard_button_callback, list_of_labels, w, h, colors, lists, all_canvas)
    root.mainloop()

if __name__ == '__main__':
    # Defining the tkinter root
    get_pixel_value = window_pixel_assignement()
    pixel_value = get_pixel_value.pixel_value

    if pixel_value > 0 and pixel_value <= 255:
        automated_masking(pixel_value)

    window_labeling_tool()


