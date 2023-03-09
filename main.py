import json
import requests
import subprocess


def get_movie_show_input():
    query = input("Enter movie/show: ")
    return query

def get_selected_media_index(title_with_id_type):
    for i, title in enumerate(title_with_id_type):
        print(f"{i+1}: {title}")
    selected_index = int(input("Please select your media: ")) - 1
    return selected_index

def get_selected_stream(data):
    for i, source in enumerate(data["sources"]):
        quality = source["quality"]
        print(f"{i+1}: {quality}")
    selected_index = int(input("Please select a stream: ")) - 1
    return selected_index

def get_selected_episode(data):
    seasons = data["episodes"]
    last_season = max(episode['season'] for episode in seasons)
    selected_season = int(input(f"Choose season 1-{last_season}: "))
    selected_episodes = [episode for episode in seasons if episode['season'] == selected_season]
    for episode in selected_episodes:
        print(episode['title'])
    selected_episode_number = int(input("Choose episode: "))
    selected_episode_id = {episode['number']: episode['id'] for episode in selected_episodes}
    for selected_episode_number in selected_episode_id:
        episode_id = selected_episode_id[selected_episode_number]
    return episode_id


url = "https://api.haikei.xyz/movies/flixhq/"
query = get_movie_show_input()
response = requests.get(url + query)
data = json.loads(response.text)

title_with_id_type = [f"{result['title']} ({result['type']})" for result in data["results"]]
selected_index = get_selected_media_index(title_with_id_type)

selected_id = data["results"][selected_index]["id"]
response = requests.get(f"{url}info?id={selected_id}")
data = response.json()

if data["type"] == "Movie":
    episode_id = data["episodes"][0]["id"]
else:
	episode_id = get_selected_episode(data)


response = requests.get(f"{url}watch?episodeId={episode_id}&mediaId={selected_id}")
data = response.json()

selected_index = get_selected_stream(data)
selected_link = data["sources"][selected_index]["url"]
referer = data["headers"]["Referer"]
subprocess.call(["mpv", selected_link, "  --http-header-fields=Referer: ", referer])
