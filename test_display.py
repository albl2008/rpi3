import epd5in65f as epd
import epdconfig
import time

try:
    # Create an instance of the display
    epd_instance = epd.EPD()
    # Initialize the display
    epd_instance.init()
    print("Display initialized successfully.")

    # Clear the display (sets all pixels to white)
    epd_instance.Clear()
    time.sleep(2)

    # Put the display to sleep
    epd_instance.sleep()
    print("Display put to sleep.")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    epdconfig.module_exit()  # Ensure GPIO is released
