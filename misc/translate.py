import sys
import json

translation_table = {
    'January': 'Janvier',
    'February': 'Février',
    'March': 'Mars',
    'April': 'Avril',
    'May': 'Mai',
    'June': 'Juin',
    'July': 'Juillet',
    'August': 'Août',
    'September': 'Septembre',
    'October': 'Octobre',
    'November': 'Novembre',
    'December': 'Decembre'
}

def main():
    if len(sys.argv) > 2:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    else:
        print("Whoops, need arguments input and output!")
        print("usage: python translate.py [input] [output]")
        sys.exit()

    with open(input_file, 'r') as f:
        file_content = f.read()

    content = json.loads(file_content)

    for i in range(len(content['playlists'])):
        playlist = content['playlists'][i]
        playlist_name = playlist['name'].split()
        if playlist_name[0] in translation_table:
            tmp = playlist_name[0]
            playlist_name[0] = translation_table[tmp]
            content['playlists'][i]['name'] = ' '.join(playlist_name)
        

    with open(output_file, 'w') as f:
        f.write(json.dumps(content, sort_keys=True, indent=2))

if __name__ == '__main__':
    main()
