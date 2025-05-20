import streamlit as st
from utils.video_processing import remove_green_screen_video

# title
st.title("Green Screen Remover for Videos")

# upload a video with green screen and background image
uploaded_video = st.file_uploader("Upload a video with green screen", type=["mp4", "avi"])
uploaded_video_background = st.file_uploader("Upload background image for video", type=["jpg", "png"])

col1, col2 = st.columns(2)

if uploaded_video is not None:
    with col1:
        st.video(uploaded_video, autoplay=True, muted=True, loop=True)
        st.markdown("Video with Green Screen")

if uploaded_video_background is not None:
    with col2:
        st.image(uploaded_video_background, caption="Background Image", use_container_width=True)

if uploaded_video is not None and uploaded_video_background is not None:
    
    start_video_processing = st.button("Start Video Processing")
    
    # save uploaded files to local directory
    if start_video_processing:
        # save uploaded files to local directory
        video_path = 'videos/uploaded_video.mp4'
        video_background_path = 'images/video_background_image.jpg'

        with open(video_path, "wb") as f:
            f.write(uploaded_video.getbuffer())

        with open(video_background_path, "wb") as f:
            f.write(uploaded_video_background.getbuffer())

        # output video path
        output_video_path = 'videos/output_video.mp4'

        # show loading spinner while processing the video
        with st.spinner('Processing video...'):
            # call the function to process the video and remove the green screen
            remove_green_screen_video(video_path, video_background_path, output_video_path)

        # after processing, show the processed video
        st.success("Video processed successfully!")
        # display the path where the video is saved
        st.video(output_video_path)