import numpy as np
import pandas as pd
import plotly.express as px


def fetch_medal_tally(df,years,country):
    medal_df = df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"])
    flag = 0
    if years == "Overall" and country == "Overall":
        temp_df = medal_df
    if years =="Overall" and country != "Overall":
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if years !="Overall" and country == "Overall":
        temp_df = medal_df[medal_df['Year'] == int(years)] 
    if years !="Overall" and country != "Overall":
        temp_df = medal_df[(medal_df['Year']== int(years)) & (medal_df['region']== country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    
    return x

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"])
    medal_tally=medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['total'] =medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')

    return years,country

def data_over_time(df,col):
    nations_over_time = df.drop_duplicates(['Year',col])['Year'].value_counts().sort_index().reset_index()
    nations_over_time.columns = ['Edition',col]
    return nations_over_time

def most_successful(df,Sport):
    temp_df = df.dropna(subset=['Medal'])

    if Sport !='Overall':
        temp_df= temp_df[temp_df['Sport']== Sport]

    x=temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on ='Name',right_on='Name',how='left')[['Name','count','Sport','region']].drop_duplicates('Name')
    x.rename(columns={'count':'Medal_Count','region':'Country'},inplace=True)
    return x