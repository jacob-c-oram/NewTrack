from src.red_black_tree import RedBlackTree
from src.b_tree import BTree
from src.dataset_utils import load_song_dataset
import time
import random

# recommend a list of songs based on the answers user enters
def recommend_songs(tree, filters, structure_name):
    print(f"\nFinding songs using {structure_name}...")

    matching_songs = [] # for keeping track songs based on the filters
    seen_songs = set() # keep track of songs to prevent duplicating them in the playlist
    start_time = time.time()

    # getting the filters to use for the songs
    for song in tree:
        if filters.get("genres"):
            song_genre = song.get("track_genre", "").lower()
            if song_genre not in filters["genres"]:
                continue

        if filters.get("explicit") is not None and song.get("explicit", False) != filters["explicit"]:
            continue

        if filters.get("danceability") and not filters["danceability"][0] <= song.get("danceability", 0) <= filters["danceability"][1]:
            continue
        if filters.get("valence") and not filters["valence"][0] <= song.get("valence", 0) <= filters["valence"][1]:
            continue
        if filters.get("popularity") and not filters["popularity"][0] <= song.get("popularity", 0) <= filters["popularity"][1]:
            continue

        # for keeping track of song name and artist together
        song_id = (song.get("track_name", ""), song.get("artists", ""))  # Unique identifier
        if song_id not in seen_songs:
            matching_songs.append(song)
            seen_songs.add(song_id)

    elapsed_time = time.time() - start_time

    if matching_songs:
        # max number of songs for the playlist
        max_songs = filters.get("max_songs")
        if max_songs and len(matching_songs) > max_songs:
            matching_songs = random.sample(matching_songs, max_songs)

        print(f"Found {len(matching_songs)} matching songs:")
        for song in matching_songs:
            print(
                f"  Title: {song.get('track_name', 'Unknown')} by {song.get('artists', 'Unknown')}, "
                f"Genre: {song.get('track_genre', 'Unknown')}, Danceability: {song.get('danceability', 0):.2f}"
            )
    else:
        print("No matching songs found.")

    print(f"Query Time: {elapsed_time:.6f} seconds")
    return matching_songs, elapsed_time


def ask_user_questions(unique_genres, ask_max_songs=True):
    # questions for the recommendations
    filters = {}

    # ask for max songs in playlist
    if ask_max_songs:
        print("\nWhat's the maximum number of songs you want in your playlist? (Enter a number or press Enter for no limit)")
        max_songs_input = input("Enter the maximum number of songs: ").strip()
        try:
            filters["max_songs"] = int(max_songs_input) if max_songs_input else None
        except ValueError:
            print("Invalid input. No limit will be applied.")
            filters["max_songs"] = None
    else:
        filters["max_songs"] = None

    # explicitness question
    print("\nDo you want to include songs with explicit content?")
    print("1. Yes (Include both explicit and non-explicit songs)")
    print("Enter anything else if No (Only non-explicit songs)")
    explicit_choice = input("Enter your choice: ")
    filters["explicit"] = None if explicit_choice == "1" else False

    # danceability question
    print("\nHow danceable should the songs be?")
    print("1. Very danceable")
    print("2. Somewhat danceable")
    print("3. Not very danceable")
    print("Enter anything else if you have no preference.")
    danceability_choice = input("Enter your choice: ")
    filters["danceability"] = {
        "1": (0.7, 1.0),  # very danceable
        "2": (0.4, 0.6),  # somewhat danceable
        "3": (0, 0.4),    # not very danceable
        "4": None,        # no preference
    }.get(danceability_choice)

    # valence question
    print("\nWhat emotional tone do you prefer?")
    print("1. Positive and upbeat")
    print("2. Calm and neutral")
    print("3. Melancholic and slow")
    print("Enter anything else if you have no preference.")
    valence_choice = input("Enter your choice: ")
    filters["valence"] = {
        "1": (0.5, 1.0),  # positive and upbeat
        "2": (0.3, 0.5),  # calm and neutral
        "3": (0, 0.3),    # melancholic and slow
        "4": None,        # no preference
    }.get(valence_choice)

    # popular or not question
    print("\nHow popular should the songs be?")
    print("1. Very popular")
    print("2. Not as well known")
    print("Enter anything else if you have no preference.")
    popularity_choice = input("Enter your choice: ")
    filters["popularity"] = {
        "1": (50, 100),  # very popular
        "2": (0, 50),    # not as well known
        "3": None,       # no preference
    }.get(popularity_choice)

    # grouped similar genres together so there weren't so many choices for user
    genre_groups = {
        "1": [
            "pop", "alt-rock", "alternative", "indie", "indie-pop", "power-pop", "psych-rock", "punk", "punk-rock", "rock",
            "rock-n-roll", "rockabilly", "grunge", "guitar", "acoustic", "romance", "emo", "garage", "ska", "disco"
        ],
        "2": [
            "edm", "electro", "electronic", "house", "deep-house", "progressive-house", "techno", "trance", "dubstep",
            "dance", "club", "chill", "breakbeat", "chicago-house", "detroit-techno", "drum-and-bass", "dub", "idm", "industrial", "synth-pop", "trip-hop", "groove", "happy"
        ],
        "3": ["hip-hop", "r-n-b", "rap", "trap", "dancehall"],
        "4": ["jazz", "blues", "bluegrass", "soul", "funk", "gospel"],
        "5": ["classical", "opera", "piano", "instrumental", "study", "minimal-techno"],
        "6": [
            "afrobeat", "reggae", "latin", "reggaeton", "salsa", "samba", "tango", "forro", "mpb", "pagode", "sertanejo",
            "world-music", "turkish", "iranian", "spanish", "swedish", "british", "brazil", "latino", "malay", "party", "german", "indian", "french", "pop-film"
        ],
        "7": ["heavy-metal", "death-metal", "black-metal", "grindcore", "hard-rock", "metal", "metalcore", "hardcore", "hardstyle", "goth"],
        "8": ["country", "honky-tonk", "folk", "singer-songwriter", "songwriter"],
        "9": ["ambient", "chill", "sleep", "new-age", "sad"],
        "10": ["k-pop", "j-pop", "j-rock", "cantopop", "mandopop", "j-dance", "j-idol", "anime"],
        "11": ["children", "disney","show-tunes", "comedy", "kids"]
    }

    print("\nSelect genres:")
    print("1. Pop and Rock")
    print("2. Electronic and Dance")
    print("3. Hip-Hop and R&B")
    print("4. Jazz, Blues, and Soul")
    print("5. Classical and Instrumental")
    print("6. World Music")
    print("7. Metal and Hard Rock")
    print("8. Country and Folk")
    print("9. Chill and Ambient")
    print("10. Asian Pop and Rock")
    print("11. Miscellaneous")
    print("12. Search for a genre")
    print("13. View every individual genres")
    print("Enter anything else if you have no preference.")

    # genre question
    selected_genres = []
    genre_choice = input("Enter your choice: ").strip()

    # add options for searching and seeing all genres
    # greater than any option skip and include all genres
    if str(len(genre_groups) + 3) in genre_choice:
        filters["genres"] = None
    elif str(len(genre_groups) + 2) in genre_choice: # see all genres
        print("\nAll Available Genres:")
        for idx, genre in enumerate(unique_genres, start=1):
            print(f"{idx}. {genre}")
        print("Enter your choice:")
        genre_indices = input().strip().split(',')
        for idx in genre_indices:
            if idx.isdigit() and 1 <= int(idx) <= len(unique_genres):
                selected_genres.append(unique_genres[int(idx) - 1].lower())
    elif str(len(genre_groups) + 1) in genre_choice:  # search for the genre
        search_term = input("Enter a genre to search for: ").strip().lower()
        matching_genres = [genre for genre in unique_genres if search_term in genre.lower()]
        if matching_genres:
            print("\nMatching Genres:")
            for idx, genre in enumerate(matching_genres, start=1):
                print(f"{idx}. {genre}")
            print("Enter your choice:")
            genre_indices = input().strip().split(',')
            for idx in genre_indices:
                if idx.isdigit() and 1 <= int(idx) <= len(matching_genres):
                    selected_genres.append(matching_genres[int(idx) - 1].lower())
        else:
            print("No matching genres found. Skipping genre selection.")
    else: # choose from the groups
        group_indices = genre_choice.split(',')
        for idx in group_indices:
            if idx.isdigit() and idx in genre_groups:
                selected_genres.extend(genre_groups[idx])

    filters["genres"] = selected_genres if selected_genres else None

    return filters

def select_genres_for_search(unique_genres):
    """
    Ask the user to select genres for the search operation.
    """
    genre_groups = {
        "1": [
            "pop", "alt-rock", "alternative", "indie", "indie-pop", "power-pop", "psych-rock", "punk", "punk-rock", "rock",
            "rock-n-roll", "rockabilly", "grunge", "guitar", "acoustic", "romance", "emo", "garage", "ska", "disco"
        ],
        "2": [
            "edm", "electro", "electronic", "house", "deep-house", "progressive-house", "techno", "trance", "dubstep",
            "dance", "club", "chill", "breakbeat", "chicago-house", "detroit-techno", "drum-and-bass", "dub", "idm", "industrial", "synth-pop", "trip-hop", "groove", "happy"
        ],
        "3": ["hip-hop", "r-n-b", "rap", "trap", "dancehall"],
        "4": ["jazz", "blues", "bluegrass", "soul", "funk", "gospel"],
        "5": ["classical", "opera", "piano", "instrumental", "study", "minimal-techno"],
        "6": [
            "afrobeat", "reggae", "latin", "reggaeton", "salsa", "samba", "tango", "forro", "mpb", "pagode", "sertanejo",
            "world-music", "turkish", "iranian", "spanish", "swedish", "british", "brazil", "latino", "malay", "party", "german", "indian", "french", "pop-film"
        ],
        "7": ["heavy-metal", "death-metal", "black-metal", "grindcore", "hard-rock", "metal", "metalcore", "hardcore", "hardstyle", "goth"],
        "8": ["country", "honky-tonk", "folk", "singer-songwriter", "songwriter"],
        "9": ["ambient", "chill", "sleep", "new-age", "sad"],
        "10": ["k-pop", "j-pop", "j-rock", "cantopop", "mandopop", "j-dance", "j-idol", "anime"],
        "11": ["children", "disney","show-tunes", "comedy", "kids"]
    }

    print("\nSelect genres:")
    print("1. Pop and Rock")
    print("2. Electronic and Dance")
    print("3. Hip-Hop and R&B")
    print("4. Jazz, Blues, and Soul")
    print("5. Classical and Instrumental")
    print("6. World Music")
    print("7. Metal and Hard Rock")
    print("8. Country and Folk")
    print("9. Chill and Ambient")
    print("10. Asian Pop and Rock")
    print("11. Miscellaneous")
    print("12. Search for a genre")
    print("13. View individual genres")
    print("Enter anything else if you have no preference.")

    selected_genres = []
    genre_choice = input("Enter your choice: ").strip()

    if str(len(genre_groups) + 3) in genre_choice:
        return None
    elif str(len(genre_groups) + 2) in genre_choice:
        print("\nAll Available Genres:")
        for idx, genre in enumerate(unique_genres, start=1):
            print(f"{idx}. {genre}")
        print("Enter your choices:")
        genre_indices = input().strip().split(',')
        for idx in genre_indices:
            if idx.isdigit() and 1 <= int(idx) <= len(unique_genres):
                selected_genres.append(unique_genres[int(idx) - 1].lower())
    elif str(len(genre_groups) + 1) in genre_choice:
        search_term = input("Enter a genre to search for: ").strip().lower()
        matching_genres = [genre for genre in unique_genres if search_term in genre.lower()]
        if matching_genres:
            print("\nMatching Genres:")
            for idx, genre in enumerate(matching_genres, start=1):
                print(f"{idx}. {genre}")
            print("Enter your choice:")
            genre_indices = input().strip().split(',')
            for idx in genre_indices:
                if idx.isdigit() and 1 <= int(idx) <= len(matching_genres):
                    selected_genres.append(matching_genres[int(idx) - 1].lower())
        else:
            print("No matching genres found. Skipping genre selection.")
    else:
        group_indices = genre_choice.split(',')
        for idx in group_indices:
            if idx.isdigit() and idx in genre_groups:
                selected_genres.extend(genre_groups[idx])

    return selected_genres if selected_genres else None

def search_songs(rbt, btree, unique_genres):
    # search by title, artist, or genre
    print("\nSearch the dataset for songs by:")
    print("1. Song title")
    print("2. Artist")
    print("3. Genre")

    search_choice = input("Enter your choice: ").strip()

    if search_choice == "1":
        query = input("Enter the song title: ").strip().lower()
        filters = {"track_name": query}
    elif search_choice == "2":
        query = input("Enter the artist name: ").strip().lower()
        filters = {"artists": query}
    elif search_choice == "3":
        genres = select_genres_for_search(unique_genres)
        if genres is not None:
            filters = {"genres": genres}
        else:
            print("No genres selected. Returning to the main menu.")
            return
    else:
        print("Invalid choice. Returning to the main menu.")
        return

    # red - black tree search
    print("\nSearching using Red-Black Tree...")
    start_time = time.time()
    rbt_results = search_in_tree(rbt, filters)
    rbt_time = time.time() - start_time

    # B - tree search
    print("\nSearching using B-Tree...")
    start_time = time.time()
    btree_results = search_in_tree(btree, filters)
    btree_time = time.time() - start_time

    # results
    display_search_results(rbt_results, rbt_time, "Red-Black Tree")
    display_search_results(btree_results, btree_time, "B-Tree")



def search_in_tree(tree, filters):
    # search song
    results = []
    for song in tree:
        track_name = song.get("track_name", "")
        artists = song.get("artists", "")
        track_genre = song.get("track_genre", "")

        # make strings, all lowercase, and compare them
        track_name = str(track_name).lower() if isinstance(track_name, (str, float, int)) else ""
        artists = str(artists).lower() if isinstance(artists, (str, float, int)) else ""
        track_genre = str(track_genre).lower() if isinstance(track_genre, (str, float, int)) else ""


        if "track_name" in filters and filters["track_name"] not in track_name:
            continue
        if "artists" in filters and filters["artists"] not in artists:
            continue
        if filters.get("genres"):
            if track_genre not in filters["genres"]:
                continue

        results.append(song)

    return results


def display_search_results(results, elapsed_time, structure_name):
    print(f"\n{structure_name} Results:")
    print(f"Found {len(results)} songs in {elapsed_time:.6f} seconds.")
    if results:
        for song in results:  # show all of the results
            print(f"  Title: {song.get('track_name', 'Unknown')} by {song.get('artists', 'Unknown')}, "
                  f"Genre: {song.get('track_genre', 'Unknown')}")
    else:
        print("No matching songs found.")



def main():
    # load dataset
    print("Loading song dataset...")
    songs = load_song_dataset("dataset/songs_dataset.csv")

    unique_genres = sorted(set(song["track_genre"] for song in songs if song["track_genre"]))

    # initialize the trees
    print("Initializing data structures...")
    rbt = RedBlackTree()
    btree = BTree(order=4)

    # insert songs into trees
    print("Inserting songs into data structures...")
    for song in songs:
        rbt.insert(song["danceability"], song)
        btree.insert(song["danceability"], song)

    while True:
        print("\nMusic Recommendation System")
        print("---------------------------")
        print("1. Create a playlist")
        print("2. Find all songs that meet your criteria")
        print("3. Search the dataset")
        print("4. Exit")

        choice = input("Enter your choice: ")
        if choice == "4":
            print("Exiting the program. Goodbye!")
            break
        elif choice == "1":
            filters = ask_user_questions(unique_genres, ask_max_songs=True)
            rbt_songs, rbt_time = recommend_songs(rbt, filters, "Red-Black Tree")
            btree_songs, btree_time = recommend_songs(btree, filters, "B-Tree")

            # print a comparison between the trees
            print("\nComparison Summary:")
            print(f"Red-Black Tree: {len(rbt_songs)} songs found, Query Time: {rbt_time:.6f} seconds")
            print(f"B-Tree: {len(btree_songs)} songs found, Query Time: {btree_time:.6f} seconds")

            if not rbt_songs and not btree_songs:
                print("\nNo songs matched your filters. Try adjusting your preferences.")
        elif choice == "2":
            filters = ask_user_questions(unique_genres, ask_max_songs=False)
            rbt_songs, rbt_time = recommend_songs(rbt, filters, "Red-Black Tree")
            btree_songs, btree_time = recommend_songs(btree, filters, "B-Tree")

            print("\nComparison Summary:")
            print(f"Red-Black Tree: {len(rbt_songs)} songs found, Query Time: {rbt_time:.6f} seconds")
            print(f"B-Tree: {len(btree_songs)} songs found, Query Time: {btree_time:.6f} seconds")

            if not rbt_songs and not btree_songs:
                print("\nNo songs matched your filters. Try adjusting your preferences.")
        elif choice == "3":
            search_songs(rbt, btree, unique_genres)
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()


