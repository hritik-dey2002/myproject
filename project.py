import streamlit as st
import spacy
import nltk
spacy.load('en_core_web_sm')
nltk.download('stopwords')
import pandas as pd
import time, datetime
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
from streamlit_tags import st_tags
from PIL import Image
import plotly.express as px
from plotly import optional_imports
# from pdfminer.high_level import extract_text

# connection = pymysql.connect(host='localhost', user='root', password='')
# cursor = connection.cursor()

def run():
    st.title("Smart Resume Screening")
    activities = ["User", "Admin","Company"]
    choice = st.selectbox("Choose among the given options:", activities)
    # img = Image.open('./Logo/smart.jpg')
    # img = img.resize((700, 390))
    # st.image(img)

   
    if choice == 'User':

            pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
            if st.button("submit resume", type="primary"):
                if pdf_file is not None:
                    # save_image_path = './Uploaded_Resumes/' + pdf_file.name
                    # with open(save_image_path, "wb") as f:
                    #     f.write(pdf_file.getbuffer())
                    # resume_data = ResumeParser(save_image_path).get_extracted_data()
                    resume_data = ResumeParser(pdf_file).get_extracted_data()
                    # text = extract_text(save_image_path)
                    # st.text(text)
                    if resume_data:
                        st.header("*Resume Analysis*")
                        st.success("Congratulations " + resume_data['name'] +' . your resume has been submitted')
                        st.subheader("*Candidates Basic info*")
                        try:
                            st.text('Name: ' + resume_data['name'])
                            st.text('Email: ' + resume_data['email'])
                            st.text('Resume pages: ' + str(resume_data['no_of_pages']))
                        except:
                            pass

                        ts = time.time()
                        cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                        cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                        timestamp = str(cur_date + '_' + cur_time)

                        st.balloons()
                else:
                    st.warning('Warning message')
            





    elif choice=='Admin':
        st.success('Welcome to Admin Side')
        admin_user=st.text_input("username")
        admin_password=st.text_input("password",type='password')
        if st.button('login'):
            if admin_user=='admin' and admin_password=='admin123':
                st.success("welcome admin")
                st.balloons()
            else:
                st.error("Wrong ID & Password Provided")






    else:
        st.header("welcome to company side")
        admin_user=st.text_input("username")
        admin_password=st.text_input("password",type='password')
        if st.button('login'):
            if admin_user=='company' and admin_password=='company123':
                st.success("welcome company")
                st.balloons()
                keywords = st_tags(
                    label='# Enter Keywords:',
                    text='Press enter to add more',
                    value=['Zero', 'One', 'Two'],
                    suggestions=['five', 'six', 'seven', 
                        'eight', 'nine', 'three', 
                        'eleven', 'ten', 'four'],
                    maxtags = 4,
                    key='1')
            else:
                st.error("Wrong ID & Password Provided")

run()
