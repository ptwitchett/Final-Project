from flask import Flask, request, redirect, url_for, render_template
from main import search_for_track, get_token, get_audio_features_for_tracks
from graph import plot_radar_chart
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Initialize an empty list to store track information (name, ID, artist)
track_info_list = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global track_info_list
    
    if request.method == 'POST':
        # Get the access token
        token = get_token()
 
        # Get the track name from the form submission
        track_name = request.form['track_name']

        # Call the search_for_track function with the access token and track name
        track_info = search_for_track(token, track_name)
        
        if track_info:
            # Add the track information (name, ID, artist) to the track_info_list
            track_info_list.extend(track_info)
    
    # Construct the HTML response
    response = "<h1>Music Visualiser</h1>"
    response += "<ul>To begin, enter song names and search. When you are done, submit"
    response += "<h2>Song list:</ul>"
    for track_info in track_info_list:
        response += f"<li>{track_info['name']} by {track_info['artist']}: {track_info['id']}</li>"
    response += "</ul>"
    
    # Render the form
    response += """
    <form method="post" action="/">
        <label for="track_name">Enter track name:</label>
        <input type="text" name="track_name" id="track_name">
        <button type="submit">Search</button>
    </form>
    """

    # Add button to trigger audio features retrieval
    response += """
    <form method="post" action="/get_audio_features">
        <button type="submit">submit</button>
    </form>
    """
    
    # Return the HTML response
    return response

@app.route('/get_audio_features', methods=['POST'])
def get_audio_features():
    # Get the access token
    token = get_token()
    
    # Extract track IDs from the stored track information
    track_ids = [track['id'] for track in track_info_list]
    
    # Get audio features for all track IDs
    audio_features = get_audio_features_for_tracks(token, track_ids)
    
    # Calculate the average of certain audio features
    if audio_features:
        # Define the audio features you want to calculate the average for
        features_to_average = ['danceability', 'energy', 'valence', 'loudness', 'tempo', 'instrumentalness']
        
        # Initialize dictionary to store sum of feature values
        feature_sum = {feature: 0.0 for feature in features_to_average}
        
        # Sum the feature values for all tracks
        for track_features in audio_features:
            for feature in features_to_average:
                feature_sum[feature] += track_features[feature]
        
        # Calculate the average for each feature
        feature_average = {feature: feature_sum[feature] / len(audio_features) for feature in features_to_average}
        
        print("Average Audio Features:", feature_average)
        
        # Plot radar chart for average audio features
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        plot_radar_chart(features_to_average, list(feature_average.values()), ax)
        
        # Convert the plot to base64 string
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode()
        
        # Close plot to prevent memory leaks
        plt.close()
        
        # Render radar chart in HTML response
        return render_template('radar_chart.html', radar_chart=img_base64)
    
    # Redirect back to the main page if no audio features are retrieved
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
