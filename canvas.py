import tkinter as tk


def saving_corner_coordinates(modus, coordinates, lab, label_dict_select_area, img_nr):
    global big_global_label_dict_rectangle
    if modus == 'rect':
        if not img_nr in big_global_label_dict_rectangle.keys():
            big_global_label_dict_rectangle[img_nr] = {}
            big_global_label_dict_rectangle[img_nr][lab] = [coordinates]
        elif img_nr in big_global_label_dict_rectangle.keys():
            if not lab in big_global_label_dict_rectangle[img_nr].keys():
                big_global_label_dict_rectangle[img_nr][lab] = [coordinates]
            elif lab in big_global_label_dict_rectangle[img_nr].keys():
                big_global_label_dict_rectangle[img_nr][lab].append(coordinates)
    elif modus == 'sel_area':
        if not img_nr in label_dict_select_area.dict.keys():

            label_dict_select_area.dict[img_nr] = {}
            label_dict_select_area.dict[img_nr][lab] = [coordinates]
        elif img_nr in label_dict_select_area.dict.keys():

            if not lab in label_dict_select_area.dict[img_nr].keys():
                label_dict_select_area.dict[img_nr][lab] = [
                    coordinates]
            elif lab in label_dict_select_area.dict[img_nr].keys():
                label_dict_select_area.dict[img_nr][lab].append(
                    coordinates)

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

        self.root = root
        self.line_list = []

    def update_canvas(self, lists, img_nr):

        print('image_nr:', img_nr)
        print(len(lists.mask_image_merge_list))
        self.canvas.imgref = lists.image_list[img_nr]
        self.canvas_2.imgref = lists.mask_list[img_nr]
        self.canvas_3.imgref = lists.mask_image_merge_list[img_nr]
        self.canvas.itemconfig(self.canvas_image, image=lists.image_list[img_nr])
        self.canvas_2.itemconfig(self.canvas_2_image, image=lists.mask_list[img_nr])
        self.canvas_3.itemconfig(self.canvas_3_image, image=lists.mask_image_merge_list[img_nr])
        for i in range(len(self.line_list)):
            line = self.line_list[i]
            self.canvas.itemconfig(line, state='hidden')

    def draw_initial_form(self, color, lab, label_dict_select_area, img_nr):

        def start_line(event):
            global select_area_coordinates_one_label
            global start_x
            global start_y
            select_area_coordinates_one_label = []
            self.canvas.old_cords = event.x, event.y
            self.root.unbind('<ButtonPress-1>')
            start_x = event.x
            start_y = event.y
            select_area_coordinates_one_label.append((start_x, start_y))

        def mouse_move(event):
            self.canvas.delete('line')
            x_live, y_live = self.canvas.old_cords
            line = self.canvas.create_line(x_live, y_live, event.x, event.y, width=1, fill=color, tags='line')
            self.line_list.append(line)

        def draw_line(event):

            global first_line
            x, y = event.x, event.y
            x1, y1 = self.canvas.old_cords
            end_x = x
            end_y = y
            distance_end_start = (((end_y - start_y) ** 2) + ((end_x - start_x) ** 2)) ** (1 / 2)

            if distance_end_start < 5 and first_line == False:
                line_1 = self.canvas.create_line(x1, y1, x, y, width=1, fill=color)
                line_2 = self.canvas.create_line(end_x, end_y, start_x, start_y, width=1,
                                                 fill=color)  # Frage: Spielt Anordnung von x1,y1,x,y eine rolle?
                self.line_list.append(line_1)
                self.line_list.append(line_2)
                self.root.unbind('<ButtonRelease-1>')
                self.root.unbind("<B1-Motion>")
                select_area_coordinates_one_label.append((end_x, end_y))

                saving_corner_coordinates('sel_area', select_area_coordinates_one_label, lab, label_dict_select_area, img_nr)

            else:
                line = self.canvas.create_line(x1, y1, x, y, width=1,
                                               fill=color)  # Frage: Spielt Anordnung von x1,y1,x,y eine rolle?
                self.line_list.append(line)
                self.canvas.old_cords = x, y
                first_line = False
                select_area_coordinates_one_label.append((x, y))

        self.root.bind('<ButtonPress-1>', start_line)
        self.root.bind("<B1-Motion>", mouse_move)
        self.root.bind('<ButtonRelease-1>', draw_line)

    def draw_forms(self, label_dict_select_area, img_nr, label_buttons):

        print('label_dict:', label_dict_select_area.dict)

        if img_nr in label_dict_select_area.dict.keys():
            for select_area_labels in label_dict_select_area.dict[img_nr].keys():
                for button_wrapper in label_buttons:
                    if button_wrapper.button['text'] == select_area_labels:
                        current_color = button_wrapper.button['fg']
                for area_corner_coords in range(len(label_dict_select_area.dict[img_nr][select_area_labels])):

                    for i in range(len(
                            label_dict_select_area.dict[img_nr][select_area_labels][area_corner_coords]) - 1):
                        corner1 = label_dict_select_area.dict[img_nr][select_area_labels][area_corner_coords][i]
                        corner2 = label_dict_select_area.dict[img_nr][select_area_labels][area_corner_coords][
                            i + 1]
                        line1 = self.canvas.create_line(corner1, corner2, width=1, fill=current_color, tag='line_1',
                                                        state='normal')
                        self.line_list.append(line1)
                    first_corner = label_dict_select_area.dict[img_nr][select_area_labels][area_corner_coords][
                        0]
                    last_corner = label_dict_select_area.dict[img_nr][select_area_labels][area_corner_coords][
                        -1]
                    print('lc', last_corner)
                    line2 = self.canvas.create_line(last_corner, first_corner, fill=current_color, tag='line_2',
                                                    state='normal')
                    self.line_list.append(line2)
        print('xxxx', self.line_list)                                                                                                                     
