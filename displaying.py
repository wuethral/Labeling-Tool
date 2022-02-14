from canvas import AllCanvas
import os

def displaying_current_image(lists, all_canvas, label_dict_select_area, img_nr, redo_mask_list, label_buttons):

    if redo_mask_list:
        lists.update_lists()

    AllCanvas.update_canvas(all_canvas, lists, img_nr)
    AllCanvas.draw_forms(all_canvas, label_dict_select_area, img_nr, label_buttons)
