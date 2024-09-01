# YouTube Playlist Manager

This is a simple command-line application that demonstrates how to use the YouTube Data API v3 to perform various operations such as searching for videos, retrieving video statistics, creating playlists, and adding videos to playlists.

## Prerequisites

- Python 3.6 or higher
- A Google account
- A Google Cloud project with the YouTube Data API v3 enabled
- OAuth 2.0 Client ID credentials

## Setup
1. Create a Google Cloud Project and Enable the YouTube Data API

- Go to the Google Cloud Console.
- Click on the project drop-down and select "New Project".
- Give your project a name and click "Create".
- Select your new project from the project drop-down.
- In the left sidebar, click on "APIs & Services" > "Library".
- Search for "YouTube Data API v3" and click on it.
- Click "Enable" to enable the API for your project.

2. Create OAuth 2.0 Client ID

- In the Google Cloud Console, go to "APIs & Services" > "Credentials".
- Click "Create Credentials" and select "OAuth client ID".
- Select "Desktop app" as the application type.
- Give your OAuth 2.0 client a name and click "Create".
- Download the client configuration file and save it as client_secret.json in your project directory.

3. Clone the Repository and Install Dependencies

- Clone this repository:

    ```bash
    git clone https://github.com/yourusername/youtube-playlist-manager.git
    cd youtube-playlist-manager
    ```

- Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

- Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

- Run the application:

    ```bash
    python youtube_playlist_manager.py
    ```