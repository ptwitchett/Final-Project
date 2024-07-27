#Imports
from flask import Flask, request, redirect, url_for, render_template
import pandas as pd
from collections import Counter
from main import search_for_track, get_token, get_audio_features_for_tracks, get_artist_details
from statistics import calculate_additional_statistics
from graph import create_lowest_std_scatter_plot, create_release_year_popularity_scatter_plot
from html_generator import generate_statistics_html, generate_song_details_html, generate_scatter_plot_explanation

app = Flask(__name__)

#empty global lists to store track information
track_info_list = []
search_results = []

#main route
@app.route('/', methods=['GET', 'POST'])
def index():
    global track_info_list, search_results

    if request.method == 'POST' and 'track_name' in request.form:
        #get the access token
        token = get_token()

        #get the track name from the user submission
        track_name = request.form['track_name']

        #call the search_for_track function with the access token and track name
        search_results = search_for_track(token, track_name)
    #renders index template passing on track info and search results
    return render_template('index.html', track_info_list=track_info_list, search_results=search_results, enumerate=enumerate)

@app.route('/add', methods=['POST'])
def add_track():
    global track_info_list, search_results

    #get the index of the track to add
    index = int(request.form['index'])

    #add the selected track to the track list if index value is valid
    if 0 <= index < len(search_results):
        track_info_list.append(search_results[index])

    #clear the search results ready for next search
    search_results = []

    #redirect back to the main page 
    return redirect(url_for('index'))

@app.route('/remove', methods=['POST'])
def remove_track():
    global track_info_list

    #get the index of the track to remove
    index = int(request.form['index'])

    #remove the track from the list of tracks
    if 0 <= index < len(track_info_list):
        track_info_list.pop(index)

    #redirect back to the main page
    return redirect(url_for('index'))

@app.route('/get_audio_features', methods=['POST'])
def get_audio_features():
    global track_info_list

    #get the access token
    token = get_token()

    #extract track ID and artist ID from the stored track information
    track_ids = [track['id'] for track in track_info_list]
    artist_ids = list(set(artist_id for track in track_info_list for artist_id in track['artist_ids']))

    #get audio features for all track IDs
    audio_features = get_audio_features_for_tracks(token, track_ids)

    #get artist's genres
    artist_details = get_artist_details(token, artist_ids)
    artist_genres = {artist['id']: artist['genres'] for artist in artist_details}

    #add genres to track information
    for track in track_info_list:
        track['genres'] = list(set(genre for artist_id in track['artist_ids'] for genre in artist_genres.get(artist_id, [])))

    #calculate the three most common genres
    all_genres = [genre for track in track_info_list for genre in track['genres']]
    genre_counts = Counter(all_genres)
    most_common_genres = [genre for genre, count in genre_counts.most_common(3)]

    #define features to display and analyze
    features_to_display = [
        'danceability', 'energy', 'valence', 'loudness', 'tempo', 
        'instrumentalness', 'key', 'duration_ms', 'liveness', 'mode',
        'release_date', 'popularity'
    ]

    #create a DataFrame for the defined features using pandas
    features_df = pd.DataFrame(audio_features, columns=features_to_display)
    #extracts release year from release_date
    features_df['release_date'] = [int(track_info['release_date'].split('-')[0]) for track_info in track_info_list]
    #extracts popuarity from track_info
    features_df['popularity'] = [track_info['popularity'] for track_info in track_info_list]

    #creates new dataframe with all numerical features (not genres)
    numeric_features_df = features_df.drop(columns=['genres'], errors='ignore')
    #normalises and calculates means and std for numerical features
    normalized_features_df, normalized_feature_means, normalized_feature_stds, additional_statistics = calculate_additional_statistics(numeric_features_df)

    #generate HTML for statistics and song details to be displayed 
    additional_stats_html, normalized_stats_html, weak_correlation_html, weak_features = generate_statistics_html(features_to_display, normalized_feature_means, normalized_feature_stds, additional_statistics)
    song_details_html = generate_song_details_html(track_info_list, most_common_genres)
    scatter_plot_explanation_html = generate_scatter_plot_explanation()

    #find the feature pairs with the lowest standard deviation
    scatter_chart_lowest_std, feature1, feature2 = create_lowest_std_scatter_plot(normalized_features_df)

    #create the scatter plot for release year vs popularity
    scatter_chart_release_popularity = create_release_year_popularity_scatter_plot(features_df)

    #renders correlation_results.html but with arguments for the previously generated html content above
    return render_template('correlation_results.html', 
                           correlation_table=additional_stats_html + song_details_html,
                           scatter_chart_lowest_std=scatter_chart_lowest_std, 
                           scatter_chart_release_popularity=scatter_chart_release_popularity,
                           weak_correlation_messages=weak_correlation_html,
                           normalized_statistics=normalized_stats_html,
                           feature1=feature1,
                           feature2=feature2,
                           weak_features=weak_features)

if __name__ == '__main__':
    app.run(debug=True)
