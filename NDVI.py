import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def calculate_ndvi(red_image, nir_image):
    """Calculates the NDVI from red and NIR image arrays."""
    return (nir_image.astype(np.float32) - red_image.astype(np.float32)) / \
           (nir_image.astype(np.float32) + red_image.astype(np.float32))


def display_ndvi(ndvi_image):
    """Displays the NDVI image using Matplotlib."""
    fig, ax = plt.subplots()
    cax = ax.imshow(ndvi_image, cmap="RdYlGn", vmin=-1, vmax=1)
    fig.colorbar(cax, label='NDVI Value')
    st.pyplot(fig)


def main():
    st.title("NDVI Calculator")

    # File upload section
    red_image_file = st.file_uploader(
        "Upload Red Band Image (TIF)", type="tif")
    nir_image_file = st.file_uploader(
        "Upload NIR Band Image (TIF)", type="tif")

    if red_image_file is not None and nir_image_file is not None:
        try:
            red_image = np.array(Image.open(red_image_file))
            nir_image = np.array(Image.open(nir_image_file))

            # Calculate NDVI
            ndvi_image = calculate_ndvi(red_image, nir_image)

            # Display results
            st.subheader("NDVI Image")
            display_ndvi(ndvi_image)

            # Optionally display NDVI statistics
            st.subheader("NDVI Statistics")
            st.write("Minimum:", np.min(ndvi_image))
            st.write("Maximum:", np.max(ndvi_image))
            st.write("Mean:", np.mean(ndvi_image))

        except Exception as e:
            st.error(f"Error processing GeoTIFF files: {e}")


if __name__ == '__main__':
    main()
