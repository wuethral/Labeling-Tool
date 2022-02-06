import tkinter as tk
from tkinter import messagebox


class Ok():

    def __init__(self, window, t1):
        self.window = window
        self.t1 = t1
        self.pixel_value = 0

    def ok(self):
        self.pixel_value = int(self.t1.get())
        if self.pixel_value >= 1 and self.pixel_value <= 255:
            messagebox.showinfo(title='Pixel Assingment', message='Successful pixel assignment')
            self.window.destroy()
        else:
            messagebox.showerror(title='Pixel Assingment', message='Pixel out of range')

    def already_assigned(self):
        self.pixel_value = 9999999999
        self.window.destroy()


def window_pixel_assignement():
    window = tk.Tk()
    window.title('Assign pixel value to mask (Label):')
    window.geometry('400x500')

    l1 = tk.Label(window, text='Choose for 1-255:', font=(14))
    l1.grid(row=0, column=0, padx=5, pady=5)
    entry_pixel = tk.StringVar()
    t1 = tk.Entry(window, textvariable=entry_pixel, font=(14))
    t1.grid(row=0, column=1)
    get_pixel_value = Ok(window, t1)
    b1 = tk.Button(window, command=lambda: get_pixel_value.ok(), text='Ok', font=(14))
    b1.grid(row=2, column=1)
    b2 = tk.Button(window, command=lambda: get_pixel_value.already_assigned(), text='Already Done', font=(14))
    b2.grid(row=3, column=1)

    window.mainloop()
    return get_pixel_value