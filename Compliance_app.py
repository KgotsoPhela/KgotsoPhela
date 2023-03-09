# tfguh
# Streamlit dependencies
import streamlit as st
import joblib, os
import pandas as pd
import numpy as np
import pickle 
import re
import string
from skimage import io
import cv2
from skimage.transform import resize
import os
#from skimage.io import imread
#from sklearn.feature_extraction.text import CountVectorizer
#from nltk.tokenize import word_tokenize
#from nltk.stem.wordnet import WordNetLemmatizer
import matplotlib.pyplot as plt
import tensorflow as tf
#from wordcloud import WordCloud
import base64
from skimage import io, transform
from PIL import Image
from io import BytesIO
from zipfile import ZipFile
import seaborn as sns

import pickle

with open('C:/Users/KgotsoPhela(LubanziI/Downloads/Lubanzi prjs/Pics/Compliance/model.pkl', 'rb') as f:
    model = pickle.load(f)







                                            # PREDICTIONS



                                      # CREATE CONTAINERS
#tittle_and_welcome = st.container()
#image_input = st.container()
#folder_input = st.container()
#image_visuals = st.container()
#folder_visuals = st.container()
#predictions = st.container()


                                        # OUR PAGE TITTLE


# Set the background color of the app
#st.set_page_config(page_title="My Streamlit App", page_icon=":smiley:", layout="wide", initial_sidebar_state="expanded", background_color="#87CEFA")

#name = st.sidebar.text_input('Compliance App')

import streamlit as st

# Create a text input widget in the sidebar
#name = st.sidebar.text_input('Compliance App')
st.markdown("<h1 style='text-align: center; background-color: orange;'>Non Compliance Detector</h1>", unsafe_allow_html=True)
p = st.sidebar.markdown("<h1 style='text-align: center;'>SELECT PAGES BELOW</h1>", unsafe_allow_html=True)
#slid = st.sidebar.slider(' ', 1, 0)
wrk = st.sidebar.checkbox('**My Compliance Page**')
about = st.sidebar.checkbox('**About Us Page**')
#st.che
if wrk:


    # Create a header in the main section of the app
    #st.markdown("<h1 style='text-align: center; background-color: orange;'>Non Compliance Detector</h1>", unsafe_allow_html=True)

    st.write('  ')

    # Load the model and run the prediction
    with open('C:/Users/KgotsoPhela(LubanziI/Downloads/Lubanzi prjs/Pics/Compliance/model.pkl', 'rb') as f:
        model = pickle.load(f)



    #tt = st.markdown("<h2 style = 'text-align: center';>Click to upload images</h2>", unsafe_allow_html=True)
    #tt = st.markdown("<h1 style = 'text-align: center';>Non Compliance Detector</h1>", unsafe_allow_html=True)



    with st.expander("**Click to upload images**"):
        # Create a file uploader that is meant to take in zipped folders 
        multi_upload = st.file_uploader("Upload zipped files", accept_multiple_files=True)

    # Unzip or extract the contents of the folder
    if multi_upload is not None and len(multi_upload) > 0:


        with st.expander('**View Uploaded Images and Detected Classes**'):

            results = []
            folders = []

            n = st.number_input('**Select Grid Width**', 1, 5, 3)
            visualise_folders = st.button('Classify and View Uploads')
            if visualise_folders:
                for zipped_file in multi_upload:
                    with ZipFile(zipped_file) as zip:
                        zip.extractall()
                        folders.append(zipped_file.name.split('.')[0])
                        
                #Classify the images in each folder
                for folder in folders:
                    st.subheader(folder)

                    files = [f for f in os.listdir(folder) if f.endswith(".JPG") or f.endswith(".PNG") or f.endswith(".jpg") or f.endswith("png")]

                    # Display the images in columns according to the grid width
                    for i in range(0, len(files), n):

                        cols = st.columns(n)
                        for j in range(n):
                            if i + j < len(files):
                                file = files[i+j]
                                img_path = os.path.join(folder, file)
                                np_img = np.array(Image.open(img_path).convert('RGB').resize((256, 256)))
                                yhat = model.predict(tf.expand_dims(np_img, 0))
                                #st.dataframe(yhat)
                                pred_class = '**Seat Belt On**' if yhat > 0.5 else '**Seat Belt Off**'
                                color = 'green' if yhat > 0.5 else 'red'

                                with cols[j]:
                                    st.write(f'<span style="color:{color}">{pred_class}</span>', unsafe_allow_html=True)
                                    st.image(np_img, caption=None, use_column_width=True)




                                    # OUTCOME VISUALISATION, TABLE STATS



        with st.expander('**Outcomes Summary Table**'):

            # Create empty lists to store the results
            #st.write('**Stats Table**')
            reg_numbers = []
            seat_belt_on_counts = []
            seat_belt_off_counts = []

            # Loop through each folder
            for folder in folders:
                # Get the registration number from the folder name
                reg_number = folder.split('_')[0]
                reg_numbers.append(reg_number)

                # Count the number of images classified as seat belt on and seat belt off
                seat_belt_on_count = 0
                seat_belt_off_count = 0
                files = [f for f in os.listdir(folder) if f.endswith(".JPG") or f.endswith(".PNG") or f.endswith(".jpg") or f.endswith("png")]
                for file in files:
                    img_path = os.path.join(folder, file)
                    np_img = np.array(Image.open(img_path).convert('RGB').resize((256, 256)))
                    yhat = model.predict(tf.expand_dims(np_img, 0))
                    if yhat > 0.5:
                        seat_belt_on_count += 1
                    else:
                        seat_belt_off_count += 1
                seat_belt_on_counts.append(seat_belt_on_count)
                seat_belt_off_counts.append(seat_belt_off_count)

            # Create the dataframe

            total_counts = [seat_belt_on_counts[i] + seat_belt_off_counts[i] for i in range(len(seat_belt_on_counts))]



            # Create a function to determine the region based on the registration number
            def get_region(reg_number):
                if reg_number == 'kk':
                    return 'Midrand'
                elif reg_number == 'my':
                    return 'Centurion'
                elif reg_number == 'on':
                    return 'Centurion'
                else:
                    return 'Unknown'

            # Create the dataframe
            data = {'Incident Date & Time': 'coming soon...',
                    'Speed': '...',
                    'Registration No': reg_numbers,
                    'SB on': seat_belt_on_counts,
                    'SB off': seat_belt_off_counts,
                    'Total number of pictures': total_counts}

            df = pd.DataFrame(data)

            # Add the Region column to the dataframe
            df['Region'] = df['Registration No'].apply(get_region)

            # Display the dataframe in your Streamlit app
            st.dataframe(df)



            #df2 = pd.DataFrame(data2)
            #df2['Predictions'] = yhat
            #st.dataframe(df2)
            
        with st.expander('**Outcomes Complete Table**'):
            # Loop through each folder
            st.write('**------------------------------------------------FULL DETAILS TABLE-----------------------------------------------------**')
            predictions = []
            reg_numbers = []
            for folder in folders:
                # Get the registration number from the folder name
                reg_number = folder.split('_')[0]
                files = [f for f in os.listdir(folder) if f.endswith(".JPG") or f.endswith(".PNG") or f.endswith(".jpg") or f.endswith("png")]
                for file in files:
                    img_path = os.path.join(folder, file)
                    np_img = np.array(Image.open(img_path).convert('RGB').resize((256, 256)))
                    yhat = model.predict(tf.expand_dims(np_img, 0))
                    predictions.append(yhat[0][0])
                    reg_numbers.append(reg_number)

            def get_class(predictions):
                if predictions > 0.5:
                    return 'on'
                else:
                    return 'off'
                
            

            

            data2 = {'Incident Date & Time': 'coming soon...',
                    'Speed': '...',
                    'Registration No': reg_numbers,
                    'Predictions': predictions}

            df2 = pd.DataFrame(data2)

            df2['SB_satus'] = df2['Predictions'].apply(get_class)

            def get_compl(SB_status):
                if SB_status == 'on':
                    return 'Comp'
                else:
                    return 'Non-Comp'
            
            def get_branch(reg_number):
                if reg_number == 'kk':
                    return 'Sipho'
                elif reg_number == 'my':
                    return 'Kgotso'
                elif reg_number == 'on':
                    return 'Thotyelwa'
                else:
                    return 'Unknown'
                
            def get_company(reg_number):
                if reg_number == 'kk':
                    return 'Lubanzi'
                elif reg_number == 'on':
                    return 'Imizizi'
                elif reg_number == 'my':
                    return 'Lubanzi'
                else:
                    return 'Unknown'
            
            df2['Comp_stat'] = df2['SB_satus'].apply(get_compl)
            df2['Vehicle Region'] = df2['Registration No'].apply(get_region)
            df2['Company Deployed To'] = df2['Registration No'].apply(get_company)
            df2['Responsible Manager'] = df2['Registration No'].apply(get_branch)
            


            st.dataframe(df2)
            st.write('Note that the Comp_status will be determined by speed once we have the values. If the speed is above the threshold then we are going to have non compliant and if the speed is below the threshold we will have compliant')
            









                                        # GRAPHICAL REPRESENTATION OF OUR DATA



        try:
            with st.expander("**Graphical Representation of outcomes**"):
                # Create a figure with a specific size
                # Melt the dataframe to a long format
                df_melted = pd.melt(df, id_vars=['Registration No'], value_vars=['SB on', 'SB off'], var_name='Seat belt status')

                # Create the barplot using seaborn
                fig = plt.figure(figsize=(10,4))
                sns.barplot(data=df_melted, x='Registration No', y='value', hue='Seat belt status', estimator=np.sum)

                # Show the plot
                sns.set(rc={"figure.figsize": (2, 20)})
                st.pyplot(fig)
                #st.snow()
                st.balloons()

        except Exception as e:
            st.write('**Classify in order to see this section.**')#: ' + str(e))



if about:
    st.write('**About Us Coming Soon...**')


#else:
    #st.markdown("<h1 style='text-align: center; background-color: orange;'>Non Compliance Detector</h1>", unsafe_allow_html=True)
    #image = Image.open('C:/Users/KgotsoPhela(LubanziI/Desktop/snp.png')
    #st.image(image, caption='Think automation')





           #st.write('coming soon...')

    # Load the image
    #image = Image.open('C:/Users/KgotsoPhela(LubanziI/Downloads/Lubanzi prjs/Pics/Slides Pics/Lubanzi_Profile and banner pics/1667928151730.jpg')

    # Display the image
    #st.image(image, caption='Think automation')






























        # Load the image from the specified directory
    #img = io.imread(directory)

    # Resize the image using TensorFlow
    #resize = tf.image.resize(img, (256, 256))

    # Display the resized image using Matplotlib
    #fig, ax = plt.subplots()
    #ax.imshow(resize.numpy().astype(int))
    #ax.set_title('Resized Image')
    #ax.axis('off')
    #st.pyplot(fig)


