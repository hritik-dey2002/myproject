import streamlit as st
import spacy
spacy.load('en_core_web_sm')

import pandas as pd
import time, datetime
from pyresparser import ResumeParser
from resume_parser import resumeparse
from streamlit_tags import st_tags
from PIL import Image
import pymysql
import plotly.express as px
from plotly import optional_imports

# from pdfminer.high_level import extract_text

connection = pymysql.connect(host='localhost', user='root', password='')
cursor = connection.cursor()

def insert_data(name, email, timestamp, no_of_pages, skills):
    DB_table_name = 'user_data4'
    insert_sql = "insert into " + DB_table_name + """
    values (0,%s,%s,%s,%s,%s)"""
    rec_values = (
    name, email, timestamp, str(no_of_pages), skills)
    cursor.execute(insert_sql, rec_values)
    connection.commit()

def delete_data(email):
    DB_table_name = 'user_data4'
    delete_sql = "delete from " + DB_table_name + """
    where email_id=%s"""
    rec_values = (email)
    cursor.execute(delete_sql, rec_values)
    connection.commit()

def run():
    st.title("Smart Resume Screening")
    activities = ["User", "Admin","Company"]
    choice = st.selectbox("Choose among the given options:", activities)
    img = Image.open('./Logo/smart.jpg')
    img = img.resize((700, 390))
    st.image(img)

    # Create the DB
    db_sql = """CREATE DATABASE IF NOT EXISTS SRA3;"""
    cursor.execute(db_sql)
    connection.select_db("sra3")

    # Create table
    DB_table_name = 'user_data4'
    table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                    (ID INT NOT NULL AUTO_INCREMENT,
                     Name varchar(100) NOT NULL,
                     Email_ID VARCHAR(50) NOT NULL,
                     Timestamp VARCHAR(50) NOT NULL,
                     Page_no VARCHAR(5) NOT NULL,
                     Actual_skills VARCHAR(300) NOT NULL,
                     PRIMARY KEY (ID));
                    """
    cursor.execute(table_sql)

   

    if choice == 'User':
        
        # st.header("welcome to user side")
        # activities1 = ["New User", "update"]
        # choice1 = st.selectbox("Choose among the given options:", activities1)

        # if choice1 == 'New User':

            pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
            if st.button("submit resume", type="primary"):
                if pdf_file is not None:
                    save_image_path = './Uploaded_Resumes/' + pdf_file.name
                    with open(save_image_path, "wb") as f:
                        f.write(pdf_file.getbuffer())
                    resume_data = ResumeParser(save_image_path).get_extracted_data()
                    # data2 = resumeparse.read_file(save_image_path)
                    # text = extract_text(save_image_path)
                    # st.text(text)
                    if resume_data:
                        st.header("**Resume Analysis**")
                        st.success("Congratulations " + resume_data['name'] +' . your resume has been submitted')
                        st.subheader("**Candidates Basic info**")
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

                        delete_data(resume_data['email'])

                        insert_data(resume_data['name'], resume_data['email'], timestamp,
                            str(resume_data['no_of_pages']), str(resume_data['skills']))

                        connection.commit()

                    else:
                        st.error("sometimes went wrong.....")
                else:
                    st.warning('Warning message')
                    st.error("Upload the resume")


        # else:
        #     pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
        #     if st.button("submit resume", type="primary"):
        #         if pdf_file is not None:
        #             save_image_path = './Uploaded_Resumes/' + pdf_file.name
        #             with open(save_image_path, "wb") as f:
        #                 f.write(pdf_file.getbuffer())
        #             resume_data = ResumeParser(save_image_path).get_extracted_data()

        #             if resume_data:
        #                 st.header("**Resume Analysis**")
        #                 st.success("Congratulations " + resume_data['name'] +' . your resume has been submitted')
        #                 st.subheader("**Candidates Basic info**")
        #                 try:
        #                     st.text('Name: ' + resume_data['name'])
        #                     st.text('Email: ' + resume_data['email'])
        #                     st.text('Resume pages: ' + str(resume_data['no_of_pages']))
        #                 except:
        #                     pass

        #                 ts = time.time()
        #                 cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        #                 cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        #                 timestamp = str(cur_date + '_' + cur_time)

        #                 st.balloons()

        #                 delete_data(resume_data['email'])

        #                 insert_data(resume_data['name'], resume_data['email'], timestamp,
        #                     str(resume_data['no_of_pages']), str(resume_data['skills']))

        #                 connection.commit()

                


        #             else:
        #                 st.error("sometimes went wrong.....")
        #         else:
        #             st.warning('Warning message')
        #             st.error("Upload the resume")

                    
            





    elif choice=='Admin':
        st.header("welcome to admin side")
        admin_user=st.text_input("username")
        admin_password=st.text_input("password",type='password')
        if st.button('login'):
            if admin_user=='admin' and admin_password=='admin123':
                st.success("welcome admin")

                cursor.execute('''SELECT*FROM user_data4''')
                data = cursor.fetchall()
                st.header("**User's Data**")
                df = pd.DataFrame(data, columns=['ID', 'Name', 'Email', 'Timestamp', 'Total Page', 'Actual Skills'])
                st.dataframe(df)
 
                st.balloons()


            else:
                st.error("Wrong ID & Password Provided")






    else:
        st.header("welcome to company side")
        company_user=st.text_input("username")
        company_password=st.text_input("password",type='password')
        if st.button('login'):
            if company_user=='company' and company_password=='company123':
                st.success("welcome company")
               
                mark=st.text_input(label='Enter Keywords:')
                keywords = st_tags(
                    label=' Enter Keywords:',
                    text='Press enter to add more',
                    value=['Zero', 'One', 'Two'],
                    suggestions=['five', 'six', 'seven', 
                    'eight', 'nine', 'three', 
                    'eleven', 'ten', 'four'],
                    maxtags = 4,
                    key='1')
        
                st.write(keywords)

                st.balloons()

            else:
                st.error("Wrong ID & Password Provided")

run()

