from canvas import AllCanvas


def displaying_current_image(lists, all_canvas, label_dict_select_area, img_nr, redo_mask_list, label_buttons):
    '''This function updates all the canvases'''

    # When redo_mask_list is True, lists.update_lists is called for creating new lists (image, mask, mask_image_merge)
    if redo_mask_list:
        lists.update_lists()

    # updating the canvas
    AllCanvas.update_canvas(all_canvas, lists, img_nr)

    # Drawing the polygons on the current image number on canvas
    AllCanvas.draw_forms(all_canvas, label_dict_select_area, img_nr, label_buttons)
