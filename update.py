from create_mask import mask_creation
from displaying import displaying_current_image


def mask_update(w, h, list_of_labels, lists,all_canvas, label_dict_select_area, images, img_nr, label_buttons):
    '''The function mask_creation is called, which creates all masks of the current polygons in
    label_dict_select_area.dict'''

    # function mask_creation is called
    mask_creation(w, h, len(images), list_of_labels, label_dict_select_area.dict, images)

    # attribute dict from label_dict_select_area is set to an empty dictionary, because the masks have been created
    # there is no need to save the corner coordinates anymore
    label_dict_select_area.dict = {}

    # redo_mask_list has to be True, because we made changes in the folders masks and image_mask_merge
    redo_mask_list = True
    displaying_current_image(lists, all_canvas, label_dict_select_area, img_nr, redo_mask_list, label_buttons)