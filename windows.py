import tkinter as tk
from tkinter import messagebox
import os
from create_lists import CreateImageList, DictCoordinates
from canvas import AllCanvas
from label_buttons import LabelButton
from foreward_backward import next_image
from buttons import button_control, standard_button_callback
from list_of_colors import colors
from img_number import ImgNumber


class Ok():
    '''This class contains the functions for the buttons presses in the first window pop-up'''

    def __init__(self, window, t1, t2):
        self.window = window
        self.t1 = t1
        self.t2 = t2
        self.pixel_value = 0
        self.automated_masking = False

    def ok(self):
        '''This function gets the pixel value, when we want automated masking'''

        # Getting the pixel value from t1
        self.pixel_value = int(self.t1.get())

        # If the pixel value is in the range [1,255], the pixel assignment was successful. Otherwise not.
        if self.pixel_value >= 1 and self.pixel_value <= 255:
            messagebox.showinfo(title='Pixel Assingment', message='Successful pixel assignment')

            # Setting the attribute self.automated_masking to True
            self.automated_masking = True

            # Destroying window
            self.window.destroy()
        else:
            messagebox.showerror(title='Pixel Assingment', message='Pixel out of range')

    def already_assigned(self):
        '''This function gets the pixel value, when we don't want automated masking'''

        # Getting the pixel value from t2
        self.pixel_value = int(self.t2.get())
        # Setting the attribute self.automated_masking to False
        self.automated_masking = False
        # Destroy window
        self.window.destroy()


def window_pixel_assignment():
    '''In this function is responsible for the GUI, where one can decide if he wants to perform the automated masking or
     not. And also for what pixel value'''

    # Creating a new tkinter object and defining it's title and geometry
    window = tk.Tk()
    window.title('Assign pixel value to mask (label):')
    window.geometry('700x70')

    # Creating a label and placing it on window
    l1 = tk.Label(window, text='Automated masking: Choose from 1-255:', font=(14))
    l1.grid(row=0, column=0, padx=5, pady=5)

    # Creating a field, where one can write text in the GUI and placing it on window
    entry_pixel = tk.StringVar()
    pixel_value = tk.Entry(window, textvariable=entry_pixel, font=(14))
    pixel_value.grid(row=0, column=1)

    l2 = tk.Label(window, text='No automated masking: Type in the pixel value of your masks:', font=(14))
    l2.grid(row=1, column=0, padx=5, pady=5)

    entry_pixel_2 = tk.StringVar()
    pixel_value_2 = tk.Entry(window, textvariable=entry_pixel_2, font=(14))
    pixel_value_2.grid(row=1, column=1)

    # Creating an object get_pixel_value from the class Ok with window and pixel_value as inputs
    get_pixel_value = Ok(window, pixel_value, pixel_value_2)

    # Creating a button that calls the function get_pixel_value.ok() from the class Ok() and placing it on window
    b1 = tk.Button(window, command=lambda: get_pixel_value.ok(), text='Ok', font=(14))
    b1.grid(row=0, column=3)

    # Creating a button that calls the function get_pixel_value.already_assigned() from the class Ok() and placing it
    # on window
    b2 = tk.Button(window, command=lambda: get_pixel_value.already_assigned(), text='Ok', font=(14))
    b2.grid(row=1, column=3)

    window.mainloop()

    # Returning the get_pixel_value to the main function
    return get_pixel_value


def window_labeling_tool(pixel_value):
    '''Main function of the labeling tool interface'''

    # Creating an object root and defining its title and geometry with width=1400, height=1300, and origin on
    # screen (0,0)
    root = tk.Tk()
    root.title('Labeling Tool')
    root.geometry('1230x780+0+0')

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
    list_of_labels = ['50', '250', '251', '248', '253', '254', '255']

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
