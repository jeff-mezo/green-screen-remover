import streamlit as st
from utils.image_processing import remove_green_screen_image
from io import BytesIO

# Title for the page
st.title("Green Screen Remover for Images")

# Upload an image with green screen and background
st.markdown("#### Upload Green Screen Image:")
uploaded_image = st.file_uploader("", type=["jpg", "png", "jpeg"])

st.markdown("#### Upload Background Image:")
uploaded_background_image = st.file_uploader(" ", type=["jpg", "png", "jpeg"])

col1, col2 = st.columns(2)

if uploaded_image:
    with col1:
        st.image(uploaded_image, caption="Image with Green Screen", use_container_width=True)

if uploaded_background_image:
    with col2:
        st.image(uploaded_background_image, caption="Background Image", use_container_width=True)


if uploaded_image is not None and uploaded_background_image is not None:

    start_image_processing = st.button("Start Image Processing")
    
    # Save uploaded files to local directory
    if start_image_processing:
        image_path = 'images/uploaded_image.jpg'
        background_image_path = 'images/background_image.jpg'

        with open(image_path, "wb") as f:
            f.write(uploaded_image.getbuffer())

        with open(background_image_path, "wb") as f:
            f.write(uploaded_background_image.getbuffer())

        # Process the image to remove the green screen
        result_image = remove_green_screen_image(image_path, background_image_path)

        # Convert the processed image to a byte stream for download
        img_byte_arr = BytesIO()
        result_image.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)

        # Show the result
        st.image(result_image, caption="Image with Removed Green Screen", use_container_width=True)

        # Provide download button for the processed image
        st.download_button(
            label="Download Processed Image",
            data=img_byte_arr,
            file_name="processed_image.png",
            mime="image/png"
        )
    