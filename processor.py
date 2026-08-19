import pandas as pd

def total_tally(data):

    medal_tally = data.drop_duplicates(
        subset=['Team', 'NOC', 'Year', 'Season', 'City', 'Sport', 'Event', 'Region', 'Bronze', 'Gold', 'Silver']).copy()

    return medal_tally

def year_country(data, season):
    if season == 'Summer':
        data = data[data['Season'] == 'Summer']
    else:
        data = data[data['Season'] == 'Winter']

    year = sorted(data['Year'].unique().tolist(), reverse=True)
    year.insert(0, 'Overall')
    country = sorted(data['Region'].unique().tolist())
    country.insert(0, 'All')

    return year, country

def select(data, user_season, user_country, user_year):

    if user_season == 'Summer':
        new_data = data[data['Season']=='Summer']
    else:
        new_data = data[data['Season']=='Winter']

    tally = total_tally(new_data)

    if (user_country == 'All') and (user_year == 'Overall'):
        temp_df = tally.groupby('Region', observed=True)[['Gold', 'Silver', 'Bronze', 'Total']].sum().sort_values(['Gold', 'Total'], ascending=False).reset_index()
    elif (user_country != 'All') and (user_year != 'Overall'):
        temp_df = new_data[(new_data['Year']==user_year) & (new_data['Region']==user_country) & (new_data['Total']==1)].reset_index(drop=True)
    elif (user_country != 'All') and (user_year == 'Overall'):
        temp_df = tally[tally['Region']==user_country].groupby('Year', observed=True)[['Gold', 'Silver', 'Bronze', 'Total']].sum().sort_values('Year').reset_index()
    elif (user_country == 'All') and (user_year != 'Overall'):
        temp_df = tally[tally['Year']==user_year].groupby('Region', observed=True)[['Gold', 'Silver', 'Bronze', 'Total']].sum().sort_values(['Gold', 'Total'], ascending=False).reset_index()
    else:
        temp_df = tally

    return temp_df.reset_index()

def plotly_graph(data, criteria, season):
    x = data.rename(columns={'Region':'Countries', 'Event':'Events', 'Name':'Athletes'})
    x = x.drop_duplicates(['Year', criteria])

    if season == 'Summer':
        new_data = x[x['Season'] == 'Summer']
    elif season == 'Winter':
        new_data = x[x['Season'] == 'Winter']
    else:
        new_data = x

    crit_year = new_data.groupby('Year')[criteria].count().reset_index().sort_values('Year')

    return crit_year

def event_table(data, season):
    if season == 'Summer Season':
        new_data = data[data['Season'] == 'Summer']
    elif season == 'Winter Season':
        new_data = data[data['Season'] == 'Winter']
    else:
        new_data = data

    df = new_data.drop_duplicates(['Year', 'Event'])
    table = df.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count', observed=True).fillna(
        0).astype('int')

    return table

def success_athletes(data, sport):
    medalist = data[data['Total'] == 1]

    if sport != 'Overall':
        x = medalist[medalist['Sport']==sport].groupby(by=['Name', 'Sport', 'Region'], observed=True).agg(
            {'Gold':'sum', 'Silver':'sum', 'Bronze':'sum', 'Total':'sum'}).sort_values(by=['Gold', 'Total'],ascending=False).reset_index()
    else:
        x = medalist.groupby(by=['Name', 'Sport', 'Region'], observed=True).agg(
            {'Gold':'sum', 'Silver':'sum', 'Bronze':'sum', 'Total':'sum'}).sort_values(by=['Gold', 'Total'],ascending=False).reset_index()

    return x.reset_index().head(25)

def medals_graph_table(data, season, country):
    no_repeat = data.drop_duplicates(
        subset=['Team', 'NOC', 'Year', 'Season', 'City', 'Sport', 'Event', 'Region', 'Bronze', 'Gold', 'Silver']).copy()
    no_repeat.rename(columns={'Total': 'Medals'}, inplace=True)

    if season == 'Summer':
        new_data = no_repeat[no_repeat['Season'] == 'Summer']
    elif season == 'Winter':
        new_data = no_repeat[no_repeat['Season'] == 'Winter']
    else:
        new_data = no_repeat

    count_medal_graph = new_data[new_data['Region'] == country].groupby(by='Year')['Medals'].sum().reset_index()

    count_sport_table = new_data[new_data['Region'] == country].pivot_table(
        index='Sport', columns='Year', values='Medals',aggfunc='sum', observed=True).fillna(0).astype('int')

    return count_medal_graph, count_sport_table

def top_15_athletes(data, country):
    medalist = data[data['Total'] == 1]

    top_15 = medalist[medalist['Region'] == country].groupby(by=[
        'Name', 'Sex', 'Season', 'Sport'],observed=True).agg({'Gold': 'sum', 'Silver': 'sum', 'Bronze': 'sum', 'Total': 'sum'
                                                            }).sort_values(['Gold', 'Total'],ascending=False).reset_index()

    return top_15.reset_index().head(15)

def weight_v_height(data,sport):
    df = data.copy()
    df['Medal'] = pd.from_dummies(data.loc[:, ['Gold', 'Silver', 'Bronze']], default_category='No Medal')

    athlete_df = df.drop_duplicates(subset=['Name', 'Region'])

    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
    else:
        temp_df = athlete_df

    return temp_df

def men_vs_women(data, season):

    if season == 'Summer Olympics': df = data[data['Season'] == 'Summer']
    elif season == 'Winter Olympics': df = data[data['Season'] == 'Winter']
    else : df = data

    athlete_df = df.drop_duplicates(subset=['Name', 'Region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final