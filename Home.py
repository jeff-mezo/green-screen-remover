import streamlit as st

# Title of the app
st.title("Green Screen Remover App")

# Provide navigation options to the user
st.markdown("""
    Remove the background of your green screen images or videos and overlay them over another image using this app. 
    #### Select an Option:
    - **[Image Processing](pages/1_📷_Image_Chroma_Key)**: Remove green screen from images.
    - **[Video Processing](pages/2_🎥_Video_Chroma_Key)**: Remove green screen from videos.
    ## Media Player:
""")

video_file =  st.file_uploader("Upload your video", type=["mp4", "mov", "avi"])

if video_file:
    st.video(video_file)


st.markdown("Made by: Jeffer John P. Mezo")






