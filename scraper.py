import requests
import xlsxwriter
from bs4 import BeautifulSoup
from xlsxwriter import worksheet

a = " "
a = input()
a += ".xlsx"
workbook = xlsxwriter.Workbook(a)
worksheet = workbook.add_worksheet()
worksheet.set_column_pixels('A:A', 800)
worksheet.set_column_pixels('B:B', 800)
nume_string = [" "]
pret_string = [" "]
URL = input()
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id = "card_grid")
job_elements = results.find_all("div", class_ = "pad-hrz-xs" )
job_elements2 = results.find_all("div", class_ = "card-v2-pricing")
for job_element in job_elements:
    nume = job_element.find("a", class_ = "card-v2-title semibold mrg-btm-xxs js-product-url")
    nume_string.append(nume.text)
for job_element2 in job_elements2:
    pret = job_element2.find("p", class_ = "product-new-price")
    pret_string.append (pret.text)
row = 0
worksheet.write(row, 0, 'Pret')
worksheet.write(row, 1, 'Nume')
for x in nume_string:
    worksheet.write(row + 1, 1, x)
    row += 1
row = 0
for x in pret_string:
    worksheet.write(row + 1, 0, x)
    row += 1
workbook.close()