from requests import get
from bs4 import BeautifulSoup as soup
import pandas as pd
import xlsxwriter
dataFrame = pd.DataFrame(columns=['Company Name', 'Zip Code', 'Email', 'Website', 'Category'])
link = 'https://www.gelbeseiten.de/zimmervermietung/s{}' #can be any url containing companies in gelbeseiten
response = get(link.format(1))
html = soup(response.text, 'html.parser')
category = html.find('input', {'class':'what_search'})['value']
total = html.find('div', { "id" : "trefferlistenstatuszeile"})
if(total):
    total = total.find('p')
    if(total):
        total = total.text.strip()
        index = total.rfind(' ')
        total = int(total[index:])
        pages = (total//15) + 1
    else:
        pages = 1
for i in range(1, 50):
    response = get(link.format(i))
    html = soup(response.text, 'html.parser') 
    locality = html.find_all('div', {'class':'table'})
    for x in locality:
        web = x.find('div', {'class':'website'})
        name = x.find(itemprop = "name")
        zipCode = x.find(itemprop = "zipCode")
        mail = x.find('a', {'class':'email_native_app'})
        if(mail):
            mail = mail['href']
            sindex = mail.find(":") + 1
            eindex = mail.find("?")
            email = mail[sindex:eindex]
        else:
            email = 'N/A'
        if(name):
            name = name.text
        else:
            name = 'N/A'
        if(zipCode):
            zipCode = zipCode.text
        else:
            zipCode = 'N/A'
        if(web):
            web = web.find('a', {'class' : 'link'})['href']
        else:
            web = 'N/A'
        ser = pd.Series([name, zipCode, email, web, category], index = ['Company Name', 'Zip Code', 'Email', 'Website', 'Category']) 
        dataFrame = dataFrame.append(ser, ignore_index=True)                       
filename = 'output.xlsx'
writer = pd.ExcelWriter(filename, engine='xlsxwriter')
dataFrame.to_excel(writer, index=False)
writer.save()  
            
    
