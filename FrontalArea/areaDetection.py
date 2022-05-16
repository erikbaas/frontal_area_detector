import cv2
import numpy as np
import os
import time
import utility


def setParameters():
    # -- Empty function as fill parameter ---
    def empty(a):
        pass

    # --- Setting parameters for the settings & slider screen for color masking
    frameWidth = 640
    frameHeight = 480
    cap = cv2.VideoCapture(0)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    cv2.namedWindow("Color_Parameters")
    cv2.resizeWindow("Color_Parameters", 640, 240)  # Set size of the settings window
    cv2.createTrackbar("B_low", "Color_Parameters", 0, 255, empty)  # --- Note: ... initial guess, maxvalue, empty)
    cv2.createTrackbar("B_high", "Color_Parameters", 230, 255, empty)
    cv2.createTrackbar("G_low", "Color_Parameters", 0, 255, empty)
    cv2.createTrackbar("G_high", "Color_Parameters", 175, 255, empty)
    cv2.createTrackbar("R_low", "Color_Parameters", 0, 255, empty)
    cv2.createTrackbar("R_high", "Color_Parameters", 175, 255, empty)

    # --- Setting parameters for settings & slider screen
    frameWidth = 640
    frameHeight = 480
    cap = cv2.VideoCapture(0)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    cv2.namedWindow("Noise_Parameters")
    cv2.resizeWindow("Noise_Parameters", 640, 240)  # Set size of settings window
    cv2.createTrackbar("nr_dilations", "Noise_Parameters", 1, 3, empty)
    cv2.createTrackbar("AreaMin", "Noise_Parameters", 400, 40000, empty)
    cv2.createTrackbar("AreaMax", "Noise_Parameters", 30000, 40000, empty)


def area_detection_by_color():
    # --- Load in images. If not loaded, recommend user to run the main script first.
    if os.path.isfile('data/photos.npy'):
        images = np.load('data/photos.npy', allow_pickle=True)
    else:
        print("Please use the main script once to convert jpgs to npy")

    setParameters()

    # --- Settings for Dilation to remove Noise. The higher the kernel the larger the expansion per step
    kernel = np.ones((1, 1))

    # Scan through all fotos
    for i in range(len(images)):
        live_image = images[i]
        # Make a copy to draw on
        imgContour = live_image.copy()

        # Contrasting and blurring the photos
        imgContrast = cv2.addWeighted(live_image, 1, live_image, 0, 0)      # Add contrast to photo
        imgContrast = cv2.addWeighted(imgContrast, 1, imgContrast, 0, 0)      # Add contrast to photo
        imgBilateral = cv2.bilateralFilter(imgContrast, 4, 75, 75)          # 2nd arg determines amount of blur

        # Retrieve all variables fro the trackbar
        B_low = cv2.getTrackbarPos("B_low", "Color_Parameters")
        B_high = cv2.getTrackbarPos("B_high", "Color_Parameters")
        G_low = cv2.getTrackbarPos("G_low", "Color_Parameters")
        G_high = cv2.getTrackbarPos("G_high", "Color_Parameters")
        R_low = cv2.getTrackbarPos("R_low", "Color_Parameters")
        R_high = cv2.getTrackbarPos("R_high", "Color_Parameters")
        low_color = np.array([B_low, G_low, R_low])
        high_color = np.array([B_high, G_high, R_high])

        # Convert to UINT8 as opencv functions don't allow otherwise
        imgPreMask = (imgBilateral * 255).astype(np.uint8)

        # Perform the masking
        imgMask = cv2.inRange(imgPreMask, low_color, high_color)

        # Get Canny parameters from settings slider
        nr_dilations = cv2.getTrackbarPos("nr_dilations", "Noise_Parameters")

        # --- Start timer to measure execution speed
        # e1 = cv2.getTickCount()
        # Dilate image once to make contour tracking easier.
        imgDil = cv2.dilate(imgMask, kernel, iterations=nr_dilations)
        # e2 = cv2.getTickCount()
        # time = (e2 - e1) / cv2.getTickFrequency()
        # print("Time for dilation: ", time)
        # ---  Stop timer to measure execution speed^

        # Call the custom contour function
        colorful = True
        if colorful:
            print("NB: looking at color detection!")
            get_contours(imgDil, imgContour, i)
        else:
            print("NB: counting the white pixels!")
            get_contours_white(imgDil, imgContour, i)

        # Displaying the results side to side with custom utility function
        StackedImages = utility.stackImages(([live_image, imgContrast, imgBilateral],
                                             [imgMask, imgDil, imgContour]), 0.6)
        cv2.imshow("Stacked Images", StackedImages)

        # Wait for enter press to continue
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # time.sleep(0.1)       # ALTERNATIVE to the wait key: playing it slowly
        cv2.waitKey(0)


# ---- Function to get contours ----
def get_contours(img, imgContour, i):

    # Use built in contour function
    extra_variable, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    areas_in_one_image = []
    for cnt in contours:
        # Calculate Area
        area = cv2.contourArea(cnt)
        # Load in your set min and max area
        areaMin = cv2.getTrackbarPos("AreaMin", "Noise_Parameters")
        areaMax = cv2.getTrackbarPos("AreaMax", "Noise_Parameters")
        # Check if area is large enough to be part of the object
        if areaMin < area < areaMax:
            areas_in_one_image.append(area)
            cv2.drawContours(imgContour, cnt, -1, (100, 0, 255), 2)         # Contour drawn in pink
            peri = cv2.arcLength(cnt, True)                                 # Calculate how long the perimeter is

            # # Draw rectangle around shape
            approx = cv2.approxPolyDP(cnt, 0.01 * peri, closed=True)        # Approximates the shape of the perimeter
            x, y, w, h = cv2.boundingRect(approx)
            # cv2.rectangle(imgContour, (x,y), (x+w, y+h), (0, 255, 0), 1)      # Draws box around contours

            # Put text around shapes
            cv2.putText(imgContour, "Points: " + str(len(approx)), (x + 0, y + h + 40), cv2.FONT_HERSHEY_COMPLEX,
                        .7, (0,255,0), 2)
            cv2.putText(imgContour, "Areas: " + str(int(area)), (x + 0, y + h + 20), cv2.FONT_HERSHEY_COMPLEX,
                        .7, (0,255,0), 2)

    if len(areas_in_one_image) == 2:  # If two areas are detected it means one is the reference and the other the drone
        print("Two areas detected! Assuming the smallest area is the reference area...")
        A_m2 = convert_area(areas_in_one_image)
        print(f"The drone frontal area is: {A_m2} m^2")


# ---- Function to get contours and count whites ----
def get_contours_white(img, imgContour, i):

    # Calculate Area
    number_of_black_pix = cv2.countNonZero(img)
    number_of_pix = 320*335
    print("num of black pix is: ", number_of_black_pix)
    print("total num of pix is: ", number_of_pix)
    print(f"percentage black is: {round(100*number_of_black_pix/ number_of_pix,2)} percent")

    # Put text around shapes
    cv2.putText(imgContour, "nr blck pix: " + str(int(number_of_black_pix)), (10, 40), cv2.FONT_HERSHEY_COMPLEX,
                .7, (0,255,0), 2)
    cv2.putText(imgContour, "nr white pix: " + str(int(number_of_pix-number_of_black_pix)), (10, 20), cv2.FONT_HERSHEY_COMPLEX,
                .7, (0,255,0), 2)

def convert_area(areas):
    A_ref_px = min(areas)
    A_ref_m2 = 5.72*15.56/10000  # Coca cola frontal A
    A_px = max(areas)
    A_m2 = (A_px / A_ref_px) * A_ref_m2
    return A_m2