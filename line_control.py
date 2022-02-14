


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