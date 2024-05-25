import  jpype     
import  asposecells


jpype.startJVM() 
from asposecells.api import Workbook
workbook = Workbook("./test_sample/html_test.html")
workbook.save("./sql_file/html_test.sql")
jpype.shutdownJVM()