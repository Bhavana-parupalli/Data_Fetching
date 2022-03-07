import pytest
import sqlite3
from project0 import project0

def test1_fetchincidents():
    url="https://www.normanok.gov/sites/default/files/documents/2022-02/2022-02-02_daily_incident_summary.pdf"
    data=project0.fetchincidents(url)
    assert data!=None
def test1_extractincidents():
    url = "https://www.normanok.gov/sites/default/files/documents/2022-02/2022-02-02_daily_incident_summary.pdf"
    data=project0.fetchincidents(url)
    incidents=project0.extractincidents(data)
    assert len(incidents)>0
def test1_createdb():
    db='normanpd.db'
    dbase=project0.createdb()
    assert dbase==db
def test1_populatedb():
    url = "https://www.normanok.gov/sites/default/files/documents/2022-02/2022-02-02_daily_incident_summary.pdf"
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
def test1_status():
    db=project0.createdb()
    url = "https://www.normanok.gov/sites/default/files/documents/2022-02/2022-02-02_daily_incident_summary.pdf"
    data = project0.fetchincidents(url)
    incidents=project0.extractincidents(data)
    project0.populatedb(db,incidents)
    project0.status(db)
    s=sqlite3.connect(db)
    cur=s.cursor()
    cur.execute('''select nature, count(nature)
                   from incidents
                   group by nature
                   order by count(nature) desc''')
    assert cur.fetchall()!=0


