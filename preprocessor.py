import pandas as pd

def preprocess(data, reg_data):
    reg_data.loc[[168, 208, 213], 'region'] = ['Refugee Olympic Team', 'Tuvalu', 'Unknown']

    data = data.merge(reg_data, on='NOC', how='left')

    data['Age'] = data['Age'].fillna(data['Age'].mean())

    data.loc[data['NOC'] == 'SGP', 'region'] = 'Singapore'

    data['Height'] = data['Height'].fillna(data['Height'].mean())
    data['Weight'] = data['Weight'].fillna(data['Weight'].mean())

    data = data.drop(columns=['Games', 'notes'])
    data = data.astype(
        {'Sex':'category', 'Age':'int', 'Team': 'category', 'NOC': 'category', 'Season': 'category', 'City': 'category', 'Event': 'category',
         'region': 'category', 'Sport': 'category'})

    data = data.astype({'Weight':'int', 'Height':'int'})

    data = data.drop_duplicates()
    data = data.drop(columns=['ID'])
    # data = data.sort_values('Year').reset_index(drop=True)

    data = data.rename(columns={'region':'Region'})

    data = pd.get_dummies(data, columns=['Medal'], dtype='int')
    data = data.rename(columns={'Medal_Bronze': 'Bronze', 'Medal_Gold': 'Gold', 'Medal_Silver': 'Silver'})
    data['Total'] = data['Gold'] + data['Silver'] + data['Bronze']

    data = data.reindex(columns=['Name', 'Sex', 'Age', 'Height','Weight','Team','NOC','Year','Season','City','Sport','Event','Region','Gold','Silver','Bronze','Total'])

    return data