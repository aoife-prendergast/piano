from adafruit_led_animation import helper

class PianoPixelMap(helper.PixelMap):
    def __init__(self, strip, pixel_ranges, individual_pixels=False):
        helper.PixelMap.__init__(strip, pixel_ranges, individual_pixels)

    key_a_pixel_map = [
        (3,4,9), 
        (2,5,8),
        (1,6,7)
    ]

    key_b_pixel_map = [
        (10,15,16), 
        (11,14,17),
        (12,13,18)
    ]

    key_c_pixel_map = [
        (21,22,27), 
        (20,23,26),
        (19,24,25)
    ]