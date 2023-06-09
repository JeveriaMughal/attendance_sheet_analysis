import datetime
import pandas as pd 
import streamlit as st 


def get_average(time_series):
    sum=0;
    for value in time_series:
        sum=sum+value
    average_in_time_seconds=sum/len(time_series)
    HH = int(average_in_time_seconds / 3600)
    MM = int((average_in_time_seconds - HH*3600) / 60)
    SS = int(average_in_time_seconds - HH*3600 - MM*60)
    return HH, MM , SS

def app():
    uploaded_file = st.file_uploader("Choose a .xls file",)
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file, engine='xlrd')
        names=df.Name.unique().tolist()
        df['Date'] = pd.to_datetime(df['Date/Time'], format='%d/%m/%Y %H:%M:%S %p').dt.date
        df['Time'] = pd.to_datetime(df['Date/Time'], format='%d/%m/%Y %I:%M:%S %p').dt.time
        dates=(df.Date.unique().tolist())
        for name in names:
            in_time =[]
            out_time=[]
            for date in dates:
                df1 = df.loc[(df['Name'] == name) & (df['Date'] == date)]
              
                in_out_times=df1.Time.values.tolist()
                for item in in_out_times:
                    item_seconds=item.hour*3600+item.minute*60+item.second
                    
                    if item < datetime.time(12, 0 , 0):
                        in_time.append(item_seconds)
                    else:
                        out_time.append(item_seconds)
            st.title(name)
            
            
            if len(in_time)>0:
                hh,mm,ss=get_average(in_time)
                st.write("Average Arrival Time",hh,":",mm,":",ss)
            if len(out_time)>0:
                hh1,mm1,ss1=get_average(out_time)
                st.write("Average Departure Time",hh1,":",mm1,":",ss1)

app()
