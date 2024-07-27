import plotly.express as px
import json
import plotly

def create_lowest_std_scatter_plot(normalized_features_df):
    #find the two features with the lowest standard deviation
    selected_features = ['danceability', 'energy', 'valence', 'loudness']
    std_devs = normalized_features_df[selected_features].std()
    lowest_std_features = std_devs.nsmallest(2).index

    #create scatter plot for these two features
    scatter_fig = px.scatter(
        normalized_features_df, x=lowest_std_features[0], y=lowest_std_features[1],
        labels={lowest_std_features[0]: lowest_std_features[0].capitalize(), lowest_std_features[1]: lowest_std_features[1].capitalize()},
        title=f'{lowest_std_features[0].capitalize()} vs {lowest_std_features[1].capitalize()}'
    )
    #set axis ranges from 0 to 1 for clarity
    scatter_fig.update_layout(xaxis_range=[0, 1], yaxis_range=[0, 1])  
    scatter_chart = json.dumps(scatter_fig, cls=plotly.utils.PlotlyJSONEncoder)

    return scatter_chart, lowest_std_features[0], lowest_std_features[1]

def create_release_year_popularity_scatter_plot(df):
    #create scatter plot for release years vs popularity
    fig = px.scatter(df, x='release_date', y='popularity', title='Release Year vs Popularity', labels={'release_date': 'Release Year', 'popularity': 'Popularity'})
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
