from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import pandas as pd
import xlsxwriter
dataFrame = pd.DataFrame(columns=['Record No.', 'Movie Name', 'IMDB Rating', 'Metascore', 'No. of Votes', 'Gross'])
pages = [i for i in range(1,10)] #can enter any number of pages
years_url = ['2000'] #can enter any number of years
count1 = 0
for years in years_url:
    for page in pages:
        myUrl = 'https://www.imdb.com/search/title?release_date={}-01-01,{}-12-31&sort=num_votes,desc&start={}&ref_=adv_nxt'.format(years, years, ((page*50)+1))
        uClient = uReq(myUrl)
        pageHtml = uClient.read()
        uClient.close()
        pageSoup = soup(pageHtml, 'html.parser')
        containers = pageSoup.findAll('div', {"class" : "lister-item mode-advanced"})
        for i in containers:
            metascore, votes, gross = 'N/A', 'N/A', 'N/A'
            count1 += 1
            name_container = i.find('h3', {'class': 'lister-item-header'})
            name = name_container.a.text.strip()
            rating_container = i.find('div', {'class': 'inline-block ratings-imdb-rating'})
            rating = rating_container.text.strip()
            if(i.find('span', {'class': 'metascore favorable'})):
                metascore_container = i.find('span', {'class': 'metascore favorable'})
                metascore = metascore_container.text.strip()
            if(len(i.findAll('span', {'name': 'nv'})) == 2):
                vg_container = i.findAll('span', {'name': 'nv'})
                votes = vg_container[0].text.strip()
                gross = vg_container[1].text.strip()
            elif(len(i.findAll('span', {'name': 'nv'})) == 1):
                vg_container = i.findAll('span', {'name': 'nv'})
                votes = vg_container[0].text.strip()
            ser = pd.Series([count1, name, rating, metascore, votes, gross], index = ['Record No.', 'Movie Name', 'IMDB Rating', 'Metascore', 'No. of Votes', 'Gross']) 
            dataFrame = dataFrame.append(ser, ignore_index=True)
filename = 'output.xlsx'
writer = pd.ExcelWriter(filename, engine='xlsxwriter')
dataFrame.to_excel(writer, index=False)
writer.save()
