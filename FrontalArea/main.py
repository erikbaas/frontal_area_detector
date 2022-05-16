import utility
import areaDetection

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("...")
    print()
    utility.convertJPGtoNPY()
    print("...")
    print()
    print("Starting up the area detection algorithm! May take up to 10 seconds.")
    areaDetection.area_detection_by_color()
    print("...")
    print()
    print("Code ran successfully. .")


