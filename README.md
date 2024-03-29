# cs5293sp22-project0
## Author: Bhavana Parupalli 
## Packages installed
```bash
  pipenv install PyPDF2
  pipenv install pandas
  pipenv install pytest
  import tempfile
  import re
  import urllib
  import sqlite3
  import argparse
  import pytest
```
## project0
### project0.py
The project0.py contains five different methods to fetch data from the url, extract incidents from the pdf file, creating a database, connecting to database and inserting data into the database and finally displaying the nature of incidents and the count for each incident.
#### fetchincidents(url)
The fetchincidents function will take url as argument and it fetches information from the url using 'urllib' package. This function returns the bytes data.
#### extractincidents(data)
The extractincidents function will take the data returned from the fetchincidents() function as argument and then it writes the data into a temporary file, with the help of 'PyPDF2' package it extracts the first page of pdf document. Then splitting each line using '\n' and then adding in to the list. As the first page of pdf contains column names and the end of the page contains date and time. So, slicing is used to remove those from the list. The commands used are as follows:
```bash
l=[]
pg=[]
    for i in page1.split('\n'):
        pg.append(i)
    pg=pg[5:-3]
    l.append(pg)
```
Secondly, extracting the entire pdf starting from page 2. Then splitting the extracted text using '\n' and appending each page of pdf as a sublist into a list as mentioned below.
```bash
for pagenum in range(1, pagecount):
    p = pdfReader.getPage(pagenum).extractText()
    l1=[]
    for i in p.split('\n'):
        l1.append(i)
    l.append(l1)
```
Assumptions made in this step are looping through the above list, if 'OK0140200' or 'EMSSTAT' or '14005' is found then it will append until the found value and then this sublist is added to a list and again a empty sublist is created. Commands are mentioned below.
```bash
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
```
Assumptions made in this step are some of the rows contains missing values. So, these missing values are replaced with 'nan'. After going through some pdf's i found that incident_location and nature have missing values. So, as each row is stored as a sublist, the sublist is looped and if the length of the sublist is 4 then, it will check whether index 2 of the sublist is uppercase then insert 'nan' value at index 3, else insert at index 2. If the length of the sublist is 3 then it will insert 'nan' values at index 2 and 3 as given below.
```bash
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
```
Assumptions made in this step are few sublists have length 6 because the incident_location column contain location names split into 2 lines. So, in order to concatenate the two strings and remove the concatenated string the code implemented is shown below.
```bash
a=0
for i in l3:
    if len(i)==6:
        l3[a][2]=l3[a][2]+l3[a][3]
        l3[a].pop(3)
    a+=1
```
Finally, the extractincidents function will return a list in which each sublist contain each row values.
#### createdb()
The createdb function will create a database named 'normanpd.db'. The sqlite3 package opens a connection creating a normanpd.db database file. Using execute commands if incidents table exits in the database then the table is dropped. Followed by it will create a incidents table. Lastly, it returns the database. The commands used are mentioned below.
```bash
db=sqlite3.connect(dbase)
cur = db.cursor()
cur.execute('''DROP TABLE IF EXISTS incidents''')
cur.execute('''CREATE TABLE IF NOT EXISTS incidents (
             incident_time TEXT,
             incident_number TEXT,
             incident_location TEXT,
             nature TEXT,
             incident_ori TEXT)''')
```
#### populatedb(db,incidents)
The populatedb function takes db argument from createdb function and incidents argument from extractincidents function. This function open connection to 'normanpd.db' database and inserts data from the incidents into the database.
```bash
datab=sqlite3.connect(db)
cur=datab.cursor()
for i in range(0,len(incidents)):
    cur.execute('''INSERT INTO incidents(incident_time, incident_number, incident_location, nature, incident_ori)
                                        VALUES(?,?,?,?,?)''', incidents[i])
```
#### status(d)
The status function takes database as argument from createdb function. Then it selects the nature column from incidents table and counts occurence of each nature and then ordering the count in descending order. Finally, printing the each nature and it's count seperated by '|' symbol. Commands are as follows.
```bash
cur.execute('''select nature, count(nature)
                from incidents
                group by nature
                order by count(nature) desc''')
for i in cur.fetchall():
    print(i[0],'|',i[1])
```
### main.py
In main.py file project0 is imported. The main.py contains function calls to all the functions present in project0.py. The functions are called using the commands below.
```bash
incident_data = project0.fetchincidents(url)
incidents = project0.extractincidents(incident_data)
db = project0.createdb()
project0.populatedb(db, incidents)
project0.status(db)
``` 
### project0 execution
After connecting to the instance using SSH.

Clone the repository: https://github.com/Bhavana-parupalli/cs5293sp22-project0

Give the following command in command line.
```bash
pipenv run python project0/main.py --incidents <url>
```
## tests
### test_1.py
The test_1.py contains different test cases to test the functions present inside the project0.py. The test_1.py returns the passed and failed test cases.
#### test1_fetchincidents()
The test1_fetchincidents function passes the url to the fetchincidents function which is present inside the project0.py and gets the bytes data from the url. If the data is fetched then test1_fetchincidents() test case is passed else failed. The commands are as follows.
```bash
data=project0.fetchincidents(url)
assert data!=None
```
#### test1_extractincidents()
The test1_extractincidents function passes the url to the fetchincidents() and the fetched data is passed as an argument to the extractincidents function in project0.py and extracts the list of incidents. If length of extracted list is greater than 0, test case will pass else fail.
```bash
data=project0.fetchincidents(url)
incidents=project0.extractincidents(data)
assert len(incidents)>0
```
#### test1_createdb()
The test1_createdb function calls the createdb() from the project0.py. The createdb() from project0.py returns 'normanpd.db'. The test1_createdb() compares the string returned from the project0.py with 'normanpd.db'. If both are similar then test case pass else fail. The commands are mentioned below.
```bash
db='normanpd.db'
dbase=project0.createdb()
assert dbase==db
```
#### test1_populatedb()
The test1_populatedb function passes the url to the fetchincidents() and the data returned from the funtion is passed as an argument to the extractincidents() in project0.py. Followed by, using createdb() datbase 'normanpd.db' is created. The incidents extracted from extractincidents() and 'normanpd.db' are passed as an argument to the populatedb(). The populatedb() will insert all the rows into the database. The commands are as follow.
```bash
data = project0.fetchincidents(url)
incidents=project0.extractincidents(data)
datab=project0.createdb()
db=project0.createdb()
project0.populatedb(datab,incidents)
s=sqlite3.connect(db)
cur=s.cursor()
cur.execute('''select *
                from incidents''')
assert cur.fetchall()!=0
```
#### test1_status()
The test1_status function will perfom same as test1_populatedb() additionally it selects the nature and it's count in descending order as shown below.
```bash
cur.execute('''select nature, count(nature)
                from incidents
                group by nature
                order by count(nature) desc''')
assert cur.fetchall()!=0
```
### Test cases execution
After connecting to the instance using SSH.

clone the repository: git clone https://github.com/Bhavana-parupalli/cs5293sp22-project0

Finally, run the below command in command line
```bash
pipenv run pytest
```
