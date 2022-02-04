import tkinter as tk

class AllCanvas():

    def __init__(self, root, lists, rspan, w, h):
        self.w = w
        self.h = h
        self.sub_root = tk.Frame(root)
        self.sub_root.grid(column=0, row=0, rowspan=rspan, columnspan=10)
        self.canvas = tk.Canvas(self.sub_root, width=self.w, height=self.h)
        self.canvas.grid(column=0, row=0, rowspan=15)
        self.canvas_image = self.canvas.create_image(0, 0, anchor=tk.NW, image=lists.image_list[0])

        self.sub_root_2 = tk.Frame(root)
        self.sub_root_2.grid(column=0, row=self.h, rowspan=int(rspan / 2), columnspan=8)
        self.canvas_2 = tk.Canvas(self.sub_root_2, width=int(self.w * 0.8), height=int(self.h * 0.8))
        self.canvas_2.grid(column=0, row=0)
        self.canvas_2_image = self.canvas_2.create_image(0, 0, anchor=tk.NW, image=lists.mask_list[0])

        self.sub_root_3 = tk.Frame(root)
        self.sub_root_3.grid(column=9, row=self.h, rowspan=int(rspan / 2), columnspan=8)
        self.canvas_3 = tk.Canvas(self.sub_root_3, width=int(self.w * 0.8), height=int(self.h * 0.8))
        self.canvas_3.grid(column=0, row=0, rowspan=15)
        self.canvas_3_image = self.canvas_3.create_image(0, 0, anchor=tk.NW, image=lists.mask_image_merge_list[0])

    def update_canvas(self, lists):

        print('image_nr:', img_nr)
        print(len(lists.mask_image_merge_list))
        self.canvas.imgref = lists.image_list[img_nr]
        self.canvas_2.imgref = lists.mask_list[img_nr]
        self.canvas_3.imgref = lists.mask_image_merge_list[img_nr]
        self.canvas.itemconfig(self.canvas_image, image=lists.image_list[img_nr])
        self.canvas_2.itemconfig(self.canvas_2_image, image=lists.mask_list[img_nr])
        self.canvas_3.itemconfig(self.canvas_3_image, image=lists.mask_image_merge_list[img_nr])

    def draw_forms(self):

        if img_nr in big_global_label_dict_rectangle.keys():
            for rect_labels in big_global_label_dict_rectangle[img_nr].keys():
                for button_wrapper in label_buttons:
                    if button_wrapper.button['text'] == rect_labels:
                        current_color = button_wrapper.button['fg']
                for rect_coordinates in range(len(big_global_label_dict_rectangle[img_nr][rect_labels])):
                    x_one = big_global_label_dict_rectangle[img_nr][rect_labels][rect_coordinates][0][0]
                    y_one = big_global_label_dict_rectangle[img_nr][rect_labels][rect_coordinates][0][1]
                    x_two = big_global_label_dict_rectangle[img_nr][rect_labels][rect_coordinates][1][0]
                    y_two = big_global_label_dict_rectangle[img_nr][rect_labels][rect_coordinates][1][1]
                    self.canvas.create_rectangle(x_one, y_one, x_two, y_two, width=1, outline=current_color)

        if img_nr in big_global_label_dict_select_area.keys():
            for select_area_labels in big_global_label_dict_select_area[img_nr].keys():
                for button_wrapper in label_buttons:
                    if button_wrapper.button['text'] == select_area_labels:
                        current_color = button_wrapper.button['fg']
                for area_corner_coords in range(len(big_global_label_dict_select_area[img_nr][select_area_labels])):

                    for i in range(len(
                            big_global_label_dict_select_area[img_nr][select_area_labels][area_corner_coords]) - 1):
                        corner1 = big_global_label_dict_select_area[img_nr][select_area_labels][area_corner_coords][i]
                        corner2 = big_global_label_dict_select_area[img_nr][select_area_labels][area_corner_coords][
                            i + 1]
                        canvas.create_line(corner1, corner2, width=1, fill=current_color)
                    first_corner = big_global_label_dict_select_area[img_nr][select_area_labels][area_corner_coords][
                        0]
                    last_corner = big_global_label_dict_select_area[img_nr][select_area_labels][area_corner_coords][
                        -1]
                    self.canvas.create_line(last_corner, fill = current_color)