import pandas as pd
from normalization import normalize_features, calculate_statistics

#dictionary mapping numerical values from spotiy to corresponding keys
KEY_NAMES = {
    0: "C",
    1: "C#/Db",
    2: "D",
    3: "D#/Eb",
    4: "E",
    5: "F",
    6: "F#/Gb",
    7: "G",
    8: "G#/Ab",
    9: "A",
    10: "A#/Bb",
    11: "B"
}
#function to convert millisecond song durations to minutes and seconds
def ms_to_min_sec(milliseconds):
    minutes = milliseconds // 60000
    seconds = (milliseconds % 60000) // 1000
    return minutes, seconds

def calculate_additional_statistics(features_df):
    #normalize the features excluding release_date, tempo and popularity
    features_to_normalize = features_df.columns.difference(['release_date', 'popularity', 'tempo'])
    normalized_features_df = normalize_features(features_df.copy(), features_to_normalize)

    #calculate the mean and standard deviation of the normalized features
    normalized_feature_means, normalized_feature_stds = calculate_statistics(normalized_features_df)

    #calculate the average, highest, and lowest tempo
    average_tempo = features_df['tempo'].mean()
    max_tempo = features_df['tempo'].max()
    min_tempo = features_df['tempo'].min()

    #calculate the average release year, lowest, highest and how many decades they span
    average_release_year = features_df['release_date'].mean()
    min_release_year = features_df['release_date'].min()
    max_release_year = features_df['release_date'].max()
    span_decades = (max_release_year - min_release_year) // 10 + 1

    #calculate the most common decades
    features_df['decade'] = (features_df['release_date'] // 10) * 10
    most_common_decades = features_df['decade'].value_counts()
    max_count = most_common_decades.max()
    most_common_decades = most_common_decades[most_common_decades == max_count].index.tolist()

    #calculate the average popularity and its standard deviation
    average_popularity = features_df['popularity'].mean()
    std_popularity = features_df['popularity'].std()
    max_popularity = features_df['popularity'].max()
    min_popularity = features_df['popularity'].min()
    #checks std to see the range of popularity
    popularity_comment = "The songs have a narrow range of popularity." if std_popularity < 10 else "The songs have a wide range of popularity."

    #check for weak correlations and iff so adds to list of weak correlations
    weak_correlation_messages = []
    features_to_check = ['danceability', 'loudness', 'energy', 'valence']
    for feature in features_to_check:
        if normalized_feature_stds[feature] > 0.2:
            weak_correlation_messages.append(f"{feature.capitalize()} has a weak correlation within the input songs.")

    #determine if there are instrumental songs
    average_instrumentalness = features_df['instrumentalness'].mean()
    std_instrumentalness = features_df['instrumentalness'].std()
    instrumental_message = ""
    if average_instrumentalness > 0.5:
        instrumental_message = "There are mostly instrumental songs."
    elif average_instrumentalness > 0 and std_instrumentalness > 0.1:
        instrumental_message = "There are some instrumental songs."
    else:
        instrumental_message = "There are no instrumental songs."

    #analyze mode distribution
    mode_counts = features_df['mode'].value_counts(normalize=True) * 100
    mode_message = ""
    if mode_counts.get(1, 0) > 50:
        mode_message = "There is a majority of songs in the major scale, which generally means the songs are brighter and happier."
    elif mode_counts.get(0, 0) > 50:
        mode_message = "There is a majority of songs in the minor scale, which generally means the songs are darker and more melancholic."
    if 30 <= mode_counts.get(0, 0) <= 70 and 30 <= mode_counts.get(1, 0) <= 70:
        mode_message += " However, there is a good mixture of both major and minor scales in the songs, offering a balanced variety of moods."

    #analyze key distribution
    key_counts = features_df['key'].value_counts()
    total_songs = len(features_df)
    most_common_key = key_counts.idxmax()
    most_common_key_percentage = (key_counts.max() / total_songs) * 100

    if most_common_key_percentage > 50:
        key_message = f"The most common key is {KEY_NAMES[most_common_key]}, with a strong majority of {most_common_key_percentage:.2f}% of the songs."
    elif most_common_key_percentage < 50:
        key_message = f"The most common key is {KEY_NAMES[most_common_key]}, but there is a wide variety of keys among the songs."

    # calculate average, shortest, and longest duration
    average_duration_ms = features_df['duration_ms'].mean()
    shortest_duration_ms = features_df['duration_ms'].min()
    longest_duration_ms = features_df['duration_ms'].max()
    average_duration = ms_to_min_sec(average_duration_ms)
    shortest_duration = ms_to_min_sec(shortest_duration_ms)
    longest_duration = ms_to_min_sec(longest_duration_ms)

    #dictionary with all additional statisticsS
    additional_statistics = {
        "average_tempo": average_tempo,
        "max_tempo": max_tempo,
        "min_tempo": min_tempo,
        "average_release_year": average_release_year,
        "min_release_year": min_release_year,
        "max_release_year": max_release_year,
        "span_decades": span_decades,
        "most_common_decades": most_common_decades,
        "average_popularity": average_popularity,
        "std_popularity": std_popularity,
        "max_popularity": max_popularity,
        "min_popularity": min_popularity,
        "popularity_comment": popularity_comment,
        "weak_correlation_messages": weak_correlation_messages,
        "instrumental_message": instrumental_message,
        "mode_message": mode_message,
        "key_message": key_message,
        "average_duration": average_duration,
        "shortest_duration": shortest_duration,
        "longest_duration": longest_duration
    }

    return normalized_features_df, normalized_feature_means, normalized_feature_stds, additional_statistics
 # type: ignore