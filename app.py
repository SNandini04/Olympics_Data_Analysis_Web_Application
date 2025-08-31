import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.io as pio
import preprocessor,helpers
import matplotlib.pyplot as plt
import seaborn as sns
from theme_utilis import ThemeManager

st.set_page_config(layout="wide")

theme_manager = ThemeManager()
theme_manager.select_theme()   
theme_manager.apply_theme() 

df = pd.read_csv(r'dataset\athlete_events.csv')
region_df = pd.read_csv(r"dataset\noc_regions.csv")

df = preprocessor.preprocess(df,region_df)


st.sidebar.title('Olympics Analysis')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-Wise Analysis','Athlete Wise Analysis')
)



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

    st.sidebar.title('Overall Analysis')


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


    st.markdown('### Most Successful Athletes')
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport=st.selectbox('Select A Sport',sport_list)
    x = helpers.most_successful(df,selected_sport)
    st.table(x)


if user_menu == 'Country-Wise Analysis':
    st.title("🌍 Country-Wise Analysis")

    st.sidebar.title('Country-Wise Analysis')

    region_list=df['region'].dropna().unique().tolist()
    # region_list.sort()
    # region_list.insert(0,'Overall')

    selected_region=st.sidebar.selectbox('Select A Country',region_list)

    country_df=helpers.yearwise_medal_tally(df,selected_region)
    fig = px.line(country_df, x="Year", y="Medal", markers=True)
    st.title(selected_region + ' Medal Tally Over The Years')
    st.plotly_chart(fig)

   
    pt = helpers.country_wise_heatmap(df,selected_region)
    st.title(selected_region + ' Excels In The Following Sports ')
    if pt is not None and pt.shape[0] > 0 and pt.shape[1] > 0:
        fig, ax = plt.subplots(figsize=(20, 20))
        sns.heatmap(pt, annot=True,ax=ax)
        ax.set_title(f"Medals Heatmap for {selected_region}", fontsize=16, fontweight="bold")
        st.pyplot(fig)
    else:
        st.write("No valid medal heatmap available for this country.")


    st.title('Top 10 Athletes of ' + selected_region)
    top10_df = helpers.most_successful_regionwise(df,selected_region)
    st.table(top10_df)

if user_menu == 'Athlete Wise Analysis':
    st.title("🏅 Athlete-Wise Analysis")

    st.sidebar.title('Athlete-Wise Analysis')

    # athlete_country_list = df['region'].dropna().unique().tolist()
    # athlete_country_list.sort()
    # athlete_country_list.insert(0, 'Overall')

    # selected_country = st.sidebar.selectbox('Select a Country', athlete_country_list)
    athlete_df=df.drop_duplicates(subset=['Name','region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()

    fig=ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
    st.title('Distribution of Age')
    st.plotly_chart(fig)


    x = []
    name = []

    famous_sports = [
    'Basketball','Judo','Football','Tug-of-War','Athletics',
    'Swimming','Badminton','Sailing','Gymnastics',
    'Art Competition','Handball','Weightlifting','Wrestling',
    'Water Polo','Hockey','Rowing','Fencing',
    'Shooting','Boxing','Taekwondo','Cycling','Diving','Canoeing',
    'Tennis','Golf','Softball','Archery','Volleyball',
    'Synchronized Swimming','Table Tennis','Baseball',
    'Rhythmic Gymnastics','Rugby Sevens',
    'Beach Volleyball','Triathion','Rugby','Polo','Ice Hockey']

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        gold_ages = temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna()
        
        if not gold_ages.empty:
            x.append(gold_ages)
            name.append(sport)
    fig=ff.create_distplot(x,name,show_hist=False,show_rug=False) 
    st.title("Distribution Of Age With Respect To Sport[Gold Medalist]")
    st.plotly_chart(fig)




    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport=st.selectbox('Select A Sport',sport_list)
    temp_df = helpers.weight_height(df,selected_sport)
    fig,ax=plt.subplots()
    ax=sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.title('Height Vs Weight')
    st.pyplot(fig)

    st.title('Men Vs Women Participation Over The Years')
    final=helpers.men_vs_women(df)
    fig = px.line(final,x='Year',y=['Male','Female'])
    st.plotly_chart(fig)

