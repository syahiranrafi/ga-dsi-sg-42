<img src="http://imgur.com/1ZcRyrc.png" style="float: left; margin: 20px; height: 55px">

# DSI-SG-42
## Capstone Project: Building a Personalised Playlist Generator for Spotify
> Author: Syahiran Rafi

## Contents
- [Executive Summary](#executive-summary)
- [Problem Statement](#problem-statement)
- [Data Collection](#data-collection)
- [Data Dictionary](#data-dictionary)
- [Exploratory Data Analysis](#exploratory-data-analysis)
- [Building the Recommender](#building-the-recommender)
- [User Studies and Summary of Results](#user-studies-and-summary-of-results)
- [Evaluation](#Evaluation)
- [Recommendations](#recommendations)

## Executive Summary
Streaming services such as Spotify, Apple Music and Netflix often face the "cold start" problem where new users who sign up for the free trial often struggle to find content that match their preferences, leading to a high churn rate and low conversion to premium (or paid) subscriptions.

The goal of my project is to develop a data-driven solution that generates personalised playlists — right off the bat — for new Spotify users based on their listening preferences. By minimising the cold start problem, the likelihood of converting free trial users to premium subscribers increases.

## Problem Statement
How might we create a song recommendation system — based on a user's favourite genres — to help Spotify minimise the "cold start" problem for free trial users, thereby converting as many of them as possible to premium users?

## Data Collection
To build the song recommender, I used the following two source data sets:
1.  <b>spotify-top-10k.csv</b><br>
    Description: The best and biggest songs from ARIA (Australian) & Billboard (US) charts spanning 7 decades.<br>
    No. of songs: 10,000<br>
    Source: https://www.kaggle.com/datasets/joebeachcapital/top-10000-spotify-songs-1960-now/data

2.  <b>spotify-34k.csv</b><br>
    Description: Predominantly English songs of various genres with varying degrees of mainstream appeal.<br>
    No. of songs: 34,248<br>
    Source: https://github.com/enjuichang/PracticalDataScience-ENCA/blob/main/data/allsong_data.csv

## Data Dictionary
The following data dictionary is representative of the `spotify-40k-processed.csv` data set, which is obtained from the two source data sets after cleaning, pre-processing and merging.

This 'processed' data set — with approximately 40k tracks (or rows) — is the one that is used to generate the cosine similarity matrix for the song recommender.

| Feature | Type | Description |
|----------|------|--------------|
| `track_name` | str | The name of the track. |
| `artist_name` | str | The name of the artist(s) who performed the track. |
| `artist_genres` | str | The genres associated with the artist. |
| `danceability` | float | Describes how suitable a track is for dancing based on a combination of musical elements. |
| `energy` | float | Represents a perceptual measure of intensity and activity in a track. |
| `key` | int | The estimated key of the track, ranging from 0 (C) to 11 (B). |
| `loudness` | float | The overall loudness of a track in decibels (dB). |
| `mode` | int | Indicates the modality (major or minor) of a track, with 0 representing minor and 1 representing major. |
| `speechiness` | float | Detects the presence of spoken words in a track. |
| `acousticness` | float | A measure of whether a track is acoustic or not. |
| `instrumentalness` | float | Predicts whether a track contains no vocals. |
| `liveness` | float | Detects the presence of an audience in the recording. |
| `valence` | float | Describes the musical positiveness conveyed by a track. |
| `tempo` | float | The overall estimated tempo of a track in beats per minute (BPM). |

## Exploratory Data Analysis
#### User Journey
The intended user journey involves two main stages:
1. Select your favourite genre(s) to generate a list of random tracks
2. Select at least 3 songs from the randomly generated list to create your own personalist playlist of 15 songs

#### Goal of EDA
For this project, specifically, I want to determine the popularity of certain genres, and the different sub-genres available for the common genres (e.g., pop, rock, r&b).

With a better understanding of which genres are more popular amongst listeners, first-time users may then be suggested more common genres in the first "random track generator" stage.

## Building the Recommender
The following functions were created to support the above user journey:
| Function                      | Description |
|-------------------------------|-------------|
| `top_subgenres`               |Generates a list of top sub-genres for a list of genres|
| `generate_random_tracks`      |Generates a list of `n` random songs based on genre(s)|
| `generate_random_tracks_balanced` |Generates a list of `n` random songs based on genre(s), with a balanced sample of genres if more than one genre is input|
| `track_viewer`                |Formats the random list of songs into a more readable format for user studies|
| `extract_genres`              |Reformats the genre strings `'pop,rock,dance'` into a list of genres `['pop', 'rock', 'dance']`|
| `one_hot_encode_genres`       |Performs one hot encoding on `artist_genres` before building the `cosine_similarity` matrix|
| `recommend_songs`             |Recommends top `n` songs for a single `track_name` and `artist_name` pair|
| `generate_personalised_playlist` |Generates a personalised playlist of 15 songs, using the tracks selected from the randomly generated list|
| `df_to_tuples`                |Reformats the result from `generate_personalised_playlist` into a list of `('track_name','artist_name')` tuples to input in the `generate_spotify_playlist` function|
| `generate_spotify_playlist`   |Creates an actual Spotify playlist using Spotify API|

## User Studies and Summary of Results

#### Conduct of User Studies
To evaluate how well the recommender system works, I conducted user studies on 30 participants.

Each study lasts around 10 to 15 minutes. The following three steps are performed for each user:
1. Choose at least 3 genres to generate a random list of 15 tracks
2. Choose at least 3 songs to generate your own personalised playlist
3. Generate the playlist on Spotify

By the end of the study, the user will receive a link to their personalised playlist on Spotify. The user is then requested to listen to the playlist and rate each song on a scale of 0 (I do not like the song) to 10 (I like the song a lot).

As I interviewed more users, I made incremental changes to the recommender system in a bid to improve the overall enjoyability score (calculated as the average percentage score of the user's song ratings). 

Altogether, there were 5 different versions and each version was tested on a different group of users. The following table describes the base model (V1) and the incremental changes that were made for subsequent versions.

| Version | Description |
|-------------------------------|-------------|
| V1 (base) | 1. User selects at least 3 preferred songs from the random list <br> 2. The recommender gives the top 10 similar songs for each song <br> 3. 15 songs are sampled to form the playlist |
| V2 | The recommender now gives the top 5 similar songs for each song, instead of 10 |
| V3 | The random song generator and song recommender now pull from the 40k songs data set, instead of the 10k songs data set |
| V4 | The random song generator now pulls from the 10k songs data set (as in V1 and V2), while the song recommender pulls from the 40k songs data set (as in V3) |
| V5 | The random song generator shows a balanced sample of songs for each genre that the user selects |

#### Summary of Results
The following table displays the summary of results from the user studies. The percentage scores shown represent the average user ratings for each version of the recommender.

| Version | No. of Participants | Average Score |
|-------------|-------------|-------------|
| V1 (base) | 7 | 62.0% |
| V2 | 7 |61.9% |
| V3 | 2 |72.0% |
| V4 | 6 |68.9% |
| V5 | 8 |66.0% |

## Recommendations
For further development of this recommender system, I suggest exploring the following two approaches:

1. **A hybrid approach consisting of collaborative filtering and content-based filtering techniques** <br>
- Content-based filtering (current approach)
    - Currently, the song recommender employs the content-based collaborative filtering technique using cosine similarity.
    - Does not consider preferences or behavior of other users; recommendations are based solely on the user's own preferences and the item's content.
- Collaborative filtering (supplementary approach)
    - Since each user was asked to rate each song on their personalised playlist from 0 to 10 as part of the user studies, we may have sufficient preference data to start implementing collaborative filtering techniques.
        1. Item-based collaborative filtering:
            - Measures similarity between items based on the preferences and behavior of other users, rather than the content or attributes of the items themselves.
        2. User-based collaborative filtering:
            - Does not consider the content or attributes of the items themselves; recommendations are based solely on the preferences of similar users.

- In practice, hybrid approaches that combine user-based collaborative filtering, item-based filtering, and content-based filtering are often used to leverage the strengths of each technique and mitigate their weaknesses.

2. **Deep learning or matrix factorisation to determine track genres** <br>
- One major drawback in the Spotify API is that we are unable to extract the track genres, only the artist genres and album artist album genres.
- Upon further reading online, it seems like many tracks on Spotify don't even have genres assigned to them, unlike on Apple Music.
- There is an edge case which the current recommender system does not prevent: If artists X and Y were to collaborate on the same track, a user may like a song because of artist X and not necessarily artist Y. However, the current recommender would still be able to recommend songs similar to artist Y.
- A possible workaround is to experiment with deep learning and/or matrix factorisation.
    - Deep learning:
        - Neural networks and deep learning techniques, such as autoencoders, recurrent neural networks (RNNs), and convolutional neural networks (CNNs), can be used to learn complex patterns and representations from user data and song features to determine the genre(s) of each song and generate accurate, personalised recommendations.
    - Matrix factorisation:
        - This technique is often used in collaborative filtering systems. It decomposes the user-item rating matrix into lower-dimensional matrices, capturing latent factors that represent user preferences and item characteristics. These latent factors can be used to predict missing ratings (in this case, track genres) and generate recommendations.

## Files
**Code**
- 01_Data_Collection.ipynb   
- 02_EDA.ipynb
- 03_Recommender.ipynb

**Data**
- genres-10k.csv
- spotify-34k.csv
- spotify-40k-processed.csv
- spotify-top-10k-processed.csv
- spotify-top-10k.csv

**Slides**
- SG-DSI-42_CAPSTONE_PROJECT_05.pdf

**README**
- README.md

**App**
- tracks-10k-processed.csv
- banner.png
- app.py

---