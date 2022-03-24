import tkinter as tk


def saving_corner_coordinates(modus, coordinates, lab, label_dict_select_area, img_nr):
    '''This function saves the corner coordinates of the polygon at the right image number and label in the dictionary
     object label_dict_select_area from the class DictCoordinates()'''

    # This checks, if the modus is sel_area. One could draw for example rectangles, too. For that we would pass a
    # different modus into the function saving_corner_coordinates
    if modus == 'sel_area':
        # If the img_nr at which the polygon was drawn does not exist in label_dict_select_area.dict, a new key img_nr
        # with an empty dictionary as a value is initiated.
        if not img_nr in label_dict_select_area.dict.keys():
            label_dict_select_area.dict[img_nr] = {}
            # A new key for the label of the polygon is initiated with the corner coordinates of the polygon as the
            # value.
            label_dict_select_area.dict[img_nr][lab] = [coordinates]
        # If the image current image number, where the polygon was drawn already exists in label_dict_select_area.dict
        elif img_nr in label_dict_select_area.dict.keys():
            # If the label doesn't exist in label_dict_select_area.dict[img_nr], a new key for that label with value
            # of the corner coordinates of the polygon is initiated
            if not lab in label_dict_select_area.dict[img_nr].keys():
                label_dict_select_area.dict[img_nr][lab] = [coordinates]
            # If the label already exists in label_dict_select_area.dict[img_nr], the coordinates of the corners of the
            # polygon are simply appended to label_dict_select_area.dict[img_nr][lab]
            elif lab in label_dict_select_area.dict[img_nr].keys():
                label_dict_select_area.dict[img_nr][lab].append(coordinates)


class AllCanvas():
    '''Creating and updating the canvases with their images and polygons'''

    def __init__(self, root, lists, rspan, w, h):

        # Creating attributes self.w and self.h from width w and height h
        # Creating attribute self.root from root
        # Creating attribute self.line_list, where the lines in function draw_forms() will be added
        self.w = w
        self.h = h
        self.root = root
        self.line_list = []

        # Creating attribute self.sub_root, which is a frame on top of root
        self.sub_root = tk.Frame(root)
        # Placing self.sub_root at coordinate (0, 0) of the root. Self.sub_root has a width of rspan and a height of 10
        self.sub_root.grid(column=0, row=0, rowspan=rspan, columnspan=10)
        # Binding attribute self.canvas on self.sub_root width width self.w and height self.h
        self.canvas = tk.Canvas(self.sub_root, width=self.w, height=self.h)
        # Placing self.canvas at coordinate (0,0) of self.sub_root
        self.canvas.grid(column=0, row=0, rowspan=15)
        # Putting image on canvas from attribute image_list from object lists. The list index is 0 (First image in list)
        self.canvas_image = self.canvas.create_image(0, 0, anchor=tk.NW, image=lists.image_list[0])

        # From line 50-54, the same is done as in line 39-47, but for the mask
        self.sub_root_2 = tk.Frame(root)
        self.sub_root_2.grid(column=0, row=self.h, rowspan=int(rspan / 2), columnspan=8)
        self.canvas_2 = tk.Canvas(self.sub_root_2, width=int(self.w * 0.8), height=int(self.h * 0.8))
        self.canvas_2.grid(column=0, row=0)
        self.canvas_2_image = self.canvas_2.create_image(0, 0, anchor=tk.NW, image=lists.mask_list[0])

        # From line 57-61, the same is done as in line 39-47, but for the mask_image_merge
        self.sub_root_3 = tk.Frame(root)
        self.sub_root_3.grid(column=9, row=self.h, rowspan=int(rspan / 2), columnspan=8)
        self.canvas_3 = tk.Canvas(self.sub_root_3, width=int(self.w * 0.8), height=int(self.h * 0.8))
        self.canvas_3.grid(column=0, row=0, rowspan=15)
        self.canvas_3_image = self.canvas_3.create_image(0, 0, anchor=tk.NW, image=lists.mask_image_merge_list[0])


    def update_canvas(self, lists, img_number):
        '''Refreshing the canvases'''

        # Getting the current image number from the attribute img_number in the object img_number
        img_nr = img_number.img_number

        # Creating references to the images in canvas, canvas_2 and canvas_3 at the current image number img_nr
        self.canvas.imgref = lists.image_list[img_nr]
        self.canvas_2.imgref = lists.mask_list[img_nr]
        self.canvas_3.imgref = lists.mask_image_merge_list[img_nr]
        # Updating the images in the canvases with the updated attributes image_list, mask_list and
        # mask_image_merge_list from the object lists
        self.canvas.itemconfig(self.canvas_image, image=lists.image_list[img_nr])
        self.canvas_2.itemconfig(self.canvas_2_image, image=lists.mask_list[img_nr])
        self.canvas_3.itemconfig(self.canvas_3_image, image=lists.mask_image_merge_list[img_nr])

        # Looping through all the lines and updating their state to 'hidden'
        for i in range(len(self.line_list)):
            line = self.line_list[i]
            self.canvas.itemconfig(line, state='hidden')


    def draw_initial_form(self, color, lab, label_dict_select_area, img_nr):
        '''Drawing of the lines when labeling the images manually'''

        # Getting the current image number from the attribute img_number in the object img_number
        img_nr = img_nr.img_number

        def start_line(event):
            '''Starting the drawing of a line'''

            # These variables are global, because they need to be accessed from other functions (mouse_move, draw_line)
            global select_area_coordinates_one_label
            global start_x
            global start_y

            # This is an empty list, that will later be filled with the corner coordinates of the polygon
            select_area_coordinates_one_label = []
            # Changing attribute old_cords from canvas to the coordinates from event.x and event.y
            self.canvas.old_cords = event.x, event.y
            # Unbinding the function start_line from the mouse pressing
            self.root.unbind('<ButtonPress-1>')
            # Writing the x and y coordinates from event to start_x and start_y
            start_x = event.x
            start_y = event.y
            # Appending start_x and start_y to select_area_coordinates_one_label as a tuple
            select_area_coordinates_one_label.append((start_x, start_y))

        def mouse_move(event):
            '''Permanently updating the line, while moving the mouse in the image after the function start_line was
            initiated'''

            # Delete the line on the canvas
            self.canvas.delete('line')

            # Getting the coordinates x and y from self.canvas.old_cors and drawing a new line
            x_live, y_live = self.canvas.old_cords
            line = self.canvas.create_line(x_live, y_live, event.x, event.y, width=1, fill=color, tags='line')
            # Append line to self.line_list
            self.line_list.append(line)

        def draw_line(event):
            '''Drawing the finished line, after releasing the mouse button'''

            # Getting the x and y coordinates from event
            x, y = event.x, event.y
            # Getting coordinates from self.canvas.old_coordinates, which are the coordinates from the starting point of
            # the line
            x1, y1 = self.canvas.old_cords
            # Writing x and y to end_x and and_y
            end_x = x
            end_y = y
            # Calculating the length of the line from (start_x, start_y) to (end_x, end_y). This is the distance from
            # the current end point to the first point of the whole polygon
            distance_end_start = (((end_y - start_y) ** 2) + ((end_x - start_x) ** 2)) ** (1 / 2)

            # This if-else statement determines if the polygon drawing should be terminated and drawn, or if another
            # line shoud be added. If stande_end_start is smaller than 5 pixels, the drawing will be terminated
            if distance_end_start < 5:
                # Drawing the line on the canvas from the second last to the last point of the polygon and appending the
                # line to self.line_list
                line_1 = self.canvas.create_line(x1, y1, x, y, width=1, fill=color)
                self.line_list.append(line_1)

                # Drawing the line on the canvas from the last to the first point of the polygon and appending the line
                # to self.line_list
                line_2 = self.canvas.create_line(end_x, end_y, start_x, start_y, width=1, fill=color)
                self.line_list.append(line_2)

                # Unbinding the function draw_line from the mouse releasing and the function mouse_move from the the
                # mouse moving
                self.root.unbind('<ButtonRelease-1>')
                self.root.unbind("<B1-Motion>")

                # Appending the coordinates of the last point to the list select_are_coordinates_one_label
                select_area_coordinates_one_label.append((end_x, end_y))

                # The list select_are_coordinates_one_label is now full and we can call the function
                # saving_corner_coordinates
                saving_corner_coordinates('sel_area', select_area_coordinates_one_label, lab, label_dict_select_area, img_nr)

            else:
                line = self.canvas.create_line(x1, y1, x, y, width=1, fill=color)
                self.line_list.append(line)
                self.canvas.old_cords = x, y
                select_area_coordinates_one_label.append((x, y))

        # Binding the mouse pressing to the function start_line()
        self.root.bind('<ButtonPress-1>', start_line)
        # Binding the mouse moving to the function mouse_move()
        self.root.bind("<B1-Motion>", mouse_move)
        # Binding the mouse releasing to the funciton draw_line()
        self.root.bind('<ButtonRelease-1>', draw_line)


    def draw_forms(self, label_dict_select_area, img_nr, label_buttons):
        '''Drawing the polygons on canvas at position img_nr, in case we are still in the 'labeling by hand' mode'''

        # Getting the current image number from the attribute img_number in the object img_number
        img_nr = img_nr.img_number

        # Checking if img_nr is a key of label_dict_select_area
        if img_nr in label_dict_select_area.dict.keys():
            # Looping through all the labels in the dictionary at the current img_nr
            for select_area_labels in label_dict_select_area.dict[img_nr].keys():
                # Looping through all the buttons in the list object list label_buttons
                for button_wrapper in label_buttons:
                    # Checking, if the current label (pixel_number) is the label of the button
                    if button_wrapper.button['text'] == select_area_labels:
                        # Setting current_color to the color of the button
                        current_color = button_wrapper.button['fg']
                # Looping through all polygons at img_nr and that label
                for area_corner_coords in range(len(label_dict_select_area.dict[img_nr][select_area_labels])):
                    # Looping through each corner of the polygon
                    for i in range(len(label_dict_select_area.dict[img_nr][select_area_labels][area_corner_coords])
                                   - 1):
                        # Coordinates of the current corner and one corner ahead
                        corner1 = label_dict_select_area.dict[img_nr][select_area_labels][area_corner_coords][i]
                        corner2 = label_dict_select_area.dict[img_nr][select_area_labels][area_corner_coords][
                            i + 1]
                        # Create a ling from corner1 to corner2 on canvas in the color current_color we got at line 197
                        line1 = self.canvas.create_line(corner1, corner2, width=1, fill=current_color, tag='line_1',
                                                        state='normal')
                        # Append the line to self.line_list
                        self.line_list.append(line1)
                    # Do the same for the second last and last corners
                    first_corner = label_dict_select_area.dict[img_nr][select_area_labels][area_corner_coords][
                        0]
                    last_corner = label_dict_select_area.dict[img_nr][select_area_labels][area_corner_coords][
                        -1]
                    line2 = self.canvas.create_line(last_corner, first_corner, fill=current_color, tag='line_2',
                                                    state='normal')
                    self.line_list.append(line2)
