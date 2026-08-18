import streamlit as st
import pandas as pd
import preprocessor, processor
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

st.set_page_config(layout="wide")

data = pd.read_csv('datasets/athlete_events.csv')
reg_data = pd.read_csv('datasets/noc_regions.csv')
data = preprocessor.preprocess(data, reg_data)

st.sidebar.title('Olympics Dashboard')
ana_type = st.sidebar.radio('Select the analysis type :-', ['Medal Total Tally', 'Overall Analysis', 'Country Wise Analysis', 'Athlete Wise Analysis'])


if ana_type == 'Medal Total Tally':
    st.sidebar.subheader('Medal Tally')

    year, country = processor.year_country(data)

    user_year = st.sidebar.selectbox("Select Year :-", year)
    user_country = st.sidebar.selectbox("Select Country :-", country)
    user_season = st.sidebar.radio('Select Season :-', ['Summer', 'Winter'])

    if (user_country == 'All') and (user_year == 'Overall'):
        st.title(f'Overall Medal Tally of All the Countries in {user_season} Olympics')
    elif (user_country != 'All') and (user_year != 'Overall'):
        st.title(f'Athletes from {user_country} who won in {user_year} {user_season} Olympics')
    elif (user_country != 'All') and (user_year == 'Overall'):
        st.title(f'Olympic Medals won by {user_country} over the Years')
    elif (user_country == 'All') and (user_year != 'Overall'):
        st.title(f'Countries Performance in the {user_year} {user_season} Olympics')

    st.table(processor.select(data, user_season, user_country, user_year))

elif ana_type == 'Overall Analysis':
    st.title("Overall Analysis of Olympics")

    col1,col2,col3 = st.columns(3)
    with col1:
        st.write('##### Editions')
        st.header(data['Year'].unique().shape[0])
    with col2:
        st.write('##### Hosts')
        st.header(data['City'].unique().shape[0])
    with col3:
        st.write('##### Nations')
        st.header(data['Region'].unique().shape[0])

    col1,col2,col3 = st.columns(3)
    with col1:
        st.write('##### Sports')
        st.header(data['Sport'].unique().shape[0])
    with col2:
        st.write('##### Events')
        st.header(data['Event'].unique().shape[0])
    with col3:
        st.write('##### Athletes')
        st.header(data['Name'].unique().shape[0])
    #
    #
    st.header('Trend Over the Years in Olympics')
    col1,col2 = st.columns([2,1])
    user_criteria = col1.selectbox('Criteria to Plot Against :', ['Countries', 'Events', 'Athletes'])
    user_season = col2.selectbox('Season :', ['Summer', 'Winter', 'Both'])

    crit_year = processor.plotly_graph(data, user_criteria, user_season)
    fig = px.line(crit_year, x='Year', y=user_criteria)
    st.plotly_chart(fig)
    #
    #
    st.header('No. of Events Across the Years (per Sport)')
    heat_user_season = st.selectbox('', ['Summer Season', 'Winter Season', 'Both Seasons'])

    fig, axes = plt.subplots(figsize=(25, 25))
    ax = sns.heatmap(processor.event_table(data, heat_user_season), annot=True, cmap='YlGnBu')
    st.pyplot(fig)
    #
    #
    st.header('Top 25 Most Successful Athletes of All Time')
    all_sport = sorted(data['Sport'].unique().tolist())
    all_sport.insert(0, 'Overall')
    user_sport = st.selectbox('Choose Sport :', all_sport)
    st.table(processor.success_athletes(data, user_sport))

elif ana_type == 'Country Wise Analysis':

    st.sidebar.header('Country Wise Analysis of Olympics')
    country = sorted(data['Region'].unique().tolist())
    user_country = st.sidebar.selectbox('Select Country :', country)
    user_season = st.sidebar.radio('Select Season :', ['Summer', 'Winter', 'Both'])

    medal_graph, medal_table = processor.medals_graph_table(data, user_season, user_country)

    st.title(f"{user_country}'s Medal Tally in {user_season} Olympics")
    chart = px.line(medal_graph, x='Year', y='Medals')
    st.plotly_chart(chart)
    #
    #
    st.title(f"{user_country}'s Performance in Every Sport in {user_season} Olympics")
    st.write('')
    fig, axes = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(medal_table, annot=True)
    st.pyplot(fig)
    #
    #
    st.title(f'Top 15 Most Successful Athletes from {user_country}')
    st.write('')
    st.table(processor.top_15_athletes(data, user_country))

elif ana_type == 'Athlete Wise Analysis':
    athlete_df = data.drop_duplicates(subset=['Name', 'Region'])

    x1 = athlete_df['Age']
    x2 = athlete_df[athlete_df['Gold'] == 1]['Age']
    x3 = athlete_df[athlete_df['Silver'] == 1]['Age']
    x4 = athlete_df[athlete_df['Bronze'] == 1]['Age']

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Gold'] == 1]['Age'])
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = data['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = processor.weight_v_height(data,selected_sport)
    fig,axes = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    user_season = st.selectbox('Select Season :', ['Summer Olympics', 'Winter Olympics', 'Both'])
    final = processor.men_vs_women(data, user_season)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)