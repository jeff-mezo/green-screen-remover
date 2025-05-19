import streamlit as st
import cv2
import numpy as np
import os

def remove_green_screen_video(video_path, background_image_path, output_video_path):
    cap = cv2.VideoCapture(video_path)
    
    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Read the background image
    background = cv2.imread(background_image_path)

    # Create VideoWriter to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'h264')  # Video codec (MP4)
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to HSV for green screen removal
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define the green color range
        lower_green = np.array([35, 43, 46])
        upper_green = np.array([89, 255, 255])

        # Create a mask for green pixels
        mask = cv2.inRange(hsv_frame, lower_green, upper_green)

        # Invert the mask to get the foreground
        foreground_mask = cv2.bitwise_not(mask)
        foreground = cv2.bitwise_and(frame, frame, mask=foreground_mask)

        # Resize the background to fit the frame size
        background_resized = cv2.resize(background, (frame.shape[1], frame.shape[0]))

        # Apply the background mask
        background_mask = cv2.bitwise_and(background_resized, background_resized, mask=mask)

        # Combine foreground and background
        result_frame = cv2.add(foreground, background_mask)

        # Write the processed frame to the output video
        out.write(result_frame)

    # Release resources
    cap.release()
    out.release()

    # Return the path of the output video
    if os.path.exists(output_video_path):
        print(f"Video processed successfully: {output_video_path}")
        return output_video_path
    else:
        print(f"Error: Output video was not created at {output_video_path}")
        return None
