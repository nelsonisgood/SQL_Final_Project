from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables

import streamlit as st
import os
import mysql.connector
import google.generativeai as genai

## Configure Genai Key

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Load model
model=genai.GenerativeModel('gemini-pro')

## Function To Load Google Gemini Model and provide queries as response
def get_gemini_response(question,prompt):
    response=model.generate_content([prompt[0],question])
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


## Define Your Prompt
prompt=[
    """
    You are an expert in converting questions to mySQL query, and no matter what, your response must be valid mysql command.
    The SQL database has the name hw5 and the following is the show create table sql command of a table named student
    \n
    CREATE TABLE `student` (
    `身分` varchar(5) DEFAULT NULL,
    `系所` varchar(15) DEFAULT NULL,
    `年級` tinyint unsigned DEFAULT NULL,
    `學號` varchar(10) DEFAULT NULL,
    `姓名` varchar(30) DEFAULT NULL,
    `信箱` varchar(25) DEFAULT NULL,
    `班別` varchar(30) DEFAULT NULL,
    `組別` int DEFAULT NULL,
    `組長` int DEFAULT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    INSERT INTO `student` VALUES ('學生','經濟系      ',3,'B10303008','劉家妮 (CHIA-NIH LIU)','b10303008@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','經濟系      ',3,'B10303129','吳東諺 (WU, TUNG-YEN)','b10303129@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','經濟系      ',4,'B09303019','黃于軒 (HUANG,YU-hsUAN)','b09303019@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','經濟系      ',4,'B09303021','李胤愷 (Lee, yin-kai)','b09303021@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','經濟系      ',4,'B09303027','林睿霖 (LIN,RUEI-LIN)','b09303027@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','經濟系      ',4,'B09303090','呂彥欣 (LU,YAN-XIN)','b09303090@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','機械系      ',4,'B09502132','周哲瑋 (CHOU,CHE-WEI)','b09502132@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','材料系      ',4,'B09507021','王禹翔 (WANG YU-HSIANG)','b09507021@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','醫工系      ',4,'B09508013','陳品文 (CHEN, PIN-WEN)','b09508013@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','醫工系      ',4,'B09508014','邱泓翊 (CHIU, hung-yi)','b09508014@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','土木所水利組',1,'R12521323','廖宥弘 (YOU-HONG LIAO)','r12521323@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','土木所營管組',1,'R12521709','蔡承耘 (TSAI, CHENG-YUN)','r12521709@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','土木所營管組',3,'R10521707','林志璿 (ZHI-XUAN, LIN)','r10521707@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','機械所固力組',1,'R12522508','侯貝霖 (PEI-LIN HOU)','r12522508@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','機械所固力組',1,'R12522532','薛  龍 (HSUEH, LUNG)','r12522532@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','機械所製造組',1,'R12522706','包杰修 (PAO, CHIEH-HSIU)','r12522706@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','機械所製造組',1,'R12522729','鄭淳哲 (CHENG CHUN-TSE)','r12522729@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','工科海洋所  ',1,'R12525068','黃  靖 (HUANG, JING)','r12525068@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','工科海洋所  ',1,'R12525074','張瀚文 (CHANG HAN-WEN)','r12525074@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','工科海洋所  ',2,'R11525074','張容誠 (JUNG-CHENG CHANG)','r11525074@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','材料所      ',1,'R12527017','劉育君 (YU-CHUN LIU)','r12527017@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','材料所應材班',1,'R12527A01','張瑋哲 (CHANG, WEI-CHE)','r12527a01@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','動科系      ',4,'B09606007','賴宇辰 (LAI,YU/CHEN)','b09606007@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','動科系      ',4,'B09606048','王奕翔 (Wang Yi-Hsiang)','b09606048@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','生物機電系  ',4,'B08611041','郭子敬 (TZU-CHING KUO)','b08611041@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','生物機電系  ',4,'B09611018','晏文芳 (YEN, WEN-FANG)','b09611018@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','生物機電系  ',4,'B09611040','張乃恩 (ZHANG,NAI-EN)','b09611040@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','生物機電系  ',4,'B09611047','蔡予恩 (TSAI, JONAS)','b09611047@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','森林環資所  ',3,'R10625016','許致銓 (CHIH-CHUAN HSU)','r10625016@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','生物機電所  ',1,'R12631001','許喬淇 (HSU, CHIAO-CHI)','r12631001@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',1,0),('學生','生物機電所  ',1,'R12631009','謝欣妤 (HSIEH, HSIN-YU)','r12631009@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',1,0),('學生','生物機電所  ',1,'R12631012','連震宇 (LIAN, JEN-YU)','r12631012@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',1,0),('特優生','生物機電所  ',1,'R12631013','鄭朝鴻 (CHAO HUNG, JENG)','r12631013@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',1,1),('學生','生物機電所  ',1,'R12631014','蔡知芸 (TSAI, CHIH-YUN)','r12631014@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','生物機電所  ',1,'R12631025','白騏瑞 (BAI, CI-RUEI)','r12631025@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','生物機電所  ',1,'R12631036','陳思齊 (CHEN, SSU-CHI)','r12631036@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','生物機電所  ',1,'R12631069','洪旭初 (HONG, XU-CHU)','r12631069@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','工管系企管組',3,'B10701166','謝廷寬','b10701166@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','工管系科管組',2,'B11701247','黃柏儒 (HUANG,BO-RU)','b11701247@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','財金系      ',4,'B09703085','吳柏賢 (WU PO-HSIEN)','b09703085@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','資訊管理所  ',1,'R12725045','劉姝豆 (SHU-DOU,LIU)','r12725045@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','資訊管理所  ',1,'R12725046','黃冠綸 (HUANG, GUAN-LUN)','r12725046@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','資訊管理所  ',1,'R12725053','李宇軒 (LEE, YU-HSUAN)','r12725053@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','資訊管理所  ',1,'R12725066','鍾靖詮 (CHUNG, CHING-CHUAN)','r12725066@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','資訊管理所  ',2,'R11725042','陳冠甫 (GUAN-FU,CHEN)','r11725042@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','流預所      ',2,'R11849036','許國昌 (KUO-CHANG HSU)','r11849036@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','電機系      ',3,'B10901036','許景淯 (HSU CHING YU)','b10901036@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','電機系      ',3,'B10901039','劉庭均 (Liu,ting-chun)','b10901039@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','電機系      ',3,'B10901190','吳承羲 (WU,CHENG-XI)','b10901190@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','電機系      ',4,'B07901113','廖甜雅 (LIAO, TIEN-YA)','b07901113@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','電機系      ',4,'B09901019','劉瑄穎 (LIU,HSUAN-YING)','b09901019@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','電機系      ',4,'B09901162','陳冠霖 (CHEN,GUAN-LIN)','b09901162@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','資工系      ',3,'B10902086','曹宸睿 (Chen Jui Tsao)','b10902086@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','資工系      ',3,'B10902103','毛翊蓁 (MAO YI CHEN)','b10902103@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','資工系      ',4,'B09902032','彭昱齊 (PENG YUCHI)','b09902032@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','資工系      ',4,'B09902064','楊冠柏 (YANG, GUAN-BO)','b09902064@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','電機所      ',1,'R12921039','李語婕 (LEE, YU-CHIEH)','r12921039@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','電機所      ',1,'R12921040','柯岱佑 (KO, DAI-YOU)','r12921040@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','電機所      ',1,'R12921053','周昱宏 (CHOU, YU-HONG)','r12921053@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','電機所      ',1,'R12921057','林佳儀 (LIN, CHIA-YI)','r12921057@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','電機所      ',1,'R12921059','鄧雅文 (TENG, YA-WEN)','r12921059@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','電機所      ',1,'R12921063','楊士聖 (YANG, SHIH-SHENG)','r12921063@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','電機所      ',1,'R12921093','吳吉加 (CHI-CHIA WU)','r12921093@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','電機所      ',1,'R12921097','江浩辰 (JIANG, HAO-CHEN)','r12921097@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','電機所      ',1,'R12921101','丁柏豪 (PO-HAO TING)','r12921101@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','電機所      ',1,'R12921105','游景恩 (YU, JING-EN)','r12921105@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','電機所      ',1,'R12921125','楊沛蓉 (PEI-RONG YANG)','r12921125@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','',3,'R10921A16','李英碩 (LEE YING-SHUO)','r10921a16@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','',2,'F10921065','吳建翰 (WU, JIAN-HAN)','f10921065@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','資工所      ',1,'R12922031','曾光良 (TSENG, KUANG-LIANG)','r12922031@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','資工所      ',1,'R12922044','陳映璇 (YING-HSUAN CHEN)','r12922044@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','資工所      ',1,'R12922045','陳沛妤 (PEI-YU CHEN)','r12922045@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','資工所      ',1,'R12922064','林郁敏 (LIN, YU-MIN)','r12922064@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','資工所      ',1,'R12922116','王偉力 (WANG, WEI-LI)','r12922116@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','資工所      ',1,'R12922122','吳東鴻 (WU, DONG-HONG)','r12922122@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','資工所      ',1,'R12922129','賴翰霖 (HAN-LIN LAI)','r12922129@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','資工所      ',1,'R12922145','謝承恩 (HSIEH, CHENG-EN)','r12922145@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','資工所      ',1,'R12922159','沈信宏 (SHEN, XIN-HONG)','r12922159@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','資工所      ',1,'R12922204','高子維 (KAO, TZU-WEI)','r12922204@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','資工所      ',1,'R12922205','李哲維 (LEE, ZER-WEI)','r12922205@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','資工所      ',1,'R12922217','郭沛孚 (GUO, PEI-FU)','r12922217@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','資工所      ',2,'R11922140','劉盈妤 (LIU,YING-YU)','r11922140@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','資工所      ',2,'R11922156','費俊昱 (CHUN-YU FEI)','r11922156@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','電信所      ',1,'R12942078','陳怜均 (CHEN, LING-CHUN)','r12942078@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','電信所      ',1,'R12942143','林翰莘 (LIN, HAN-HSIN)','r12942143@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','電信所      ',1,'R12942148','林峻佑 (LIN, CHUN-YU)','r12942148@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','電信所      ',1,'R12942170','陳彥亨 (1)','r12942170@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','電信所      ',1,'R12942181','陳祈安 (CHEN, CHI-AN)','r12942181@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','網媒所      ',1,'R12944005','陳乙馨 (CHEN, I-HSIN)','r12944005@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','網媒所      ',1,'R12944006','郭承諺 (CHENG-YEN KUO)','r12944006@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','網媒所      ',1,'R12944014','張心瑜 (CHANG, HSIN-YU)','r12944014@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','生醫電資所  ',1,'R12945037','卓均而 (CHO, CHUN-ERH)','r12945037@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','基因學位學程',1,'R12B48005','葉政翔 (ZHENG-XIANG YE)','r12b48005@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('旁聽生','政治所      ',2,'D11322005','喬  穆 (ARTEM KOLOS)','d11322005@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('旁聽生','政治所      ',3,'R10322005','魏志展 (WEI, JHIH-JHAN)','r10322005@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('旁聽生','政治所      ',3,'R10322029','郭芃廷 (KUO, PENG-TING)','r10322029@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('旁聽生','土木所CAE組 ',1,'R12521609','洪兆昇 (CHAO-SHENG HUNG)','r12521609@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('旁聽生','電機系      ',2,'B11901174','傅啟恩 (CHI-AN OSCAR FU)','b11901174@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('旁聽生','電機系      ',3,'B10505021','蕭銜甫 (HSIAO,HSIEN-FU)','b10505021@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('旁聽生','資工系      ',2,'B11902091','姚權維 (YEO GUAN WEI)','b11902091@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('旁聽生','電機所      ',3,'D10921006','邱世弦 (CHIU, SHIH-HSUAN)','d10921006@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('旁聽生','資工所      ',3,'R10922187','陳正康 (CHEN, CHENG-KANG)','r10922187@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('旁聽生','電信所      ',2,'R11942148','洪正維 (HUNG,CHENG-WEI)','r11942148@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('旁聽生','電機所',2,'R10123456','小紅','r10123456@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('學生','物理系',3,'B09987653','小黃','b09987653@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0),('觀察者','電信所',1,'R11123001','小綠','r11123001@ntu.edu.tw','資料庫系統-從SQL到NoSQL (EE5178)',0,0);
    \nFor example, the question will be something like '我想知道所有在組別1裡面的同學', the corresponding SQL command would be like this 'select 姓名 from student where 組別 = 1', and if the question is '幫我加入一個人的資料，他的身分是學生，系所是公衛系，4年級', the corresponding SQL command would be like this 'insert into student (身分, 系所, 年級) values ('學生', '公衛系', 4)', 
    \n
    also the sql code should not have ``` in beginning or end and sql word in output.

    """

]

## Streamlit App

st.set_page_config(page_title="I can convert you sentense to MySQL query!")
st.header("NL2SQL converter with Gemini pro")

## 設定文字輸入框，label 為 widget 的顯示文字，key 是 widget 的 ID
question=st.text_input(label="Input: ",key="input")


# if enter is clicked
if question:
    response=get_gemini_response(question,prompt)
    print(response)
    output=read_sql_query(response,"hw5")
    st.subheader(f'The SQL command is:')
    st.subheader(response)
    st.subheader("The Response is")
    for row in output:
        print(row)
        st.subheader(row)