from automated_masking import automated_masking
from windows import window_pixel_assignement, window_labeling_tool

if __name__ == '__main__':

    # Calling function window_pixel_assignment, which returns an object (get_pixel_value), which contains the pixel
    # value (label) for the function automated_masking.
    get_pixel_value = window_pixel_assignement()

    # Accessing the attribute pixel_value from object get_pixel_value, which contains the label (pixel value for masks)
    pixel_value = get_pixel_value.pixel_value

    # If the attribute automated_masking form the object get_pixel_value is True, then the automated masking is executed
    if get_pixel_value.automated_masking:
        automated_masking(pixel_value)

    # Calling function window_labeling_tool and passing the variable pixel_value
    window_labeling_tool(pixel_value)