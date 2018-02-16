from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

fread =  open('./data/urlList.txt','r')
fwrite = open('./data/urlListout.txt','w')
fwrite.write('url'+'\t'+ 'iaPath' +'\t'+ 'campaignURL' + '\t'
                        + 'CAMPAIGN' 
                        +'\t'+ 'COUNTRY_SITE'
                        +'\t'+ 'POSITION'
                        +'\t'+ 'REFERRING_SITE'
                        +'\t'+ 'CREATIVE'+'\n')
for url in fread:
    url = url.rstrip()
    html = urlopen(url)
    #read URL
    soup = BeautifulSoup(html,'html.parser')
    #Get Meta tags
    for tag in soup.find_all("meta"):
        try:
            name = tag['name']
        except:
            name = "Not Defined"

        if name == 'iaPath':
            iaPathvalue = tag['content']

    #Get Campaign href from HTML content 
    for link in soup.find_all('a'):
        linkval = link.get('href')
        myDict = {}
        try:
            if re.search('.*CAMPAIGN.*',linkval):
                campaignURL = linkval.split('?')[0]
                dqp = linkval.split('?')[1]
                for keyvalue in dqp.split('&'):
                    key, value = keyvalue.split('=')
                    myDict[key] = value
                
                fwrite.write(url+'\t'+ iaPathvalue +'\t'+ campaignURL 
                        + '\t'+ myDict.get('CAMPAIGN','None')
                        +'\t'+ myDict.get('COUNTRY_SITE','None')
                        +'\t'+ myDict.get('POSITION','None')
                        +'\t'+ myDict.get('REFERRING_SITE','None')
                        +'\t'+ myDict.get('CREATIVE','None') + '\n')
        except:
            continue
fread.close()
fwrite.close()
