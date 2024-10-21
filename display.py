import sys
import time
from PIL import Image
import epd5in65f as epd
import epdconfig
from threading import Lock

# Initialize global resources
epd_instance = epd.EPD()
epd_instance.init()
lock = Lock()

def show(image_path: str):
    with lock:  # Ensure that only one thread accesses this block at a time
        try:
            epd_instance.Clear()
            time.sleep(2)

            image = Image.open(image_path)
            image = image.resize((epd_instance.width, epd_instance.height))
            buf = epd_instance.getbuffer(image)

            epd_instance.display(buf)
            time.sleep(5)
            epd_instance.sleep()

        except IOError as e:
            print(e)

        except KeyboardInterrupt:
            epdconfig.module_exit()
            exit()

if __name__ == '__main__':
    # Ensure the script is called with the correct number of arguments
    if len(sys.argv) != 2:
        print("Usage: python display.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]  # Get the image path from command line arguments
    show(image_path)  # Call the show function with the provided image path

