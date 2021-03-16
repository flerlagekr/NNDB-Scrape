#  This code will loop through each letter on www.nndb.com, scraping people data.
#  The data is then written to a csv file.
#
#  Written by Ken Flerlage, Feburary, 2018
#
#  This code is in the public domain

import codecs
import requests
from bs4 import BeautifulSoup

#---------------------------------------------------------------------------------------
# Main processing routine.
#---------------------------------------------------------------------------------------

outFile = "C:/Users/Flerlage/Cloud Drive/Documents/Ken/Blog/Famous Deaths/data.csv"
out = codecs.open(outFile, 'w', 'utf-8')
out.write ('Name,URL,Occupation,Occupation Detail,Birth,Death')
out.write('\n')

recordCount = 0

# Letter A is 493 and 000063304.
for pageLetter1 in range(493, 518):
    pageLetter2 = 62811 + pageLetter1
    pageLetter2string = "%09d" % pageLetter2
    pageURL = "http://www.nndb.com/lists/" + str(pageLetter1) + "/" + pageLetter2string
    page = requests.get(pageURL)
    
    if page.status_code==200:
        print("Downloaded from " + pageURL)
        soup = BeautifulSoup(page.content, 'html.parser')
        text = str(soup)
        text = text.replace('\n', '')
        text = text.replace('\r', '')
        textArray = text.split("<td ")
        recordType = ""

        for section in textArray:
            if recordType == "":
                # Not a known record, so check if it is a person record.
                pos = section.find("http://www.nndb.com/people/")
                if pos>0:
                    # This is a person record.
                    # Get URL
                    stringPart = section[pos:len(section)]
                    pos = stringPart.find('/">')
                    URL = stringPart[0:pos]

                    # Get Name
                    stringPart = stringPart[pos+3:len(stringPart)]
                    pos = stringPart.find("</a>")
                    personName = stringPart[0:pos]

                    # Next string will be Occupation
                    recordType = "Occupation"
            
            elif recordType == "Occupation":
                # Parse Occupation
                occName = section
                occName = occName.replace('align="center" valign="middle"><font size="-1">', '')
                occName = occName.replace('</font></td>', '')

                recordType = "Detailed"
                    
            elif recordType == "Detailed":
                # Parse Detailed Occupation
                detailedName = section
                detailedName = detailedName.replace('align="center" valign="middle"><font size="-1">', '')
                detailedName = detailedName.replace('</font></td>', '')

                recordType = "Birth"
                    
            elif recordType == "Birth":
                # Parse Birth Date
                birthDate = section
                birthDate = birthDate.replace('align="center" nowrap="" valign="middle"><tt>', '')
                birthDate = birthDate.replace('</tt></td>', '')

                recordType = "Death"
                    
            elif recordType == "Death":
                # Parse Death Date
                deathDate = section
                deathDate = deathDate.replace('align="center" nowrap="" valign="middle"><tt>', '')
                deathDate = deathDate.replace('</tt></td>', '')
                deathDate = deathDate.replace('</tr><tr>', '')
                pos = deathDate.find('</tr>')
                if pos > 0:
                    deathDate = deathDate[0:pos-1]

                # This is the last string for the full person, so write the record.
                recordString = '"' + personName + '","' + URL + '","' + occName + '","' + detailedName + '","' + birthDate + '","' + deathDate + '"'
                recordString = recordString.replace("<i>","")
                recordString = recordString.replace("</i>","")
                recordCount +=1
                if recordCount==913:
                    print(recordString)
                print("Writing record # " + str(recordCount))
                out.write (recordString)
                out.write('\n')
                recordType = ""
    else:
        # Failed to download the content.
        print("Failed to download from " + pageURL)

out.close()