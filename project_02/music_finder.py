from apis import spotify
from apis import sendgrid

import pandas as pd
from apis import authentication, utilities


def print_menu():
    print('''
---------------------------------------------------------------------
Settings / Browse Options
---------------------------------------------------------------------
1 - Select your favorite genres {get_genres}
2 - Select your favorite artists {get_artists}
3 - Select your favorite tracks {get_tracks}
4 - Discover new music
5 - Quit
---------------------------------------------------------------------
    '''.format(
          get_genres=display_genre,
          get_artists=artists,
          get_tracks = tracks))

display_genre = []
genres = []
artists = []
artist_dict = {}
track_dict = {}
tracks = []


def handle_genre_selection():
    temp = True
    while temp:
        temp = False
        list_of_genres = spotify.get_genres_abridged()
        i = 0
        while len(list_of_genres) > i:
            num = i+1
            if num in genres:
                print(str(num) + '. [x] ' + list_of_genres[i])
            else:
                print(str(num) + '. [ ] ' + list_of_genres[i])
            i += 1
        genre_select = input('Please select up to three genres as a comma-delimited list of numbers. Type "clear" to clear out genres.')
        if genre_select == 'clear':
            genres.clear()
            display_genre.clear()
            break
        temp_genres = []
        temp_num = ""
        for char in genre_select:
            if (char < '0' or char > '9') and char != ',':
                print("Error: Numbers and commas only")
                temp = True
                temp_genres = []
                temp_num = ""
                break
            else:
                if char == ',':
                    if(temp_num == ""):
                        print("Not a valid selection")
                        temp = True
                        temp_genres = []
                        temp_num = ""
                        break
                    num = int(temp_num)
                    if num > len(list_of_genres) or num < 1:
                        print("Not a valid selection")
                        temp = True
                        temp_genres = []
                        temp_num = ""
                        break
                    else:
                        temp_genres.append(num)
                        temp_num = ""
                else:
                    temp_num = temp_num + char
        should_append = False
        for char in temp_num:
            if (char < '0' or char > '9') and char != ',':
                print("Error: Numbers and commas only")
                temp = True
                temp_genres = []
                break
            elif int(temp_num) > len(list_of_genres) or int(temp_num) < 1:
                print("Not a valid selection")
                temp = True
                temp_genres = []
                break
            else:
                should_append = True
        if should_append:
            temp_genres.append(int(temp_num))
        if len(temp_genres) > 3:
            print("Please choose up to 3 genres")
            temp = True
            temp_genres = []
            temp_num = ""
        else:
            num_appended = 0
            for n in temp_genres:
                if n not in genres:
                    if len(genres) < 3:
                        genres.append(n)
                        num_appended += 1
                    else:
                        print("You may only have 3 selected genres")
                        if num_appended > 0:
                            print("Only", str(num_appended), "choice(s) appended successfuly")
                        break
    for gen in genres:
        temp_genre_title = list_of_genres[gen - 1]
        if temp_genre_title not in display_genre:
            display_genre.append(temp_genre_title)

def handle_artist_selection():
    temp = True
    while temp:
        temp = False
        user_artist = str(input('Enter the name of an artist: '))
        if user_artist == "":
            print("Invalid input. Try again")
            temp = True
            continue
        artist_search_results = spotify.get_artists(user_artist)
        i = 0
        while len(artist_search_results) > i:
            num = i+1
            global artists
            if artist_search_results[i]['name'] in artists:
                print(str(num) + '. [x] ' + artist_search_results[i]['name'])
            else:
                print(str(num) + '. [ ] ' + artist_search_results[i]['name'])
            i += 1
        artist_select = input('Please select artists as a comma-delimited list of numbers. Type "clear" to clear out artists.')
        if artist_select == 'clear' or artist_select == 'Clear':
            artists.clear()
            artist_dict.clear()
            break
        temp_artists = []
        selected_numbers = artist_select.split(',')
        for i in selected_numbers:
            try:
                temp_artists += [artist_search_results[int(i)-1]['name']]
                artist_dict[artist_search_results[int(i)-1]['name']] = artist_search_results[int(i)-1]['id']
            except:
                print('Invalid input. Try again')
                break
        artists = list(set(artists + temp_artists))


def handle_track_selection():
    temp = True
    while temp:
        temp = False
        user_track = str(input("Enter the title of a track: "))
        if user_track == "":
            print("Invalid input. Try again")
            temp = True
            continue
        track_search_results = spotify.get_tracks(user_track)
        i = 0
        #print(track_search_results)
        while len(track_search_results) > i:
            num = i + 1
            global tracks
            global track_dict
            if track_search_results[i]['id'] in track_dict:
                print(str(num) + '. [x] ' + track_search_results[i]['name'])
            else:
                print(str(num) + '. [ ] ' + track_search_results[i]['name'])
            i += 1
        track_select = input('Please select tracks as a comma-delimited list of numbers. Type "clear" to clear out tracks.')
        if track_select == 'clear' or track_select == 'Clear':
            tracks.clear()
            track_dict.clear()
            break
        temp_tracks = []
        selected_numbers = track_select.split(',')
        for i in selected_numbers:
            try:
                temp_tracks += [track_search_results[int(i) - 1]['name']]
                track_dict[track_search_results[int(i) - 1]['id']] = track_search_results[int(i) - 1]['name']
            except:
                print('Invalid input. Try again')
                break
        tracks = list(set(tracks + temp_tracks))





def get_recommendations():
    artist_list = list(artist_dict.values())
    track_list = list(track_dict.keys())
    total_length = len(artist_list) + len(tracks) + len(display_genre)
    if total_length < 1 or total_length > 5:
        print("Sorry, but number of preferred genres and artists must be between 1 and 5.")
        print("Please go back to the main menu and ensure that the amount of your preferences lies within this range")
        return
    print('Handle retrieving a list of recommendations here...')
    temp =  spotify.get_similar_tracks(artist_list, track_list, display_genre)
    data = {}


    track_list = []
    for item in temp['tracks']:
        new_track = {'name' : item['name'], 'artist_name' : item['artists'][0]['name'], 'album_image_url_small' : item['album']['images'][2]['url'],
        'album_name' : item['album']['name'], 'share_url' : item['external_urls']['spotify']}
        track_list.append(new_track)

    df = pd.DataFrame(track_list)
    print(df[['name', 'artist_name', 'share_url']])

    html_content = spotify.get_formatted_tracklist_table_html(track_list)

    #generate html file
    html_file = open('recommendedtracks.html', 'w')
    html_file.write(html_content)
    html_file.close()

    send_email = input('Would you like to email this list to a friend (y/n)?')
    while True:
        if send_email == 'y' or send_email == 'Y':
            from_email = input('What is your email?')
            to_emails = input('What is the email of your friend?')
            subject = "Playlist Recommendation (from Spotify)"
            html_content = input('What would you like to say to them about this playlist?') + html_content
            sendgrid.send_mail(from_email,to_emails, subject, html_content)
            break
        else:
            print("Canceling...")
            break

# Begin Main Program Loop:
while True:
    print_menu()
    choice = input('What would you like to do? ')
    if choice == '1':
        handle_genre_selection()
    elif choice == '2':
        handle_artist_selection()
    elif choice == '3':
        handle_track_selection()
    elif choice == '4':
        get_recommendations()
    elif choice == '5':
        print('Quitting...')
        break
    else:
        print(choice, 'is an invalid choice. Please try again.')
    print()
    input('Press enter to continue...')
