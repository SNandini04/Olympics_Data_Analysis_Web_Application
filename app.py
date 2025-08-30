import streamlit as st
import pandas as pd
import plotly.express as px
import preprocessor,helpers
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r'dataset\athlete_events.csv')
region_df = pd.read_csv(r"dataset\noc_regions.csv")

df = preprocessor.preprocess(df,region_df)


st.sidebar.title('Olympics Analysis')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-Wise Analysis','Athlete Wise Analysis')
)

# st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years,country = helpers.country_year_list(df)
    selected_year=st.sidebar.selectbox('Select Year',years)
    selected_country = st.sidebar.selectbox('Select Country',country)
    medal_tally = helpers.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year !="Overall" and selected_country =="Overall":
        st.title('Medal Tally In ' +  str(selected_year)  + "  Olympics")
    if selected_year =="Overall" and selected_country !="Overall":
        st.title(selected_country + " Overall Performance")
    if selected_year !="Overall" and selected_country !="Overall":
        st.title(selected_country + " Performance In " + str(selected_year) + " Olympics")
    st.table(medal_tally)


if user_menu == "Overall Analysis":
    st.title("🏅 Olympics Overall Analysis")
    # st.markdown("Explore the history and growth of the Olympics with interactive insights.")

    Editions = df['Year'].unique().shape[0]-1
    Cities = df['City'].unique().shape[0]
    Sports = df['Sport'].unique().shape[0]
    Events = df['Event'].unique().shape[0]
    Athletes = df['Name'].unique().shape[0]
    Nations = df['region'].unique().shape[0]

    st.markdown("### Top Statistics")

    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Total Editions", Editions)
    with col2: st.metric("Host Cities", Cities)
    with col3: st.metric("Sports", Sports)

    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Events", Events)
    with col2: st.metric("Athletes", Athletes)
    with col3: st.metric("Nations", Nations)

    st.markdown("---")

    st.markdown("### Participating Nations Over Time")
    nations_over_time = helpers.data_over_time(df,'region')
    fig = px.line(nations_over_time, x="Edition", y='region', markers=True)
    st.plotly_chart(fig)

    st.markdown("### Events Over Time")
    events_over_time = helpers.data_over_time(df,'Event')
    fig = px.line(events_over_time, x="Edition", y='Event', markers=True)
    st.plotly_chart(fig)

    st.markdown("### Athletes Over Time")
    athletes_over_time = helpers.data_over_time(df,'Name')
    fig = px.line(athletes_over_time, x="Edition", y='Name', markers=True)
    st.plotly_chart(fig)

    st.markdown('### No. Of Events Over Time (Every Sport)')
    fig,ax = plt.subplots(figsize=(20,20))
    x=df.drop_duplicates(['Year','Sport','Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)


    st.markdown('Most Successful Athletes')
    x = helpers.most_successful(df,'Overall')
    st.table(x)