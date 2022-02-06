import tkinter as tk

def button_control(status, root, standard_button_callback, list_of_labels, w, h, colors, lists, all_canvas,
                   label_dict_select_area, label_buttons):
    count = 1
    label_title = tk.Label(root, text='Labels:')
    label_title.grid(column=10, row=0)

    if status == 'normal':
        label_state = 'disabled'

    else:
        label_state = 'normal'

    for label in list_of_labels:
        label_buttons.append(
            TKButtonWrapper(root, 10, label, standard_button_callback, count, len(list_of_labels), w, h, colors[count],
                            label_state, lists, all_canvas, label_dict_select_area))
        count += 1

    button_height = int(20 / len(list_of_labels))

    hand_labeling_button = tk.Button(root, state=status, text='Start Hand Labeling', width=20, height=button_height,
                                     command=lambda: button_control('disabled', root, standard_button_callback,
                                                                    list_of_labels, w, h, colors, lists, all_canvas,
                                                                    label_dict_select_area))
    hand_labeling_button.grid(column=12, row=0)

    stop_hand_labeling_button = tk.Button(root, state='normal', text='Stop Hand Labeling', width=20,
                                          height=button_height,
                                          command=lambda: button_control('normal', root, standard_button_callback,
                                                                         list_of_labels, w, h, colors, lists,
                                                                         all_canvas, label_dict_select_area))
    stop_hand_labeling_button.grid(column=12, row=1)

    create_mask_button = tk.Button(root, state=status, text='Create Mask', width=20, height=button_height,
                                   command=lambda: mask_update(w, h, list_of_labels, lists, all_canvas,
                                                               label_dict_select_area))
    create_mask_button.grid(column=12, row=2)

    ''' 

    restore_button = tk.Button(root, state=status, text='Restore Image', width=20, height=button_height,
                               command=lambda: restore())
    restore_button.grid(column=13, row=2)

    erosion_kernel_3_mal_3_Button = tk.Button(root, state=status, text='Errosion 3x3', width=20, height=button_height,
                                              command=lambda: erosion(3, w, h))
    erosion_kernel_3_mal_3_Button.grid(column=12, row=4)

    erosion_kernel_5_mal_5_Button = tk.Button(root, state=status, text='Errosion 5x5', width=20, height=button_height,
                                              command=lambda: erosion(5, w, h))
    erosion_kernel_5_mal_5_Button.grid(column=12, row=5)

    erosion_kernel_7_mal_7_Button = tk.Button(root, state=status, text='Errosion 7x7', width=20, height=button_height,
                                              command=lambda: erosion(7, w, h))
    erosion_kernel_7_mal_7_Button.grid(column=12, row=6)

    erosion_kernel_9_mal_9_Button = tk.Button(root, state=status, text='Errosion 9x9', width=20, height=button_height,
                                              command=lambda: erosion(9, w, h))
    erosion_kernel_9_mal_9_Button.grid(column=12, row=7)

    dilation_kernel_3_mal_3_Button = tk.Button(root, state=status, text='Dilation 3x3', width=20, height=button_height,
                                               command=lambda: dilation(3, w, h))
    dilation_kernel_3_mal_3_Button.grid(column=13, row=4)

    dilation_kernel_5_mal_5_Button = tk.Button(root, state=status, text='Dilation 5x5', width=20, height=button_height,
                                               command=lambda: dilation(5, w, h))
    dilation_kernel_5_mal_5_Button.grid(column=13, row=5)

    dilation_kernel_7_mal_7_Button = tk.Button(root, state=status, text='Dilation 7x7', width=20, height=button_height,
                                               command=lambda: dilation(7, w, h))
    dilation_kernel_7_mal_7_Button.grid(column=13, row=6)

    dilation_kernel_9_mal_9_Button = tk.Button(root, state=status, text='Dilation 9x9', width=20, height=button_height,
                                               command=lambda: dilation(9, w, h))
    dilation_kernel_9_mal_9_Button.grid(column=13, row=7)

    delete_image_Button = tk.Button(root, state=status, text='Delete', width=20, height=button_height,
                                    command=lambda: delete_image(black))
    delete_image_Button.grid(column=12, row=3)

    get_pixels_button = tk.Button(root, state=status, text='Get Pixel Value', width=20, height=button_height,
                                  command=lambda: get_pixel())
    get_pixels_button.grid(column=13, row=0)

    stop_get_pixels_button = tk.Button(root, state=status, text='Stop Get PV', width=20, height=button_height,
                                       command=lambda: stop_get_pixels())
    stop_get_pixels_button.grid(column=13, row=1)

    make_blank_button = tk.Button(root, state=status, text='Make blank', width=20, height=button_height,
                                  command=lambda: make_blank())
    make_blank_button.grid(column=13, row=3)

    dbscan_button = tk.Button(root, state=status, text='dbscan', width=20, height=button_height,
                              command=lambda: dbscan())
    dbscan_button.grid(column=12, row=8)
    '''