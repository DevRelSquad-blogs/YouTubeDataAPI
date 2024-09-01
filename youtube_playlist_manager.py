import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# function for authentication
def get_authenticated_service():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        "client_secret.json", scopes)
    flow.run_local_server(port=8080, prompt="consent", authorization_prompt_message="")
    credentials = flow.credentials
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


# function for searching videos
def search_videos(youtube, query, max_results=10):
    try:
        search_response = youtube.search().list(
            q=query,
            type="video",
            part="id,snippet",
            maxResults=max_results
        ).execute()

        videos = []
        for search_result in search_response.get("items", []):
            video = {
                "id": search_result["id"]["videoId"],
                "title": search_result["snippet"]["title"],
                "description": search_result["snippet"]["description"],
                "thumbnail": search_result["snippet"]["thumbnails"]["default"]["url"]
            }
            videos.append(video)

        return videos
    except googleapiclient.errors.HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
        return None
    
# function to get stats for a video
def get_video_stats(youtube, video_id):
    try:
        stats_response = youtube.videos().list(
            part="statistics",
            id=video_id
        ).execute()

        if "items" in stats_response:
            stats = stats_response["items"][0]["statistics"]
            return {
                "views": stats["viewCount"],
                "likes": stats["likeCount"],
                "comments": stats["commentCount"]
            }
        else:
            return None
    except googleapiclient.errors.HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
        return None
    

# function to create a new playlist
def create_playlist(youtube, title, description):
    try:
        playlist_response = youtube.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description
                },
                "status": {
                    "privacyStatus": "private"
                }
            }
        ).execute()

        return playlist_response["id"]
    except googleapiclient.errors.HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
        return None
    
# function to add a video to the playlist
def add_video_to_playlist(youtube, playlist_id, video_id):
    try:
        add_video_response = youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        ).execute()

        return add_video_response
    except googleapiclient.errors.HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
        return None
    

# main function
def main():
    youtube = get_authenticated_service()
    
    while True:
        print("\nYouTube Playlist Manager")
        print("1. Search for videos")
        print("2. Get video statistics")
        print("3. Create a playlist")
        print("4. Add video to playlist")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == "1":
            query = input("Enter search query: ")
            results = search_videos(youtube, query)
            if results:
                for video in results:
                    print(f"Title: {video['title']}")
                    print(f"Video ID: {video['id']}")
                    print(f"Description: {video['description'][:50]}...")
                    print("---")
            else:
                print("No videos found or an error occurred.")
        
        elif choice == "2":
            video_id = input("Enter video ID: ")
            stats = get_video_stats(youtube, video_id)
            if stats:
                print(f"Views: {stats['views']}")
                print(f"Likes: {stats['likes']}")
                print(f"Comments: {stats['comments']}")
            else:
                print("Video not found or stats unavailable.")
        
        elif choice == "3":
            title = input("Enter playlist title: ")
            description = input("Enter playlist description: ")
            playlist_id = create_playlist(youtube, title, description)
            if playlist_id:
                print(f"Playlist created with ID: {playlist_id}")
            else:
                print("Failed to create playlist.")
        
        elif choice == "4":
            playlist_id = input("Enter playlist ID: ")
            video_id = input("Enter video ID to add: ")
            result = add_video_to_playlist(youtube, playlist_id, video_id)
            if result:
                print("Video added to playlist successfully.")
            else:
                print("Failed to add video to playlist.")
        
        elif choice == "5":
            print("Thank you for using YouTube Playlist Manager!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()