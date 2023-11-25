import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
from scipy.stats import linregress


## figure 1 shows the top 20 artists based off of Spotify Sream numbers:
# Load data from CSV
df = pd.read_csv('Spotify_Youtube.csv')

# Group by artist and sum the number of streams
artist_streams = df.groupby('Artist')['Stream'].sum().reset_index()

# Sort the data by the total number of streams in descending order
artist_streams = artist_streams.sort_values(by='Stream', ascending=False)

# Select the top 20 artists
top_20_artists = artist_streams.head(20)

# Plotting
plt.figure(figsize=(12, 8))
bars = plt.bar(range(len(top_20_artists['Artist'])), top_20_artists['Stream'], color='skyblue')
plt.xlabel('Artist')
plt.ylabel('Total Streams (Spotify)')
plt.title('Total Spotify Streams for Each Artist (Top 20)')
plt.xticks(range(len(top_20_artists['Artist'])), top_20_artists['Artist'], rotation=45, ha='right')

# Individual bar labels
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval*1.025, f'{yval/1e6:.0f}M', ha='center',va='top', fontsize=8)

plt.tight_layout()
plt.savefig('top_20_artist_streams_plot.png')
plt.show()

## Figure 2 - Comparing Danceability and Speechiness in the top 1K songs

# Select the top 1000 tracks based on stream count
top_1K_tracks = df.nlargest(1000, 'Stream')

# Plotting attributes against stream count
plt.figure(figsize=(12, 8))

# Example attributes, replace with your actual attribute columns
# attributes = ['Danceability', 'Energy', 'Speechiness', 'Acousticness', 'Instrumentalness', 'Liveness', 'Valence']
attributes = ['Danceability','Speechiness']


for attribute in attributes:
    # Plot the data points
    plt.plot(top_1K_tracks['Stream'], top_1K_tracks[attribute],'o-', label=f'{attribute} Data')

plt.xlabel('Stream Count (1e9)')
plt.ylabel('Attribute Value')
plt.title('Comparing the Danceability and Speechiness of the Top 1000 Songs (Based on Streams)')
plt.legend()

# Set x-axis ticks to start from the minimum value of 'Stream'
min_stream = int(min(top_1K_tracks['Stream']))
max_stream = int(max(top_1K_tracks['Stream']))
subset_values = range(min_stream, max_stream, 500000000)  # Adjust the step size as needed
plt.xticks(subset_values)

plt.tight_layout()
plt.savefig('Danceability_vs_Speechiness_Top_1K_Songs.png')
plt.show()
