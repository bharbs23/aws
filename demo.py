import glob
import csv
import xlwt
import os

wb = xlwt.Workbook()


for filename in glob.glob("C:/Users/bharbs/Desktop/aws_scripts/scripts/output/*.csv"):
    (f_path, f_name) = os.path.split(filename)
    (f_short_name, f_extension) = os.path.splitext(f_name)
    ws = wb.add_sheet(str(f_short_name))
    spamReader = csv.reader(open(filename, 'rb'), delimiter=',',quotechar='"')
    row_count = 0
    for row in spamReader:
        for col in range(len(row)):
            ws.write(row_count,col,row[col])
        row_count +=1

wb.save("C:/Users/bharbs/Desktop/aws_scripts/scripts/output.xls")

print "Done"