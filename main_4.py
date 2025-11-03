import machine
import neopixel
import math
import time

STRIP1_NUM_PIXELS = 11 + 10 + 10
STRIP1_PIN_NUM = 2
DELAY_MS = 35
STRIP1_MAX_BRIGHTNESS = 125
STRIP1_PAD_WITH_X_ZEROS = 100

strip1 = neopixel.NeoPixel(machine.Pin(STRIP1_PIN_NUM), STRIP1_NUM_PIXELS)

def create_sine_table(length, max):
    sine_table = []
    for i in range(length):
        # Calculate sine value (0 to 2π)
        value = math.sin(2 * math.pi * i / length)
        # Convert to 0-255 range
        byte_value = int((value + 1) * max / 2)
        sine_table.append(byte_value)
    return sine_table

def create_pixel_offset():
    pixel_offset = []
    for i in range(5):
        pixel_offset.append(0)
    for i in range(5):
        pixel_offset.append(85)
    for i in range(5):
        pixel_offset.append(85)
    for i in range(6):
        pixel_offset.append(170)
    for i in range(5):
        pixel_offset.append(170)
    for i in range(5):
        pixel_offset.append(0)
    return pixel_offset

def add_zeros(input_list, num_zeros):
    try:
        first_zero_index = input_list.index(0)
    except ValueError:
        min_value = min(input_list)
        first_zero_index = input_list.index(min_value)
    
    for _ in range(num_zeros):
        input_list.insert(first_zero_index, 0)
    return input_list
    
def set_next_strip_value(strip, sine_table, pixel_offsets):
    for pixel in range(len(strip)):
        offset = pixel_offsets[pixel]
        if offset >= len(sine_table):
            offset -= len(sine_table)
        value = sine_table[offset]
        pixel_offsets[pixel] = offset + 1
        strip[pixel] = (value, value, value)
    strip.write()

def cleanup():
    strip1.fill((0, 0, 0))
    strip1.write()

strip1_sine_table = create_sine_table(length=256, max=STRIP1_MAX_BRIGHTNESS)
strip1_sine_table = add_zeros(strip1_sine_table, num_zeros=STRIP1_PAD_WITH_X_ZEROS)
strip1_pixel_offsets = create_pixel_offset()
# strip1_pixel_order = create_random_pixel_order(num_pixels=STRIP1_NUM_PIXELS)

print("STRIP1 CONFIGURATION")
print(strip1_sine_table)
print(max(strip1_sine_table), min(strip1_sine_table))
print(strip1_pixel_offsets)

def glow(wait_ms=DELAY_MS):
    try:
        while True:
            set_next_strip_value(strip1, strip1_sine_table, strip1_pixel_offsets)
            # print("Pixel 0 value:", strip1[0], "Pixel 10 value:", strip1[10], "Pixel 20 value:", strip1[20], "Pixel 30 value:", strip1[30])
            time.sleep_ms(wait_ms)
    except Exception as e:
        cleanup()
        raise

def main():
    try:
        cleanup()
        glow()    
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
    finally:
        cleanup()
        
if __name__ == "__main__":
    main()
