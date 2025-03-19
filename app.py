# imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# set up our app
st.set_page_config(page_title="Data sweeper", layout="wide")
st.title("Data aweeper")
st.write("Transfrom your files brtween CSV and Excel formats with built-in  data clean and visualization! ")


upload_files = st.file_uploader("Upload your files(CSV or Excel):", type=["csv","xlsx"], accept_multiple_files=True)

if upload_files:
    for file in upload_files:
        file_ext = os.path.splitext(file.name) [-1].lower()


        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}" )    
            continue   

        # Dislay info about the file
        st.write(f"**File Name:**{file.name}")
        st.write(f"**File Size**{file.size/1024}")

        # Show 5 rows of our df
        st.write("Preview the Head of the Dataframe")
        st.dataframe(df.head())

        # OPtions for Data Clining
        st.subheader("Data cleaning Option")
        if st.checkbox(f"clean data from {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates From {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicate removes!") 
            with col2:
                if st.button(f"Fill Missing Value for {file.name}"):
                    numaric_cols = df.select_dtypes(include=['number']).columns
                    df[numaric_cols] = df[numaric_cols].fillna(df[numaric_cols].mean())
                    st.write("Missing Values have been Filled!")
        # Choose Specific columns to keep or Convert
        st.subheader("Select Columns to Convert")
        columns = st.multiselect(f"Choose columns fro {file.name}", df.columns, default=df.columns)
        df = df[columns]  


        # Crete Some Visulizations
        st.subheader("Data visulization")
        if st.checkbox(f"Show visulization for {file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:,:2])


        # convert the File -> Svg To Excel
        st.subheader("Conversion Option")
        conversion_type = st.radio(f"Convert {file.name} to :", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert  {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"


            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)



            # Download Buton
            st.download_button(
                label = f"Download {file.name} as {conversion_type}",
                data= buffer,
                file_name = file_name,
                mime = mime_type
            )
st.success("All Files processed")
            

