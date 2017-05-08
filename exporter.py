import json
import os
import sys
import spotipy
import spotipy.util as util

OUTPUT = 'playlists.json'

USERNAME = '<YOUR_USERNAME_HERE>'

SPOTIPY_CLIENT_ID = '<YOUR_CLIENT_ID_HERE>'
SPOTIPY_CLIENT_SECRET = '<YOUR_CLIENT_SECRET_HERE>'

SPOTIPY_REDIRECT_URI = 'http://localhost/'

def main():
    os.environ['SPOTIPY_CLIENT_ID'] = SPOTIPY_CLIENT_ID
    os.environ['SPOTIPY_CLIENT_SECRET'] = SPOTIPY_CLIENT_SECRET
    os.environ['SPOTIPY_REDIRECT_URI'] = SPOTIPY_REDIRECT_URI

    scope = 'playlist-read-private'

    token = util.prompt_for_user_token(USERNAME, scope)

    if not token:
        print('Can\'t get token for', USERNAME)
        return

    sp = spotipy.Spotify(auth=token)
    playlists = sp.user_playlists(USERNAME)

    export_content = {'playlists': []}

    for playlist in playlists['items']:
        if playlist['owner']['id'] != USERNAME:
            continue

        to_append = {}
        to_append['name'] = playlist['name']

        print('Processing ' + playlist['name'] + '...')

        results = sp.user_playlist(USERNAME, playlist['id'], fields='tracks, next')

        count = 0

        with open('toto.json', 'w') as f:
            f.write(json.dumps(results, sort_keys=True, indent=2))

        tracks = results['tracks']

        tracks_to_append = []

        while True:
            count += len(tracks['items'])
        
            for i, item in enumerate(tracks['items']):
                track = item['track']
                tracks_to_append.append(track['name'] + " - " + track['artists'][0]['name'])
            
            if tracks['next']:
                tracks = sp.next(tracks)
            else:
                break

        to_append['count'] = count
        to_append['tracks'] = tracks_to_append
        export_content['playlists'].append(to_append)

    with open('playlists.json', 'w') as f:
        f.write(json.dumps(export_content, sort_keys=True, indent=2))

if __name__ == '__main__':
    main()
