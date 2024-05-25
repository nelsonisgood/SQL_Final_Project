import aspose.cells 
from aspose.cells import Workbook


workbook = Workbook("./test_sample/txt_test.txt")
workbook.save("./sql_file/txt_test.sql")