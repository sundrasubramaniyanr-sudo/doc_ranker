import streamlit as st
import sqlite3
from datetime import date
import pandas as pd

DB='ngo_system.db'
st.set_page_config(page_title='SANTHAM Home for Aged', page_icon='❤️', layout='wide')

def conn(): return sqlite3.connect(DB)
def init():
    c=conn(); x=c.cursor()
    x.execute('CREATE TABLE IF NOT EXISTS needs (id INTEGER PRIMARY KEY AUTOINCREMENT,item TEXT,quantity REAL,unit TEXT,status TEXT,date_added TEXT)')
    x.execute('CREATE TABLE IF NOT EXISTS donors (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,phone TEXT,email TEXT,date_registered TEXT)')
    x.execute('CREATE TABLE IF NOT EXISTS donations (id INTEGER PRIMARY KEY AUTOINCREMENT,donor TEXT,item TEXT,quantity REAL,unit TEXT,amount REAL,donation_date TEXT)')
    c.commit(); c.close()
def q(sql):
    c=conn(); d=pd.read_sql_query(sql,c); c.close(); return d
def e(sql,p):
    c=conn(); c.execute(sql,p); c.commit(); c.close()
init()

st.sidebar.title('SANTHAM')
st.sidebar.caption('Donation & Basic-Needs Management System')
page=st.sidebar.radio('Navigation',['Dashboard','Current Needs','Donors','Add Donation','Donation History','Reports'])

if page=='Dashboard':
    st.title(' SANTHAM Home for Aged'); st.subheader('Donation & Basic-Needs Management System')
    st.write('A simple digital system for organizing basic requirements and donation records.')
    n,d,do=q('SELECT * FROM needs'),q('SELECT * FROM donors'),q('SELECT * FROM donations')
    a,b,c,x=st.columns(4); a.metric('Elderly Residents','≈ 10'); b.metric('Open Requirements',int((n.status!='Completed').sum()) if not n.empty else 0); c.metric('Registered Donors',len(d)); x.metric('Donations Recorded',len(do))
    st.divider(); st.subheader('Current Requirements')
    st.dataframe(n[['item','quantity','unit','status','date_added']] if not n.empty else pd.DataFrame(),use_container_width=True,hide_index=True)

elif page=='Current Needs':
    st.title(' Current Needs')
    with st.form('need',clear_on_submit=True):
        a,b,c=st.columns(3); item=a.text_input('Item'); qty=b.number_input('Quantity',min_value=.1,step=1.); unit=c.text_input('Unit')
        if st.form_submit_button('Add Requirement'):
            if item and unit: e('INSERT INTO needs(item,quantity,unit,status,date_added) VALUES(?,?,?,?,?)',(item,qty,unit,'Needed',str(date.today()))); st.success('Requirement added.')
            else: st.error('Enter item and unit.')
    n=q('SELECT * FROM needs ORDER BY id DESC'); st.dataframe(n,use_container_width=True,hide_index=True)
    if not n.empty:
        sid=st.selectbox('Select requirement',n.id.tolist()); status=st.selectbox('New status',['Needed','Partially Received','Completed'])
        if st.button('Update Status'): e('UPDATE needs SET status=? WHERE id=?',(status,sid)); st.success('Status updated. Refresh if needed.')

elif page=='Donors':
    st.title('👤 Donor Registration')
    with st.form('donor',clear_on_submit=True):
        name=st.text_input('Donor Name'); phone=st.text_input('Phone'); email=st.text_input('Email')
        if st.form_submit_button('Register Donor'):
            if name: e('INSERT INTO donors(name,phone,email,date_registered) VALUES(?,?,?,?)',(name,phone,email,str(date.today()))); st.success('Donor registered.')
            else: st.error('Donor name is required.')
    st.dataframe(q('SELECT * FROM donors ORDER BY id DESC'),use_container_width=True,hide_index=True)

elif page=='Add Donation':
    st.title('Add Donation'); d=q('SELECT name FROM donors ORDER BY name'); opts=d.name.tolist() if not d.empty else ['Walk-in / Other']
    with st.form('donation',clear_on_submit=True):
        donor=st.selectbox('Donor',opts); item=st.text_input('Donated Item'); qty=st.number_input('Quantity',min_value=0.,step=1.); unit=st.text_input('Unit'); amount=st.number_input('Monetary Contribution (₹)',min_value=0.,step=100.); dd=st.date_input('Donation Date',date.today())
        if st.form_submit_button('Record Donation'):
            if item: e('INSERT INTO donations(donor,item,quantity,unit,amount,donation_date) VALUES(?,?,?,?,?,?)',(donor,item,qty,unit,amount,str(dd))); st.success('Donation recorded.')
            else: st.error('Enter donated item.')

elif page=='Donation History':
    st.title('📋 Donation History'); st.dataframe(q('SELECT * FROM donations ORDER BY donation_date DESC,id DESC'),use_container_width=True,hide_index=True)

else:
    st.title('📊 Reports'); d=q('SELECT * FROM donations')
    if d.empty: st.info('Add donations to see reports.')
    else:
        a,b=st.columns(2); a.metric('Total Monetary Contributions',f"₹{d.amount.sum():,.0f}"); b.metric('Donation Records',len(d))
        s=d.groupby('item',as_index=False).quantity.sum(); st.subheader('Donated Quantity by Item'); st.bar_chart(s.set_index('item'))

st.caption('Prototype — Community Connect Project | SANTHAM Home for Aged')
