import pandas as pd

def load_song_dataset(filepath="dataset/songs_dataset.csv"):
    # load the data set

    # try to read dataset
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        # if not found throw out a message
        print(f"Error: File not found at {filepath}")
        return []

    # columns needed
    df = df[['track_name', 'artists', 'track_genre', 'tempo', 'popularity', 'danceability', 'valence', 'explicit']]

    print(f"Loaded dataset with {len(df)} songs.")
    return df.to_dict(orient="records")

