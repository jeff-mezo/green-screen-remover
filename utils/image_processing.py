import cv2
import numpy as np
from PIL import Image

def remove_green_screen_image(image_path, background_image_path):
    # read input from user
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # convert to RGB

    background = cv2.imread(background_image_path)
    background_rgb = cv2.cvtColor(background, cv2.COLOR_BGR2RGB)  # convert to RGB

    # define the green color space for the green-screen selection
    lower_green = np.array([35, 43, 46])  # Lower bound of green in HSV
    upper_green = np.array([89, 255, 255])  # Upper bound of green in HSV

    # convert image to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # create a mask of the green color range
    mask = cv2.inRange(hsv_image, lower_green, upper_green)

    # invert the mask to select non-green areas
    foreground_mask = cv2.bitwise_not(mask)
    foreground = cv2.bitwise_and(image_rgb, image_rgb, mask=foreground_mask)

    # resize the background to match the input image size
    background_resized = cv2.resize(background_rgb, (image.shape[1], image.shape[0]))

    # apply the mask to the resized background
    background_mask = cv2.bitwise_and(background_resized, background_resized, mask=mask)

    # combine the foreground and background
    result = cv2.add(foreground, background_mask)

    # convert the result back to PIL Image for Streamlit
    final_image = Image.fromarray(result)
    return final_image

