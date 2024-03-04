import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static


def read_csv_file(uploaded_file):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)
        return df
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        return None


def create_map(df):
    # Filter out rows with NaN values in Latitude or Longitude columns
    df = df.dropna(subset=['Latitude', 'Longitude'])

    # Create a folium map centered on the average coordinates of the data
    map_center = [df['Latitude'].mean(), df['Longitude'].mean()]
    my_map = folium.Map(location=map_center, zoom_start=10)

    # Add markers for each row in the DataFrame
    for index, row in df.iterrows():
        folium.Marker(location=[row['Latitude'], row['Longitude']],
                      popup=f"Row {index}").add_to(my_map)

    return my_map


def display_selected_columns(df, selected_columns):
    st.write("### Selected Columns Information")
    st.write(df[selected_columns])


def main():
    st.title('CSV Reader and Mapper App')

    # File uploader for CSV
    uploaded_file = st.file_uploader(
        "Upload a CSV file with Latitude and Longitude columns", type=["csv"])

    # Display uploaded data
    if uploaded_file is not None:
        st.sidebar.info(f"File uploaded: {uploaded_file.name}")

        # Read CSV file
        df = read_csv_file(uploaded_file)

        # Display DataFrame
        if df is not None:
            st.write("### Displaying Data from CSV")
            st.write(df)

            # Check if the required columns (Latitude and Longitude) are present
            if 'Latitude' in df.columns and 'Longitude' in df.columns:
                # Buttons to display latitude and longitude information
                if st.button("Show Latitude Information"):
                    st.write("### Latitude Information")
                    st.write(df['Latitude'])

                if st.button("Show Longitude Information"):
                    st.write("### Longitude Information")
                    st.write(df['Longitude'])

                # Section to display selected columns
                st.write("### Column Display Section")
                selected_columns = st.multiselect(
                    "Select columns to display", df.columns)
                if selected_columns:
                    display_selected_columns(df, selected_columns)

                # Map of Locations
                st.write("### Map of Locations")
                my_map = create_map(df)
                folium_static(my_map)
            else:
                st.warning(
                    "CSV file does not contain Latitude and Longitude columns. Add these columns for mapping.")


if __name__ == "__main__":
    main()
