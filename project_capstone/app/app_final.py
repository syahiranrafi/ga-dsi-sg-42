#######################################################
#######################################################

# Import libraries
import streamlit as st
from streamlit.components.v1 import html
import hashlib
from PIL import Image

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from http.server import HTTPServer, BaseHTTPRequestHandler
import re

import pandas as pd
import random

from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

#######################################################
#######################################################

# Load your data
tracks_10k_df = pd.read_csv('tracks-10k-processed.csv')

# 2k sample
tracks_2k_df = tracks_10k_df.sample(n=2000, random_state=42)

#######################################################
#######################################################

### Prepare track_similarity matrix

# Drop irrelevant columns
music_data = tracks_2k_df.drop(['track_uri', 'artist_uri', 'album_uri',
       'album_name', 'album_artist_uri', 'album_artist_name',
       'album_release_date', 'album_image_url', 'disc_number', 'track_number',
       'track_duration_(ms)', 'track_preview_url', 'isrc', 'added_by', 'added_at', 'artist_genres', 'album_genres', 'label', 'copyrights'], axis=1)

# Set track_name and artist_name as index
music_data.set_index(['track_name', 'artist_name'], inplace=True)

# Create a StandardScaler object
scaler = StandardScaler()

# Define the numerical columns to scale
numerical_columns = ['explicit', 'popularity', 'danceability',
       'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
       'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature']

# Apply standardization to the numerical columns
music_data[numerical_columns] = scaler.fit_transform(music_data[numerical_columns])

# Drop null rows
music_data = music_data.dropna()

# Create track_sim
track_sim = pd.DataFrame(cosine_similarity(music_data), columns=music_data.index, index=music_data.index)

#######################################################
#######################################################

# Function for generating random tracks based on genres
def generate_random_tracks_balanced(genres):
    # Load data from 'tracks_2k_df'
    track_data = tracks_2k_df
    
    # Ensure genres is a list by splitting the input string at commas
    genres_list = [genre.strip() for genre in genres.split(",")]
    
    # Initialise empty data frame to store results
    songs = pd.DataFrame()
    
    # If 1 genre is chosen, 10 random songs are shown
    if len(genres_list) == 1:
        for g in genres_list:
            # Append to 'songs' df using pd.concat()
            songs_by_genre = track_data[track_data['artist_genres'].apply(lambda x: g in x)].sample(10)
            songs = pd.concat([songs, songs_by_genre])
    # If 2 genres are chosen, 5 random songs of each genre are selected and shown
    elif len(genres_list) == 2:
        for g in genres_list:
            # Append to 'songs' df using pd.concat()
            songs_by_genre = track_data[track_data['artist_genres'].apply(lambda x: g in x)].sample(5)
            songs = pd.concat([songs, songs_by_genre])
    # If 3 or more genres are chosen, 4 random songs of each genre are selected,
    # but random sample of 10 songs are shown in the end
    else:
        for g in genres_list:
            # Append to 'songs' df using pd.concat()
            songs_by_genre = track_data[track_data['artist_genres'].apply(lambda x: g in x)].sample(4)
            songs = pd.concat([songs, songs_by_genre])
        songs = songs.sample(n=10, random_state=42)
 
    # Extract track_name, artist_name and artist_genres
    track_artist_genres = list(zip(songs['track_name'], songs['artist_name'], songs['artist_genres']))
    random.shuffle(track_artist_genres)
    result = {i + 1: tpl for i, tpl in enumerate(track_artist_genres)}
    
    # Format the dictionary into the desired output
    output = []
    
    for track_number, (track_name, artist_name, genres) in result.items():
        output.append(f"track {track_number}: {track_name} | ")
        output.append(f"artist(s): {artist_name}")
        if track_number != len(result):
            output.append("")  # Add a blank line for readability between tracks
    
    # Join the output list into a single formatted string
    formatted_output = "\n".join(output)
    
    return formatted_output

#######################################################
#######################################################

def recommend_songs(track_name, artist_name, n):
    sim_df = track_sim

    try:
        # Use loc to retrieve data based on MultiIndex values
        result = sim_df.loc[(track_name, artist_name)]

        # Sort the MultiIndex levels lexically
        result_sorted = result.sort_index()

        # Drop the specified track_name from the MultiIndex DataFrame
        result_dropped = result_sorted.drop(track_name, level="track_name")

        # Sort the resulting DataFrame (if needed) and retrieve top values
        top_values = result_dropped.sort_values(ascending=False).head(n)

        # Convert to a list of tuples
        top5list = list(top_values.index)

        return top5list

    except KeyError:
        print(f"No recommendations found for '{track_name}' by '{artist_name}'")
        return pd.Series([])  # Return an empty Series if no recommendation is found

#######################################################
#######################################################

# Function to generate personalized playlist
def generate_personalised_playlist(input_tracks):
    playlist = []
    
    # Iterate through the list of input tracks
    for input_track in input_tracks:
        # Extract track name and artist name from input
        track_info = input_track.split(" || ")
        track_name = track_info[0].replace("track: ", "")
        artist_name = track_info[1].replace("artist(s): ", "")
        
        # Recommend 5 songs based on track and artist
        top5songs = recommend_songs(track_name, artist_name, 5)
        playlist += top5songs
    
    # Select a subset of 15 songs randomly
    if len(playlist) < 15:
        return "Choose at least 3 songs!"
    else:
        playlist_subset = random.sample(playlist,15)
        
        # Format the playlist into the desired output
        output = []

        for i in range(len(playlist_subset)):
            track_number = i+1
            track_name = playlist_subset[i][0]
            artist_name = playlist_subset[i][1]
            output.append(f"track {track_number}: {track_name} || ")
            output.append(f"artist(s): {artist_name}")
            if track_number != len(playlist_subset):
                output.append("")  # Add a blank line for readability between tracks

        # Join the output list into a single formatted string
        formatted_output = "\n".join(output)
    
        return formatted_output

#######################################################
#######################################################

# Create a temporary HTTP server to get the assigned port
temp_server = HTTPServer(('localhost', 0), BaseHTTPRequestHandler)
port = temp_server.server_address[1]
temp_server.server_close()

# Replace these with your own Spotify credentials
CLIENT_ID = '8fb08fbbc06c428e8aacfed09b3c26df'
CLIENT_SECRET = '40f537d0cf2140d79d7a29a9dff2c92f'

# Update the REDIRECT_URI with the assigned port
REDIRECT_URI = f'http://example.com/callback'

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope="playlist-modify-public"))

#######################################################
#######################################################

def tracklist_to_tuples(tracklist):
    tuples = []
    for track in tracklist:
        track_info = re.sub(r'^track \d+: ', '', track)
        parts = track_info.split(" || ")
        track_info = parts[0].strip()
        artists = ", ".join([artist.strip() for artist in parts[1].split("artist(s):")[1].split(",")])
        tuples.append((track_info, artists))
    return tuples

#######################################################
#######################################################

def generate_spotify_playlist(tracklist, creator):
    # Example list of (track_name, artist_name) tuples
    track_artist_tuples = tracklist_to_tuples(tracklist)

    # Create lists to store the track names and artist names
    track_names = []
    artist_names = []

    # Iterate over the tuples and append the track names and artist names to the respective lists
    for track_name, artist_name in track_artist_tuples:
        track_names.append(track_name)
        artist_names.append(artist_name)

    # Create a DataFrame to store the track and artist information
    tracks_40k_df = pd.DataFrame({'track_name': track_names, 'artist_name': artist_names})

    # Create an empty list to store the track URIs
    track_uris = []

    # Search for each track and add its URI to the list
    for index, row in tracks_40k_df.iterrows():
        track_name = row['track_name']
        artist_name = row['artist_name']
        query = f'track:{track_name} artist:{artist_name}'
        results = sp.search(q=query, type='track', limit=1)

        if results['tracks']['items']:
            track_uri = results['tracks']['items'][0]['uri']
            track_uris.append(track_uri)
        else:
            print(f"No track found for '{track_name}' by '{artist_name}'")

    # Create a new playlist
    user_id = sp.current_user()['id']
    playlist_name = f"{creator}'s Playlist"
    playlist_description = f"A custom playlist for {creator}"
    playlist = sp.user_playlist_create(user=user_id,
                                    name=playlist_name,
                                    public=True,
                                    description=playlist_description)

    # Add the tracks to the new playlist
    sp.playlist_add_items(playlist_id=playlist['id'], items=track_uris)
    print(f"{creator}'s Playlist created successfully with {len(track_uris)} tracks.")

#######################################################
#######################################################

# Initialize session state for storing selected tracks
if 'selected_tracks' not in st.session_state:
    st.session_state.selected_tracks = {}

# Streamlit app
def main():
    # Set page configuration with a wider layout
    st.set_page_config(page_title="Personalised Playlist Generator", page_icon=":musical_note:")

    # Load and display the banner image
    banner_image = Image.open("banner.png")  # Replace "banner.jpg" with your image file name
    st.image(banner_image, use_column_width=True)

    # Create tabs
    tabs = st.tabs(["Choose your favourite genres", "Generate your personalised playlist", "Listen on Spotify"])

    def render_tracks(tracks):
        for track in tracks:
                col1, col2 = st.columns([5, 1])
                track_name = track.split(" | ")[0].split(": ")[1]
                artist_name = track.split(" | ")[1].split(": ")[1]
                with col1:
                    track_info = f"track: {track_name} || artist(s): {artist_name}"
                    st.write(track_info)
                with col2:
                    # Generate a unique key for the button
                    unique_key = hashlib.md5(f"{track_name}_{artist_name}".encode()).hexdigest()
                    if st.button("Add", key=unique_key, on_click=add_track, args=(track_name, artist_name)):
                        pass

    def add_track(track_name, artist_name):
        track_info = f"track: {track_name} || artist(s): {artist_name}"
        st.session_state.selected_tracks[track_info] = {
            "track_name": track_name,
            "artist_name": artist_name
        }
        # st.experimental_rerun()

    # Random Track Generator tab
    with tabs[0]:

        # Sidebar to display generated tracks
        # st.sidebar.title("Selected tracks")
        # selected_tracks = st.sidebar.empty()

        # Random Track Generator tab
        st.title("Random track generator 🎸")
        genres = st.text_input("What are your favourite genres?", "pop, rock, hip hop")

        if "tracks" not in st.session_state:
            st.session_state.tracks = []

        if st.button("GENERATE TRACKS"):
            result = generate_random_tracks_balanced(genres)
            tracks = result.split("\n\n")
            st.session_state.tracks = tracks
            # render_tracks(tracks)

            # Expand the sidebar and display the selected tracks
            # with st.expander("Selected tracks"):
                # for key, track_data in st.session_state.selected_tracks.items():
                    # st.write(key)
            
        render_tracks(st.session_state.tracks)

    # Personalised Playlist Generator tab
    with tabs[1]:

        st.title("Personalised playlist generator 🎵")

        # Input fields for track information
        # st.subheader("Choose your top song from each randomly generated list")

        if "final_tracks" not in st.session_state:
            st.session_state.final_tracks = []

        # Generate playlist button
        if st.button("GENERATE PLAYLIST", key="generate_playlist_button"):
            # Use selected tracks if available, otherwise use the optional input tracks
            if st.session_state.selected_tracks:
                if len(st.session_state.selected_tracks) < 3:
                    input_tracks = list(st.session_state.selected_tracks.keys())
                    playlist = generate_personalised_playlist(input_tracks)
                    st.write(playlist)
                else:
                    input_tracks = list(st.session_state.selected_tracks.keys())
                    playlist = generate_personalised_playlist(input_tracks)
                    final_tracks = playlist.split("\n\n")
                    st.session_state.final_tracks = final_tracks
                    
                    st.subheader("Here is your personalised playlist!")
                    st.write(playlist)
            else:
                st.write("Choose at least 3 songs from the first tab!")
                return
            
    # Actual Playlist Generator tab
    with tabs[2]:

        st.title("Create your personalised playlist on Spotify 🎧")

        name = st.text_input("What is your name?", "")

        # Listen on Spotify button
        if st.button("LISTEN ON SPOTIFY"):
            # Use selected tracks if available, otherwise use the optional input tracks
            if st.session_state.final_tracks:
                input_tracks = list(st.session_state.final_tracks)
                generate_spotify_playlist(input_tracks, name)
                st.subheader("Open Spotify to access your playlist! Happy listening 🎶")

    # Display selected tracks in the sidebar
    # st.sidebar.write("Selected tracks:")
    for key, track_data in st.session_state.selected_tracks.items():
        st.sidebar.write(key)
            
if __name__ == "__main__":
    main()

#######################################################
#######################################################