import xlsxwriter
import sqlite3

workbook = xlsxwriter.Workbook('result.xlsx')
worksheet = workbook.add_worksheet()

conn = sqlite3.connect("data.db")
c = conn.cursor()

row = 0
for rec in c.execute('''SELECT * FROM score'''):
    for i in range(1, 12):
        worksheet.write(row, i - 1, str(rec[i]))
    row += 1

workbook.close()
