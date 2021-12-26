import requests
#import xlsxwriter
from bs4 import BeautifulSoup
#from xlsxwriter import worksheet

#a = " "
#a = input()
#a += ".xlsx"
#workbook = xlsxwriter.Workbook(a)
#worksheet = workbook.add_worksheet()
#worksheet.set_column_pixels('A:A', 800)
#worksheet.set_column_pixels('B:B', 800)
#change the first and 2nd collumn sizes
#name_string = [" "]
#pret_string = [" "]
URL = input()
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id = "posts")
job_elements = results.find_all("h1", class_ = "post-title entry-title" )
for job_element in job_elements:
    name = job_element.find("a", rel = "bookmark")
    title = name.text
    title = title.replace(" ","-")
    title = title.replace("[","")
    title = title.replace("]","")
    link = str(name)
    print(name.text)
    link = link[9:]
    link = link[0:20]
    link = link + title
    print(link)
#row = 0
#worksheet.write(row, 0, 'Link')
#worksheet.write(row, 1, 'Name')
#for x in name_string:
#    worksheet.write(row + 1, 1, x)
#    row += 1
#workbook.close()