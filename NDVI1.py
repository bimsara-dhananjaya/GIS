import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def calculate_ndvi(red_image, nir_image):
    """Calculates the NDVI from red and NIR image arrays."""
    return (nir_image.astype(np.float32) - red_image.astype(np.float32)) / \
           (nir_image.astype(np.float32) + red_image.astype(np.float32))


def display_ndvi(ndvi_image, water_mask):
    """Displays the NDVI image with water body mask using Matplotlib."""
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    # Display NDVI image
    cax1 = ax[0].imshow(ndvi_image, cmap="RdYlGn", vmin=-1, vmax=1)
    ax[0].set_title('NDVI Image')
    fig.colorbar(cax1, ax=ax[0], label='NDVI Value')

    # Display water mask
    cax2 = ax[1].imshow(water_mask, cmap="Blues", vmin=0, vmax=1)
    ax[1].set_title('Water Body Mask')
    fig.colorbar(cax2, ax=ax[1], label='Water Probability')

    st.pyplot(fig)


def detect_water(ndvi_image, threshold=0.1):
    """Detects water bodies using a threshold on NDVI values."""
    water_mask = np.where(ndvi_image < threshold, 1, 0)
    return water_mask


def main():
    st.title("Water Body Detection with NDVI")

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

            # Detect water bodies
            water_mask = detect_water(ndvi_image)

            # Display results
            st.subheader("NDVI and Water Body Detection")
            display_ndvi(ndvi_image, water_mask)

        except Exception as e:
            st.error(f"Error processing GeoTIFF files: {e}")


if __name__ == '__main__':
    main()
