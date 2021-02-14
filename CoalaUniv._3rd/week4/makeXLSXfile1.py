import openpyxl

wb = openpyxl.Workbook()

sheet = wb.active
sheet['A1'] = 'hello world!'
sheet.cell(row=3, column=3).value='BYE!!'        #행 / 열 번호를 통해 셀 값을 입력하거나 변경한다. 

subject = ['Python', 'Java', 'HTML', 'JavaScript']
sheet.append(subject)        #시트에 행을 추가한다. 

wb.save('test.xlsx')