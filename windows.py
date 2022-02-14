import tkinter as tk
from tkinter import messagebox
import os
from create_lists import CreateImageList, DictCoordinates
from PIL import Image, ImageTk
from canvas import AllCanvas
from label_buttons import LabelButton
from foreward_backward import next_image
from buttons import button_control, standard_button_callback
from list_of_colors import colors
from img_number import ImgNumber


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
    pixel_value = tk.Entry(window, textvariable=entry_pixel, font=(14))
    pixel_value.grid(row=0, column=1)
    get_pixel_value = Ok(window, pixel_value)
    b1 = tk.Button(window, command=lambda: get_pixel_value.ok(), text='Ok', font=(14))
    b1.grid(row=2, column=1)
    b2 = tk.Button(window, command=lambda: get_pixel_value.already_assigned(), text='Already Done', font=(14))
    b2.grid(row=3, column=1)

    window.mainloop()
    return get_pixel_value


def window_labeling_tool(pixel_value):
    '''Main function of the labeling tool interface'''

    # Creating an object root and defining its geometry with width=1400, height=1300, and origin on screen (0,0)
    root = tk.Tk()
    root.geometry('1400x1300+0+0')

    # Saving the image names in folder 'images' in a list
    path = 'images'
    images = os.listdir(path)

    # Defining the images geometry width height h, width w and row span rspan
    h = 428
    w = 760
    rspan = 15

    # Creating an object list filling it with the images and masks
    lists = CreateImageList(path, images, w, h)
    lists.create_image_list()
    lists.creating_masks_list()

    # creating object image_number
    img_number = ImgNumber()

    # creating an object with all canvases in it
    all_canvas = AllCanvas(root, lists, rspan, w, h)

    # list of labels for the masks, these will be pixel values of the masks
    list_of_labels = ['249', '250', '251', '248', '253', '254', '255']

    # Creating and object in which the corner coordinates of the hand labeling polygons are saved
    label_dict_select_area = DictCoordinates()

    # Creating an object where the buttons for the labeling are saved in a list
    label_buttons = LabelButton()

    # Binding the right button on keyboard of computer to the root. Calling function next_image, when pressing this
    # button
    root.bind("<Right>",
              lambda x: next_image(root, list_of_labels, w, h, lists, all_canvas, label_dict_select_area, label_buttons,
                                   img_number))

    # Calling function button control with with all necessary variables
    redo_mask_list = False
    button_control('normal', root, standard_button_callback, list_of_labels, w, h, colors, lists, all_canvas,
                   label_dict_select_area, label_buttons, img_number, redo_mask_list, images, pixel_value)

    root.mainloop()
