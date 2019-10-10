import requests
from lxml import html
import re
import pdfkit
import string
import os


def reader(link,start, last,folder):
#link = "https://www.wuxiaworld.com/novel/against-the-gods/atg-chapter-0"
        found =""
        f = requests.get(link)
        page = html.fromstring(f.text)
        p = html.tostring(page).decode('utf-8')

        
        p = p.replace("&#8220;" , '"')
        p = p.replace("&#8230;" , "...")
        p = p.replace("&#8221;" , '"')
        p = p.replace("&#8217;" , "'")
        p = p.replace("&#8211;" , "-")
        
        lines = p.splitlines()
        
        for i in range(len(lines)):
                if lines[i] == '<div class="fr-view">':
                        found = lines[i+1]
                        break
                
        for i in range(len(lines)):
                if '/images/arrow-right.png' in lines[i]:
                        nextchap = lines[i-1]
                        nextchap = re.search('"(.*)" class', nextchap).group(1)
                        nextchap = "https://www.wuxiaworld.com" + nextchap
                        break
                
        found = found.replace("</p><p>" , "\n\n")
        found = found.replace("<p>" , "")
        found = found.replace("</p>" , "")
        found = found.replace("<strong>" , "")
        found = found.replace("</strong>" , "")
        name = found.splitlines()[0]
        
        
        if(("Chapter" not in name) or ("Previous" in name) or (len(name) > 45)):
                name = "Chapter "+str(start)
                
        name = name.translate(str.maketrans('', '', string.punctuation))

        found = '\n'.join(found.splitlines()[1:])
        found = '\n'.join(found.splitlines()[:-3])


        file = open(folder + "/" +name + ".html", "w+")
        file.write(r'<style>p { font-family: Palatino, "Palatino Linotype", "Palatino LT STD", "Book Antiqua", Georgia, serif; font-size: 20px; font-style: normal; font-variant: normal; font-weight: 400; line-height: 25px; }</style>')
        file.write("<h2><strong><center>" + name + "</center></strong></h2>" + "<br>")
        file.write("<p>" + found.replace("\n\n" , "</p><p>") + "</p>")
        file.close()

        

        options = {
        'page-size': 'Executive',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        }
        path_wkthmltopdf = r'C:\\Program Files\\wkhtmltopdf\bin\\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
        pdfkit.from_file(folder + r'/' +name + ".html",folder + r'/' + name + ".pdf", options = options,configuration=config)
        os.remove(folder + "/" +name + ".html")
        if(start == last):
                return False
        else:
                print(nextchap)
                return reader(nextchap,start+1,last,folder)
      


folder = str(input())
link = str(input())
start = int(input())
last = int(input())
print(reader(link,start,last,folder))
