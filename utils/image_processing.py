import cv2
import numpy as np
from PIL import Image

def remove_green_screen_image(image_path, background_image_path):
    # Read the input image and background image
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert input image to RGB

    background = cv2.imread(background_image_path)
    background_rgb = cv2.cvtColor(background, cv2.COLOR_BGR2RGB)  # Convert background to RGB

    # Define green color range for segmentation
    lower_green = np.array([35, 43, 46])  # Lower bound of green in HSV
    upper_green = np.array([89, 255, 255])  # Upper bound of green in HSV

    # Convert the input image to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Create a mask for green pixels in the image
    mask = cv2.inRange(hsv_image, lower_green, upper_green)

    # Invert the mask to get the foreground
    foreground_mask = cv2.bitwise_not(mask)
    foreground = cv2.bitwise_and(image_rgb, image_rgb, mask=foreground_mask)

    # Resize the background to match the input image size
    background_resized = cv2.resize(background_rgb, (image.shape[1], image.shape[0]))

    # Apply the mask to the resized background
    background_mask = cv2.bitwise_and(background_resized, background_resized, mask=mask)

    # Combine the foreground and background
    result = cv2.add(foreground, background_mask)

    # Convert the result back to PIL Image for Streamlit
    final_image = Image.fromarray(result)
    return final_image

