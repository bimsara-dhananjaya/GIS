import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def calculate_ndvi(red_image, nir_image):
    """Calculates the NDVI from red and NIR image arrays."""
    return (nir_image.astype(np.float32) - red_image.astype(np.float32)) / \
           (nir_image.astype(np.float32) + red_image.astype(np.float32))


def segment_landcover(ndvi_image, veg_threshold=0.2, water_threshold=-0.1):
    """Segments land cover based on NDVI values."""
    vegetation_mask = np.where(ndvi_image > veg_threshold, 1, 0)
    water_mask = np.where(ndvi_image < water_threshold, 1, 0)
    soil_mask = np.logical_and(
        ndvi_image <= veg_threshold, ndvi_image >= water_threshold)

    return vegetation_mask, water_mask, soil_mask


def display_landcover(ndvi_image, vegetation_mask, water_mask, soil_mask):
    """Displays the NDVI image and segmented land cover using Matplotlib."""
    fig, ax = plt.subplots(1, 4, figsize=(16, 6))

    # Display NDVI image
    cax1 = ax[0].imshow(ndvi_image, cmap="RdYlGn", vmin=-1, vmax=1)
    ax[0].set_title('NDVI Image')
    fig.colorbar(cax1, ax=ax[0], label='NDVI Value')

    # Display vegetation mask
    cax2 = ax[1].imshow(vegetation_mask, cmap="Greens", vmin=0, vmax=1)
    ax[1].set_title('Vegetation Mask')
    fig.colorbar(cax2, ax=ax[1], label='Vegetation Probability')

    # Display water mask
    cax3 = ax[2].imshow(water_mask, cmap="Blues", vmin=0, vmax=1)
    ax[2].set_title('Water Mask')
    fig.colorbar(cax3, ax=ax[2], label='Water Probability')

    # Display soil mask
    cax4 = ax[3].imshow(soil_mask, cmap="Reds", vmin=0, vmax=1)
    ax[3].set_title('Soil Mask')
    fig.colorbar(cax4, ax=ax[3], label='Soil Probability')

    st.pyplot(fig)


def main():
    st.title("Land Cover Segmentation with NDVI")

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

            # Segment land cover
            vegetation_mask, water_mask, soil_mask = segment_landcover(
                ndvi_image)

            # Display results
            st.subheader("NDVI and Land Cover Segmentation")
            display_landcover(ndvi_image, vegetation_mask,
                              water_mask, soil_mask)

        except Exception as e:
            st.error(f"Error processing GeoTIFF files: {e}")


if __name__ == '__main__':
    main()
