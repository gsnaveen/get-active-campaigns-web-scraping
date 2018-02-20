from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

fread =  open('./data/urlList.txt','r') # Read inout list of URLs
fwrite = open('./data/activeCampaigns.txt','w') # Open a write file for output 
fwrite.write('url'+'\t'+ 'metatag' +'\t'+ 'campaignURL' + '\t'
                        + 'CAMPAIGN' 
                        +'\t'+ 'COUNTRY'
                        +'\t'+ 'POSITION'
                        +'\t'+ 'REFERRING_URL'
                        +'\t'+ 'CREATIVE'+'\n') # Writing header of the file
for url in fread:
    url = url.rstrip()
    html = urlopen(url)
    #read URL
    soup = BeautifulSoup(html,'html.parser') # Parse input URL content
    #Get Meta tags
    metatagValue = ''
    for tag in soup.find_all("meta"):
        try:
            name = tag['name']
        except:
            name = "Not Defined"

        if name == 'metatag':
            metatagValue = tag['content']

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
                
                fwrite.write(url+'\t'+ metatagValue +'\t'+ campaignURL 
                        + '\t'+ myDict.get('CAMPAIGN','None')
                        +'\t'+ myDict.get('COUNTRY','None')
                        +'\t'+ myDict.get('POSITION','None')
                        +'\t'+ myDict.get('REFERRING_URL','None')
                        +'\t'+ myDict.get('CREATIVE','None') + '\n')
        except:
            continue
fread.close()
fwrite.close()
