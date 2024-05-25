import  jpype     
import  asposecells    
import subprocess 
import tabula

# 查看PDF內容
dfs = tabula.read_pdf("./test_sample/data.pdf", pages='1', stream=True) # pages可選擇頁數 ex: 'all', '1'

# 將PDF轉成csv檔
tabula.convert_into("./test_sample/data.pdf", "./sql_file/data.csv", output_format="csv", pages='1', stream=True)


jpype.startJVM() 
from asposecells.api import Workbook
workbook = Workbook("./sql_file/data.csv") # pdf -> csv -> sql
workbook.save("./sql_file/data.sql")
jpype.shutdownJVM()





# 只能產出PostgreSQL語法

# 定義命令
# command = [
#     "csv2sql", "all",
#     "-i", "output.csv",
#     "-o", "cars_info.sql",
#     "car_info"
# ]

# # 執行命令
# subprocess.run(command)

