from displaying import displaying_current_image


def next_image(root, labels_we_want, w, h, lists, all_canvas, label_dict_select_area, label_buttons, img_nr):
    '''This function is responsible for displaying the next image, when going forward in the tool'''

    # Adding 1 to the image number (attribute img_number from object img_nr)
    img_nr.plus()

    # Calculating the length of the attribute image_list from the object lists (number of images in the folder images)
    # The length is saved as self.length in the class CreateImageList
    lists.len()

    # If the current image is the last image, unbind the function next_image from the right arrow on the keyboard
    if img_nr.img_number == (lists.length - 1):
        root.unbind("<Right>")
    # Else, bind the right arrow to the function next_image again, but with the updated parameters
    else:
        root.bind("<Right>", lambda x: next_image(root, labels_we_want, w, h, lists, all_canvas, label_dict_select_area,
                                                  label_buttons, img_nr))

    # If the current iag is the first image, unbind the function last_image form the left arrow on the keyboard
    if img_nr.img_number == 0:
        root.unbind("<Left>")
    # Else, bind the left arrow the the function last image again, but with the updated parameters
    else:
        root.bind("<Left>", lambda x: last_image(root, labels_we_want, w, h, lists, all_canvas, label_dict_select_area,
                                                 label_buttons, img_nr))

    # redo_mask_list is False, because we didn't make any changes in the folders
    redo_mask_list = False
    displaying_current_image(lists, all_canvas, label_dict_select_area, img_nr, redo_mask_list,
                             label_buttons.label_buttons)


def last_image(root, labels_we_want, w, h, lists, all_canvas, label_dict_select_area, label_buttons, img_nr):
    '''This function is responsible for displaying the next image, when going backward in the tool'''

    # Subtracting 1 to the image number (attribute img_number from object img_nr)
    img_nr.minus()

    # When img_nr.img_number becomes (-1), make it zero
    if img_nr.img_number == -1:
        img_nr.img_number = 0

    # Calculating the length of the attribute image_list from the object lists (number of images in the folder images)
    # The length is saved as self.length in the class CreateImageList
    lists.len()

    # If the current image is the last image, unbind the function next_image from the right arrow on the keyboard
    if img_nr.img_number == (lists.length - 1):
        root.unbind("<Right>")
    # Else, bind the right arrow to the function next_image again, but with the updated parameters
    else:
        root.bind("<Right>", lambda x: next_image(root, labels_we_want, w, h, lists, all_canvas, label_dict_select_area,
                                                  label_buttons, img_nr))

    # If the current iag is the first image, unbind the function last_image form the left arrow on the keyboard
    if img_nr.img_number == 0:
        root.unbind("<Left>")
    # Else, bind the left arrow the the function last image again, but with the updated parameters
    else:
        root.bind("<Left>", lambda x: last_image(root, labels_we_want, w, h, lists, all_canvas, label_dict_select_area,
                                                 label_buttons, img_nr))

    # redo_mask_list is False, because we didn't make any changes in the folders
    redo_mask_list = False
    displaying_current_image(lists, all_canvas, label_dict_select_area, img_nr, redo_mask_list,
                             label_buttons.label_buttons)
