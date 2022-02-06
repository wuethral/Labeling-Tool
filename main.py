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
from create_lists import CreateImageList, DictCoordinates
from canvas import AllCanvas
from windows import window_pixel_assignement
from buttons import button_control

label_buttons = []
img_nr = 0
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
    def __init__(self, root, which_column, callback_arg, callback, counting, nr_of_labels, w, h, color, label_state, lists, all_canvas, label_dict_select_area):
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
        self.lists = lists
        self.all_canvas = all_canvas
        self.label_dict_select_area = label_dict_select_area
        self.create_button()

    def create_button(self):
        self.button = tk.Button(self.root, text=self.callback_arg, fg = self.color, state=self.label_state,
                             command=lambda: self.callback(self.root, self.callback_arg,
                                                           self.w, self.h, self.color, self.lists, self.all_canvas, self.label_dict_select_area), width=10,
                             height=int(20 / self.nr_of_labels))
        self.button.grid(column=self.which_column, row=self.counting)


def standard_button_callback(root, lab, w, h, color, lists, all_canvas, label_dict_select_area):

    root.bind('s', lambda x: area_selection(root, w, h, lab, color, all_canvas, label_dict_select_area))
    root.bind('d', lambda x: clearing_of_label(root, lab, lists, all_canvas, label_dict_select_area))



def toggle_label_buttons(lab):
    global label_buttons
    for button_wrapper in label_buttons:
        if button_wrapper.button['text'] == lab:
            button_wrapper.button['fg'] = 'green'
        else:
            button_wrapper.button['fg'] = 'black'


def area_selection(root, w, h, lab, color, all_canvas, label_dict_select_area):

    AllCanvas.draw_initial_form(all_canvas, color, lab, label_dict_select_area, img_nr)


def clearing_of_label(root, lab, lists, all_canvas, label_dict_select_area):
    global canvas


    if img_nr in big_global_label_dict_rectangle:
        current_page_rectangle = big_global_label_dict_rectangle[img_nr]
        if lab in current_page_rectangle:
            del big_global_label_dict_rectangle[img_nr][lab]
        else:
            pass
    else:
        pass

    if img_nr in label_dict_select_area.dict:
        current_page_select_area = label_dict_select_area.dict[img_nr]
        if lab in current_page_select_area:
            del label_dict_select_area.dict[img_nr][lab]
        else:
            pass
    else:
        pass
    displaying_current_image(lists, all_canvas, label_dict_select_area)


def displaying_current_image(lists, all_canvas, label_dict_select_area):
    global label_buttons
    global redo_mask_list
    global images
    global img_nr
    global root

    if redo_mask_list:

        path = 'images'
        images = os.listdir(path)
        lists.update_lists()

    AllCanvas.update_canvas(all_canvas, lists, img_nr)
    AllCanvas.draw_forms(all_canvas, label_dict_select_area, img_nr, label_buttons)
    redo_mask_list = False

def next_image(root, labels_we_want, w, h, lists, all_canvas, label_dict_select_area):
    global img_nr
    global label_buttons

    global get_pixel_flag
    get_pixel_flag = False
    img_nr += 1
    lists.len()

    if img_nr == (lists.length - 1):
        root.unbind("<Right>")
    else:
        root.bind("<Right>", lambda x: next_image(root, labels_we_want, w, h, lists, all_canvas, label_dict_select_area))

    if img_nr == 0:
        root.unbind("<Left>")
    else:
        root.bind("<Left>", lambda x: last_image(root, labels_we_want, w, h, lists, all_canvas, label_dict_select_area))

    displaying_current_image(lists, all_canvas, label_dict_select_area)

def last_image(root, labels_we_want, w, h, lists, all_canvas, label_dict_select_area):
    global img_nr
    global get_pixel_flag
    get_pixel_flag = False
    img_nr -= 1
    if img_nr == -1:
        img_nr = 0
    print('img_nr',img_nr)
    lists.len()

    if img_nr == (lists.length - 1):
        root.unbind("<Right>")
    else:
        root.bind("<Right>", lambda x: next_image(root, labels_we_want, w, h, lists, all_canvas, label_dict_select_area))

    if img_nr == 0:
        root.unbind("<Left>")
    else:
        root.bind("<Left>", lambda x: last_image(root, labels_we_want, w, h, lists, all_canvas, label_dict_select_area))

    displaying_current_image(lists, all_canvas, label_dict_select_area)

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

def mask_update(w, h, list_of_labels, lists,all_canvas, label_dict_select_area):
    global images
    global redo_mask_list
    print(w, h)
    mask_creation(w, h, 10, list_of_labels, label_dict_select_area.dict, images)
    label_dict_select_area.dict = {}
    redo_mask_list = True
    displaying_current_image(lists, all_canvas, label_dict_select_area)

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

''' 
def button_control(status, root, standard_button_callback, list_of_labels, w, h, colors, lists, all_canvas, label_dict_select_area):
    count = 1
    label_title = tk.Label(root, text='Labels:')
    label_title.grid(column=10, row=0)


    if status == 'normal':
        label_state = 'disabled'

    else:
        label_state = 'normal'

    for label in list_of_labels:
        label_buttons.append(TKButtonWrapper(root, 10, label, standard_button_callback, count, len(list_of_labels), w, h, colors[count], label_state, lists, all_canvas, label_dict_select_area))
        count += 1

    button_height = int(20 / len(list_of_labels))

    hand_labeling_button = tk.Button(root, state = status, text='Start Hand Labeling', width=20, height=button_height,
                                  command=lambda: button_control('disabled', root, standard_button_callback, list_of_labels, w, h, colors, lists, all_canvas, label_dict_select_area))
    hand_labeling_button.grid(column=12, row=0)

    stop_hand_labeling_button = tk.Button(root,state = 'normal', text='Stop Hand Labeling', width=20, height=button_height,
                                       command=lambda: button_control('normal', root, standard_button_callback, list_of_labels, w, h, colors, lists, all_canvas, label_dict_select_area))
    stop_hand_labeling_button.grid(column=12, row=1)

    create_mask_button = tk.Button(root,state = status, text='Create Mask', width=20, height=button_height,
                                command=lambda: mask_update(w, h, list_of_labels, lists, all_canvas, label_dict_select_area))
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
'''

def window_labeling_tool():

    global images
    global root
    root = tk.Tk()
    root.geometry('1400x1300+0+0')
    path = 'images'

    h = 428
    w = 760
    rspan = 15  # rowspan of image

    images = os.listdir(path)
    lists = CreateImageList(path, images, w, h)
    lists.create_image_list()
    lists.creating_masks_list()



    list_of_labels = ['249', '250', '251', '248', '253', '254', '255']

    if len(os.listdir('bounding_boxes')) != 0:
        mask_path = 'bounding_boxes/' + images[img_nr]
        mask = Image.open(mask_path)

    else:
        mask = Image.open('black.png')

    mask = ImageTk.PhotoImage(mask.resize((int(w * 0.8), int(h * 0.8))))

    all_canvas = AllCanvas(root,lists,rspan,w,h)

    label_dict_select_area = DictCoordinates()
    root.bind("<Right>", lambda x: next_image(root, list_of_labels, w, h, lists, all_canvas, label_dict_select_area))


    button_control('normal', root, standard_button_callback, list_of_labels, w, h, colors, lists, all_canvas, label_dict_select_area, label_buttons)
    root.mainloop()

if __name__ == '__main__':
    # Defining the tkinter root
    get_pixel_value = window_pixel_assignement()
    pixel_value = get_pixel_value.pixel_value

    if pixel_value > 0 and pixel_value <= 255:
        automated_masking(pixel_value)

    window_labeling_tool()


