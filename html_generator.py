def generate_statistics_html(features_to_display, normalized_feature_means, normalized_feature_stds, additional_statistics):
    statistics_html = "<ul>"
    for feature in features_to_display:
        if feature not in ['genres']:
            statistics_html += f"<li>{feature} - Normalized Mean: {normalized_feature_means[feature]:.2f}, Normalized Std Dev: {normalized_feature_stds[feature]:.2f}</li>"
    statistics_html += "</ul>"

    additional_stats_html = "<h2>Additional Statistics</h2>"

    #tempo section
    additional_stats_html += "<h3>Tempo</h3>"
    additional_stats_html += f"<p>Average Tempo: {additional_statistics['average_tempo']:.2f} BPM (Range: {additional_statistics['min_tempo']:.2f} - {additional_statistics['max_tempo']:.2f} BPM)</p>"

    #release years section
    additional_stats_html += "<h3>Release Years</h3>"
    additional_stats_html += f"<p>Average Release Year: {additional_statistics['average_release_year']:.0f}</p>"
    additional_stats_html += f"<p>Song span: {additional_statistics['min_release_year']} to {additional_statistics['max_release_year']} ({additional_statistics['span_decades']} decades)</p>"
    additional_stats_html += "<p>Most Common Decades: "
    additional_stats_html += ", ".join([f"{decade}s" for decade in additional_statistics['most_common_decades']])
    additional_stats_html += "</p>"

    #popularity section
    additional_stats_html += "<h3>Popularity</h3>"
    additional_stats_html += "<p>Popularity is a measure from 0 to 100 indicating how popular a track is based on the total number of plays. A higher value indicates a more popular track. Spotify calculates this value by considering the number of plays and how recent those plays are.</p>"
    additional_stats_html += f"<p>Average Popularity: {additional_statistics['average_popularity']:.2f}</p>"
    additional_stats_html += f"<p>Popularity Range: {additional_statistics['min_popularity']} to {additional_statistics['max_popularity']}</p>"
    additional_stats_html += f"<p>{additional_statistics['popularity_comment']}</p>"

    #song duration section
    additional_stats_html += "<h3>Song Duration</h3>"
    avg_duration = additional_statistics['average_duration']
    shortest_duration = additional_statistics['shortest_duration']
    longest_duration = additional_statistics['longest_duration']
    additional_stats_html += f"<p>Average Song Duration: {avg_duration[0]} minutes and {avg_duration[1]} seconds</p>"
    additional_stats_html += f"<p>Shortest Song Duration: {shortest_duration[0]} minutes and {shortest_duration[1]} seconds</p>"
    additional_stats_html += f"<p>Longest Song Duration: {longest_duration[0]} minutes and {longest_duration[1]} seconds</p>"

    #other features section
    additional_stats_html += "<h3>Other Features</h3>"
    additional_stats_html += f"<p>{additional_statistics['instrumental_message']}</p>"
    additional_stats_html += f"<p>{additional_statistics['mode_message']}</p>"
    additional_stats_html += f"<p>{additional_statistics['key_message']}</p>"

    weak_correlation_html = ""
    weak_features = []
    if additional_statistics['weak_correlation_messages']:
        weak_correlation_html += "<ul>"
        for message in additional_statistics['weak_correlation_messages']:
            weak_correlation_html += f"<li>{message}</li>"
            weak_features.append(message.split(' ')[0].lower())
        weak_correlation_html += "</ul>"

    return additional_stats_html, statistics_html, weak_correlation_html, weak_features

def generate_song_details_html(track_info_list, most_common_genres):
    song_details_html = "<h2>Song Details</h2>"
    song_details_html += "<ul>"
    for track_info in track_info_list:
        song_details_html += (f"<li>{track_info['name']} by {track_info['artist']} "
                              f"(Album: {track_info['album']}, Released: {track_info['release_date']}, "
                              f"Popularity: {track_info['popularity']})</li>")
    song_details_html += "</ul>"
    song_details_html += "<h2>Most Common Genres</h2>"
    song_details_html += "<ul>"
    for genre in most_common_genres:
        song_details_html += f"<li>{genre}</li>"
    song_details_html += "</ul>"

    return song_details_html

def generate_scatter_plot_explanation():
    explanation_html = "<h2>Scatter Plot Explanation</h2>"
    explanation_html += "<p>This graph shows the two audio features with the strongest correlation between the input songs.</p>"
    return explanation_html
