from displaying import displaying_current_image

def next_image(root, labels_we_want, w, h, lists, all_canvas, label_dict_select_area, label_buttons, img_nr):

    img_nr.plus()
    lists.len()

    if img_nr.img_number == (lists.length - 1):
        root.unbind("<Right>")
    else:
        root.bind("<Right>", lambda x: next_image(root, labels_we_want, w, h, lists, all_canvas, label_dict_select_area,
                                                  label_buttons, img_nr))

    if img_nr.img_number == 0:
        root.unbind("<Left>")
    else:
        root.bind("<Left>", lambda x: last_image(root, labels_we_want, w, h, lists, all_canvas, label_dict_select_area,
                                                 label_buttons, img_nr))
    redo_mask_list = False
    displaying_current_image(lists, all_canvas, label_dict_select_area, img_nr, redo_mask_list,
                             label_buttons.label_buttons)


def last_image(root, labels_we_want, w, h, lists, all_canvas, label_dict_select_area, label_buttons, img_nr):

    img_nr.minus()
    if img_nr.img_number == -1:
        img_nr.img_number = 0
    lists.len()

    if img_nr.img_number == (lists.length - 1):
        root.unbind("<Right>")
    else:
        root.bind("<Right>", lambda x: next_image(root, labels_we_want, w, h, lists, all_canvas, label_dict_select_area,
                                                  label_buttons, img_nr))

    if img_nr.img_number == 0:
        root.unbind("<Left>")
    else:
        root.bind("<Left>", lambda x: last_image(root, labels_we_want, w, h, lists, all_canvas, label_dict_select_area,
                                                 label_buttons, img_nr))
    redo_mask_list = False
    displaying_current_image(lists, all_canvas, label_dict_select_area, img_nr, redo_mask_list,
                             label_buttons.label_buttons)
