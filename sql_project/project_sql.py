import requests
import pandas as pd
import numpy as np
import pdfplumber
import os, re
import mysql.connector as sc
import sys

from bs4 import BeautifulSoup
from xmlutils.xml2sql import xml2sql

sys.setrecursionlimit(1000000)

# # 連接 mySQL database
# mydb = sc.connect(
#     host = "127.0.0.1",    
#     user = "root",   
#     passwd = "Gina19880528&&"
#   )
# cursor = mydb.cursor(buffered=True)

# def read_pdf(pdf_file):
#     pdf = pdfplumber.open(pdf_file)
#     p0 = pdf.pages[0]

#     text = p0.extract_text()
#     print(type(text))
#     print([text])

# def html2sql(url):
#     web = requests.get(url)
#     web.encoding='utf-8'

#     soup = BeautifulSoup(web.text, "html.parser")  # 轉換成標籤樹
#     title = soup.find_all()                           # 取得 title
#     print(title)

# xml to sql file
def xml_sql(input_xml):
    # 從檔名獲取table名稱
    split1 = input_xml.split("/")[-1]
    split2 = split1.split(".")[0]
    # 獲取現在檔案位置
    path = os.getcwd()
    output_sql = path + "/" + split2 + ".sql"

    converter = xml2sql(input_xml, output_sql)
    converter.convert(tag="item", table=split2)

# pdf_file = "C:/Users/gina1/desktop/報告-台大副本/蜜蜂相關paper/1-s2.0-S0168169921002568-main.pdf"
# read_pdf(pdf_file)

# url = input("what's your url : ")
# url = input("what's your keyword : ")
# html2sql(url)

input_xml = "C:/Users/gina1/desktop/model/xmlutils.py-master/samples/fruits.xml"
xml_sql(input_xml)

