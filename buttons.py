import tkinter as tk
from canvas import AllCanvas
from displaying import displaying_current_image
from update import mask_update
from list_of_colors import colors
from button_fuctions import delete_image, restore, erosion, dilation, get_pixel, make_blank, dbscan



def area_selection(lab, color, all_canvas, label_dict_select_area, img_nr):
    '''This function calls the function draw_initial_form from the class AllCanvas'''

    AllCanvas.draw_initial_form(all_canvas, color, lab, label_dict_select_area, img_nr)


def clearing_of_label(lab, lists, all_canvas, label_dict_select_area, img_nr, label_buttons):
    '''When the masks haven't been created yet, the polygon at the current image and label is deleted.'''

    # Checking, if the current image number is in the label_dict_select_area.dict, where the current polygons are saved.
    if img_nr.img_number in label_dict_select_area.dict:
        # Accessing label_dict_select_area.dict[img_nr.img_number] and saving it in current_page_select_area
        current_page_select_area = label_dict_select_area.dict[img_nr.img_number]
        # Checking if the current label is in current_page_select_area
        if lab in current_page_select_area:
            # Delete the corner coordinates of the polygon or polygons at that position
            label_dict_select_area.delete(img_nr.img_number, lab)
        else:
            pass
    else:
        pass
    redo_mask_list = False
    displaying_current_image(lists, all_canvas, label_dict_select_area, img_nr, redo_mask_list, label_buttons)


class TKButtonWrapper:
    '''This class creates the buttons on the GUI and adds a function call to each button'''

    def __init__(self, root, which_column, callback_arg, callback, counting, nr_of_labels, w, h, color, label_state,
                 lists, all_canvas, label_dict_select_area, img_nr, redo_mask_list, label_buttons):
        '''This function defines all attributes of the class and in the last line calls the function
        self.create_button'''

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
        self.img_nr = img_nr
        self.redo_mask_list = redo_mask_list
        self.label_buttons = label_buttons
        self.create_button()

    def create_button(self):
        '''The button attribute is created and the attribute self.callback is added to each button. It is possible to
        add different attributes in the funciton self.callback for every button, making it possible to add a different
        label to every button call'''

        self.button = tk.Button(self.root, text=self.callback_arg, fg=self.color, state=self.label_state,
                                command=lambda: self.callback(self.root, self.callback_arg,
                                                              self.w, self.h, self.color, self.lists, self.all_canvas,
                                                              self.label_dict_select_area, self.img_nr,
                                                              self.redo_mask_list, self.label_buttons), width=10,
                                height=int(20 / self.nr_of_labels))
        # Placing the buttons on the grid
        self.button.grid(column=self.which_column, row=self.counting)


def standard_button_callback(root, lab, w, h, color, lists, all_canvas, label_dict_select_area, img_nr, redo_mask_list,
                             label_buttons):
    '''This function binds the buttons s and d on the keyboard to the functions area_selection() and
    clearing_of_label()'''

    # Button s on the keyboard is bound to the root with the command area_selection()
    root.bind('s', lambda x: area_selection(lab, color, all_canvas, label_dict_select_area, img_nr))

    # Button d on the keyboard is bound to the root with the command clearing_of_label()
    root.bind('d', lambda x: clearing_of_label(lab, lists, all_canvas, label_dict_select_area, img_nr, label_buttons))


def button_control(status, root, standard_button_callback, list_of_labels, w, h, colors, lists, all_canvas,
                   label_dict_select_area, label_buttons, img_nr, redo_mask_list, images, pixel_value):
    '''Control of all the buttons in the GUI'''

    # Setting the counter to 1. This counter will be an input to the class TKButtonWrapper and is important for the
    # placement of the different buttons on the grid
    count = 1

    # This is the tittle of the buttons. It will be didplayed in the GUI on top of all buttons.
    label_title = tk.Label(root, text='Labels:')
    label_title.grid(column=10, row=0)

    # This if else statement determines if the state of the buttons is 'disabled' or 'normal', meaning turned on or off.
    if status == 'normal':
        label_state = 'disabled'
    else:
        label_state = 'normal'

    # Looping through all the labels and Create a object TKButtonWrapper for each label
    for label in list_of_labels:
        # Appending each TKButtonWrapper object to the attribute label_buttons from the class label_button
        label_buttons.label_buttons.append(
            TKButtonWrapper(root, 10, label, standard_button_callback, count, len(list_of_labels), w, h, colors[count],
                            label_state, lists, all_canvas, label_dict_select_area, img_nr, redo_mask_list,
                            label_buttons))
        # Adding 1 to the counter, in order for the buttons to be 1 position lower on the grid than the last button
        count += 1

    # The height of the button is defined as 20 divided by the length of the list_of_labels list
    button_height = int(20 / len(list_of_labels))

    # The hand_labeling_button controls the state of all buttons on the GUI. It calls the function button_control(), but
    # with the first input as 'disabled' This button activates the buttons TKButtonWrapper, but deactivates all other
    # buttons except the stop_hand_labeling_button. The button is placed on the grid at column 12 and row 0
    hand_labeling_button = tk.Button(root, state=status, text='Start Hand Labeling', width=20, height=button_height,
                                     command=lambda: button_control('disabled', root, standard_button_callback,
                                                                    list_of_labels, w, h, colors, lists, all_canvas,
                                                                    label_dict_select_area,label_buttons, img_nr,
                                                                    redo_mask_list, images, pixel_value))
    hand_labeling_button.grid(column=12, row=0)

    # The stop_hand_labeling_button does the opposite of the hand_labeling_button. It deactivates the buttons in
    # TKButtonWrapper, but reacvtivates all other buttons.
    # buttons except the stop_hand_labeling_button.
    # The button is placed on the grid at column 12 and row 1
    stop_hand_labeling_button = tk.Button(root, state='normal', text='Stop Hand Labeling', width=20,
                                          height=button_height,
                                          command=lambda: button_control('normal', root, standard_button_callback,
                                                                         list_of_labels, w, h, colors, lists,
                                                                         all_canvas, label_dict_select_area,
                                                                         label_buttons, img_nr, redo_mask_list, images,
                                                                         pixel_value))
    stop_hand_labeling_button.grid(column=12, row=1)

    # The create_mask_button calls the function mask_update
    # The button is placed on the grid at column 12 and row 2
    create_mask_button = tk.Button(root, state=status, text='Create Mask', width=20, height=button_height,
                                   command=lambda: mask_update(w, h, list_of_labels, lists, all_canvas,
                                                               label_dict_select_area, images, img_nr, label_buttons))
    create_mask_button.grid(column=12, row=2)

    # The delete_image_button calls the function delete_image.
    # The button is placed on the grid at column 12 and row 3
    delete_image_button = tk.Button(root, state=status, text='Delete', width=20, height=button_height,
                                    command=lambda: delete_image(images, lists, all_canvas, label_dict_select_area,
                                                                 label_buttons, img_nr))
    delete_image_button.grid(column=12, row=3)

    # The restore_button calls the function restore
    # The button is placed on the grid at column 13 and row 2
    restore_button = tk.Button(root, state=status, text='Restore Image', width=20, height=button_height,
                               command=lambda: restore(images, lists, img_nr, w, h, all_canvas, label_dict_select_area,
                                                       label_buttons))
    restore_button.grid(column=13, row=2)

    erosion_kernel_3_mal_3_Button = tk.Button(root, state=status, text='Errosion 3x3', width=20, height=button_height,
                                              command=lambda: erosion(3, w, h, images, lists, all_canvas,
                                                                      label_dict_select_area, img_nr, label_buttons))
    erosion_kernel_3_mal_3_Button.grid(column=12, row=4)

    erosion_kernel_5_mal_5_Button = tk.Button(root, state=status, text='Errosion 5x5', width=20, height=button_height,
                                              command=lambda: erosion(5, w, h, images, lists, all_canvas,
                                                                      label_dict_select_area, img_nr, label_buttons))
    erosion_kernel_5_mal_5_Button.grid(column=12, row=5)

    erosion_kernel_7_mal_7_Button = tk.Button(root, state=status, text='Errosion 7x7', width=20, height=button_height,
                                              command=lambda: erosion(7, w, h, images, lists, all_canvas,
                                                                      label_dict_select_area, img_nr, label_buttons))
    erosion_kernel_7_mal_7_Button.grid(column=12, row=6)

    erosion_kernel_9_mal_9_Button = tk.Button(root, state=status, text='Errosion 9x9', width=20, height=button_height,
                                              command=lambda: erosion(9, w, h, images, lists, all_canvas,
                                                                      label_dict_select_area, img_nr, label_buttons))
    erosion_kernel_9_mal_9_Button.grid(column=12, row=7)

    dilation_kernel_3_mal_3_Button = tk.Button(root, state=status, text='Dilation 3x3', width=20, height=button_height,
                                               command=lambda: dilation(3, w, h, images, lists, all_canvas,
                                                                        label_dict_select_area, img_nr, label_buttons))
    dilation_kernel_3_mal_3_Button.grid(column=13, row=4)

    dilation_kernel_5_mal_5_Button = tk.Button(root, state=status, text='Dilation 5x5', width=20, height=button_height,
                                               command=lambda: dilation(5, w, h, images, lists, all_canvas,
                                                                        label_dict_select_area, img_nr, label_buttons))
    dilation_kernel_5_mal_5_Button.grid(column=13, row=5)

    dilation_kernel_7_mal_7_Button = tk.Button(root, state=status, text='Dilation 7x7', width=20, height=button_height,
                                               command=lambda: dilation(7, w, h, images, lists, all_canvas,
                                                                        label_dict_select_area, img_nr, label_buttons))
    dilation_kernel_7_mal_7_Button.grid(column=13, row=6)

    dilation_kernel_9_mal_9_Button = tk.Button(root, state=status, text='Dilation 9x9', width=20, height=button_height,
                                               command=lambda: dilation(9, w, h, images, lists, all_canvas,
                                                                        label_dict_select_area, img_nr, label_buttons))
    dilation_kernel_9_mal_9_Button.grid(column=13, row=7)

    root.bind('p', lambda x: get_pixel(root, all_canvas, lists, label_dict_select_area, img_nr, label_buttons, images))


    make_blank_button = tk.Button(root, state=status, text='Make blank', width=20, height=button_height,
                                  command=lambda: make_blank(images, img_nr, lists, all_canvas, label_dict_select_area,
                                                             label_buttons))
    make_blank_button.grid(column=13, row=3)
    
    dbscan_button = tk.Button(root, state=status, text='dbscan', width=20, height=button_height,
                              command=lambda: dbscan(images, img_nr, lists, w, h, all_canvas, label_dict_select_area,
                                                     label_buttons, pixel_value))
    dbscan_button.grid(column=12, row=8)
