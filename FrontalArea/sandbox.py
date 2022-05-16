# import utility
# import os
# import numpy as np
# import cv2

# # Practicing the kruistabel.
#
# a_can = 5.72 * 15.56 / 10000
# a = 11.02 * a_can / 1.49
#
# print(a)

# How to find the large and small value in a list
# opps = [4,9]
#
# klein = min(opps)
# groot = max(opps)
#
# print(klein)


# if os.path.isfile('data/photos.npy'):
#     images = np.load('data/photos.npy', allow_pickle=True)
# else:
#     print("Please use the main script once to convert jpgs to npy")
#
# # Start timer to measure execution speed
# e1 = cv2.getTickCount()
#
# for i in range(len(images)):
#     live_image = images[i]
#     live_image = cv2.GaussianBlur(live_image, (7, 7), 1)
#
# # Stop timer to measure execution speed
# e2 = cv2.getTickCount()
# time = (e2 - e1) / cv2.getTickFrequency()
# print("Time for npy arrays: ", time)
#
# # Leaving them as images.
#
#
# input("press enter to continue")
#
#
# folder = "data/photos"
#
# images = []
#
# for filename in os.listdir(folder):
#     img = cv2.imread(os.path.join(folder,filename))
#     if img is not None:
#         images.append(img)
#
# # Start timer to measure execution speed
# e1 = cv2.getTickCount()
#
# for i in range(1,len(images)):
#     live_image = images[i]
#     live_image = cv2.GaussianBlur(live_image, (7, 7), 1)
#
# # Stop timer to measure execution speed
# e2 = cv2.getTickCount()
# time = (e2 - e1) / cv2.getTickFrequency()
# print("Time for images: ", time)


# print("string {}", int(9))
#
#
# print('String_nr_'+str(9))

# f = open("data/Gates_Csv/cornersFound.csv", "w")
# f.truncate()
# f.close()

# # List of strings
# row_contents = [2,9]
# # Append a list as new line to an old csv file
# utility.append_list_as_row('data/Gates_Csv/cornersFound.csv', row_contents)