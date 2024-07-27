import pandas as pd
from sklearn.preprocessing import MinMaxScaler

#manually defined ranges for each numerical feature
feature_ranges = {
    'danceability': (0, 1),
    'energy': (0, 1),
    'valence': (0, 1),
    'loudness': (-60, 0),
    'tempo': (0, 250),
    'instrumentalness': (0, 1),
    'key': (0, 11),
    'duration_ms': (0, 600000),  # 10 minutes
    'liveness': (0, 1),
    'mode': (0, 1),
    'release_date': (1950, 2023),  # Assuming songs are from 1950 to 2023
    'popularity': (0, 100)
}

    #normalises each feature with the above ranges, makes all values range from 0 - 1
def normalize_features(df, features):
    for feature in features:
        min_val, max_val = feature_ranges.get(feature, (0, 1))
        df[feature] = (df[feature] - min_val) / (max_val - min_val)
    return df

    #calculates the standard deviation and mean for all normalised audio features
def calculate_statistics(df):
    feature_means = df.mean()
    feature_stds = df.std()
    return feature_means, feature_stds
