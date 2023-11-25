# Import necessary libraries
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd

# Load data from CSV
df = pd.read_csv('Spotify_Youtube.csv')

# Select the top 20 artists based on stream count
top_20_artists = df.groupby('Artist')['Stream'].sum().reset_index().nlargest(20, 'Stream')

# Initialize Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    # Header section
    html.Div([
        html.H2("Interactive Artist Streams Breakdown"),
        html.P("Click on the bar chart of every artist to see the streams breakdown for every song."),
    ]),

    # Bar chart section
    dcc.Graph(
        id='bar-chart',
        figure={
            'data': [
                {'x': top_20_artists['Artist'], 'y': top_20_artists['Stream'], 'type': 'bar', 'name': 'Stream Count'}
            ],
            'layout': {
                'title': 'Top 20 Artists - Stream Count',
                'xaxis': {'title': 'Artist'},
                'yaxis': {'title': 'Stream Count'},
            }
        }
    ),

    # Details section
    html.Div(id='selected-song-details')
])

# Define callback to update details when a bar is clicked
@app.callback(
    Output('selected-song-details', 'children'),
    [Input('bar-chart', 'clickData')]
)
def display_selected_song_details(click_data):
    # Check if a bar is clicked
    if click_data is None:
        return 'Select a bar to view details'

    # Get selected artist
    selected_artist = click_data['points'][0]['x']
    
    # Get songs and stream counts for the selected artist without the index column
    selected_songs = df[df['Artist'] == selected_artist][['Track', 'Stream']].reset_index(drop=True)

    # Create details text with Markdown formatting
    details_text = f"**Selected Artist:** {selected_artist}\n\n"
    details_text += '**Selected Songs and Stream Count:**\n'

    # Add each song, stream count, and a line break for formatting
    for index, row in selected_songs.iterrows():
        details_text += f"{index + 1}. {row['Track']}: {row['Stream']}\n"

    # Use Markdown for formatting
    return html.Div([dcc.Markdown(details_text)])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
