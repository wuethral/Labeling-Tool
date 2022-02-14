from automated_masking import automated_masking
from windows import window_pixel_assignement, window_labeling_tool

if __name__ == '__main__':
    # Defining the tkinter root
    get_pixel_value = window_pixel_assignement()
    pixel_value = get_pixel_value.pixel_value

    if pixel_value > 0 and pixel_value <= 255:
        automated_masking(pixel_value)
    pixel_value = 248
    window_labeling_tool(pixel_value)