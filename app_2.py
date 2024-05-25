from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables

import streamlit as st
import os
import mysql.connector
import google.generativeai as genai
import tempfile
import time
import re

## Configure Genai Key

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Load model
model=genai.GenerativeModel('gemini-pro')

## Function To Load Google Gemini Model and provide queries as response
def get_gemini_response(question, prompt, db_contents):
    contents = [prompt[0], question, db_contents]
    response = model.generate_content(contents)
    return response.text


## Fucntion To retrieve query from the database
def read_sql_query(sql,db):
    host = 'localhost'
    user = 'root'
    passwd = 'Linbaynj0601'
    conn=mysql.connector.connect(user=user, password=passwd, host=host, database=db)
    cr=conn.cursor()
    cr.execute(sql)
    rows=cr.fetchall()
    conn.commit()
    cr.close()
    conn.close()
    for row in rows:
        print(row)
    return rows


## renew DB data txt file
def renew_DB(state, db, table_name=None):
    # Renew ALL DB
    if state == 'ALL DB':
        cmd = r'"C:/Program Files/MySQL/MySQL Server 8.0/bin/mysqldump.exe" -u root -p{} -h localhost {} > DBdata.txt'.format('Linbaynj0601', db)
        try:
            # Execute the command using os.system()
            result = os.system(cmd)
            if result == 0:
                print(f"DB '{db}' export successful")
            else:
                print(f"Error occurred during db'{db}' export")
        except Exception as e:
            print(f"An error occurred: {e}")

    if state == 'TABLE':
        # Construct the mysqldump command for a single table
        cmd = r'"C:/Program Files/MySQL/MySQL Server 8.0/bin/mysqldump.exe" -u root -pLinbaynj0601 -h localhost {} {} > {}.txt'.format(db, table_name, table_name)
        try:
            # Execute the command using os.system()
            result = os.system(cmd)
            if result == 0:
                print(f"Table '{table_name}' export successful")
            else:
                print(f"Error occurred during table '{table_name}' export")
        except Exception as e:
            print(f"An error occurred: {e}")

## read DB data txt file
def read_DB(state,table_name=None):
    if state == 'ALL DB':
        with open("DBdata.txt", 'r', encoding='utf-8') as file:
            db_content = file.read()
    elif state == 'TABLE':
        with open(f"{table_name}.txt", 'r', encoding='utf-8') as file:
            db_content = file.read()
    return db_content

def extract_table_name(sql_query):
    # 提取 insert 语句中的表名
    insert_pattern = r'insert\s+into\s+(\w+)'
    match = re.search(insert_pattern, sql_query, re.IGNORECASE)
    if match:
        return match.group(1)

    # 提取 create 语句中的表名
    create_pattern = r'create\s+table\s+(\w+)'
    match = re.search(create_pattern, sql_query, re.IGNORECASE)
    if match:
        return match.group(1)

    return None

## Define Your Prompt
prompt=[
    """
    You are an expert in converting questions to mySQL query, 
    and no matter what, your response must be valid mysql command.
    \n
    also the sql code should not have ``` in beginning or end and sql word in output.
    
    """

]

## Streamlit App

st.set_page_config(page_title="I can convert you sentense to MySQL query!")
st.header("NL2SQL converter with Gemini pro")

## 設定文字輸入框，label 為 widget 的顯示文字，key 是 widget 的 ID
question=st.text_input(label="Input: ",key="input")

# choose db
choice = read_sql_query('show databases', None)
choice_list = list()
table_names = []
db = str()
for i in range(len(choice)):
    choice_list.append(choice[i][0])

db_option = st.sidebar.selectbox(
    'Select Database',
    choice_list)
if db_option:
    db = db_option
    read_sql_query(f'use {db}', db)
    # 首先了解db內容和有的table
    renew_DB(state='ALL DB', db=db)
    all_db_content = read_DB(state='ALL DB')
    table_names = re.findall(r'CREATE TABLE `(\w+)`', all_db_content)
    for table in table_names:
        renew_DB(state='TABLE', db=db, table_name=table)

# if enter is clicked
if question:
    db_contents = str()
    # 找Q中有哪些table，假設tablename會用反引號標示，例如`table`
    tables_used = re.findall(r'`(\w+)`', question)
    
    if tables_used:
        for table in tables_used:
            if table in table_names:
                db_contents = read_DB(state='TABLE', table_name=table)
                response = get_gemini_response(question, prompt, db_contents)
    else:   # 如果沒有提到table就讀DBdata.txt
        renew_DB(state='ALL DB', db=db)
        all_db_content = read_DB(state='ALL DB')
        response = get_gemini_response(question, prompt, all_db_content)

    # If the response modifies the database
    if 'insert' in response.lower() or 'create' in response.lower():
        table_name = extract_table_name(response)
        if table_name:
            renew_DB(state='TABLE', db=db, table_name=table_name)
            
    
    output=read_sql_query(response, db)
    st.subheader(f'The SQL command is:')
    st.subheader(response)
    st.subheader("The Response is")
    for row in output:
        print(type(row))
        st.subheader(row)

