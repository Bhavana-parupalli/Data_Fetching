
import PyPDF2
import pandas as pd
import tempfile
import re
import datetime
import sqlite3
import urllib
from urllib.request import urlopen, Request
import ssl

def fetchincidents(url):
    #url = ("https://www.normanok.gov/sites/default/files/documents/2022-02/2022-02-02_daily_incident_summary.pdf")
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    ssl._create_default_https_context = ssl._create_unverified_context
    data = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read()
    return data

def extractincidents(data):
    fp = tempfile.TemporaryFile()
    # Write the pdf data to a temp file
    fp.write(data)
    # Set the curser of the file back to the begining
    fp.seek(0)
    # Read the PDF
    pdfReader = PyPDF2.pdf.PdfFileReader(fp)
    pagecount = pdfReader.getNumPages()
    # Get the first page
    page1 = pdfReader.getPage(0).extractText()
    pg=[]
    for i in page1.split('\n'):
        pg.append(i)
    pg=pg[5:-3]
    # Now get all the other pages
    l=[]
    l.append(pg)
    for pagenum in range(1, pagecount):
        p = pdfReader.getPage(pagenum).extractText()
        l1=[]
        for i in p.split('\n'):
            l1.append(i)
        l.append(l1)
    c=0
    l2=[]
    l3=[]
    for i in l:
        a=len(i)
        for j in range(0,a):
            if l[c][j]=='OK0140200':
                l2.append(l[c][j])
                l3.append(l2)
                l2=[]
            elif l[c][j]=='EMSSTAT':
                l2.append(l[c][j])
                l3.append(l2)
                l2=[]
            elif l[c][j]=='14005':
                l2.append(l[c][j])
                l3.append(l2)
                l2=[]
            elif l[c][j]!='':
                l2.append(l[c][j])
        c+=1
    a=0
    for i in l3:
        k=len(i)
        if k!=5:
            if k==4:
                if l3[a][2].isupper()!=True:
                    l3[a].insert(2,'nan')
                elif l3[a][2].isupper()==True:
                    l3[a].insert(3,'nan')
            elif k==3:
                l3[a].insert(2,'nan')
                l3[a].insert(3,'nan')
        a+=1
    a=0
    for i in l3:
        if len(i)==6:
            l3[a][2]=l3[a][2]+l3[a][3]
            l3[a].pop(3)
        a+=1
    return l3

def createdb():
    try:
        dbase='normanpd.db'
        db=sqlite3.connect(dbase)
        cur = db.cursor()
        cur.execute('''DROP TABLE IF EXISTS incidents''')
        cur.execute('''CREATE TABLE IF NOT EXISTS incidents (
             incident_time TEXT,
             incident_number TEXT,
             incident_location TEXT,
             nature TEXT,
             incident_ori TEXT)''')
        db.commit()
        db.close()
        return dbase
    except ERROR as e:
        print(e)

def populatedb(db,incidents):
    datab=sqlite3.connect(db)
    cur=datab.cursor()
    for i in range(0,len(incidents)):
        cur.execute('''INSERT INTO incidents(incident_time, incident_number, incident_location, nature, incident_ori)
                                        VALUES(?,?,?,?,?)''', incidents[i])
    datab.commit()
    cur.execute('''select  *
                   from incidents''')
    df=pd.DataFrame(cur.fetchall(),columns=['incident_time','incident_number','incident_location','nature','incident_ori'])

def status(d):
    datab=sqlite3.connect(d)
    cur=datab.cursor()
    cur.execute('''select nature, count(nature)
                   from incidents
                   group by nature
                   order by count(nature) desc''')
    for i in cur.fetchall():
        print(i[0],'|',i[1])
    return cur.fetchall()





