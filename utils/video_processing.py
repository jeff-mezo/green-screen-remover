import streamlit as st
import cv2
import numpy as np
import os

def remove_green_screen_video(video_path, background_image_path, output_video_path):
    cap = cv2.VideoCapture(video_path)
    
    # get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # read the background image
    background = cv2.imread(background_image_path)

    # create VideoWriter to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'h264')  # Video codec (h264 = .mp4), using mp4a causes problems in Streamlit playback
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # convert frame to HSV for green screen removal
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # define the green color range
        lower_green = np.array([35, 43, 46])
        upper_green = np.array([89, 255, 255])

        # create a mask for green pixels
        mask = cv2.inRange(hsv_frame, lower_green, upper_green)

        # invert the mask to get the foreground
        foreground_mask = cv2.bitwise_not(mask)
        foreground = cv2.bitwise_and(frame, frame, mask=foreground_mask)

        # resize the background to fit the frame size
        background_resized = cv2.resize(background, (frame.shape[1], frame.shape[0]))

        # apply the background mask
        background_mask = cv2.bitwise_and(background_resized, background_resized, mask=mask)

        # combine foreground and background
        result_frame = cv2.add(foreground, background_mask)

        # write the processed frame to the output video
        out.write(result_frame)

    # release resources
    cap.release()
    out.release()

    # return the path of the output video
    if os.path.exists(output_video_path):
        print(f"Video processed successfully: {output_video_path}")
        return output_video_path
    else:
        print(f"Error: Output video was not created at {output_video_path}")
        return None
