from apis import spotify
from apis import sendgrid

def print_menu():
    print('''
---------------------------------------------------------------------
Settings / Browse Options
---------------------------------------------------------------------
1 - Select your favorite genres {get_genres}
2 - Select your favorite artists {get_artists}
3 - Discover new music
4 - Quit
---------------------------------------------------------------------
    '''.format(
          get_genres=display_genre, 
          get_artists=artists))

display_genre = []
genres = []
artists = []


def handle_genre_selection():
    # 1. Allow user to select one or more genres using the
    #    spotify.get_genres_abridged() function
    # 2. Allow user to store / modify / retrieve genres
    #    in order to get song recommendations
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
                    print(temp_num)
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

        #For the last value that we miss
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
            for n in temp_genres:
                if n not in genres:
                    if len(genres) < 3:
                        genres.append(n)
                    else:
                        print("You may only have 3 genres")
                        break

    #for the title selection to appear on the menu
    # ONLY WORKS FOR ONE NUMBER HELP                    
    j=0
    while j<len(genres):
        temp_genre_title = list_of_genres[int(genre_select)-1]
        display_genre.append(temp_genre_title)
        j+=1

def handle_artist_selection():
    # 1. Allow user to search for an artist using
    #    spotify.get_artists() function
    # 2. Allow user to store / modify / retrieve artists
    #    in order to get song recommendations
    #list_of_artist_names = artist_search_results

    temp = True
    while temp:
        temp = False
        user_artist = str(input('Enter the name of an artist: '))
        artist_search_results = spotify.get_artists(user_artist)
        i = 0
        while len(artist_search_results) > i:
            num = i+1
            if num in artists:
                print(str(num) + '. [x] ' + artist_search_results[i]['name'])
            else:
                print(str(num) + '. [ ] ' + artist_search_results[i]['name'])
            i += 1
        artist_select = input('Please select up to three artists as a comma-delimited list of numbers. Type "clear" to clear out artists.')
        if artist_select == 'clear':
            artists.clear()
            break
        temp_artists = []
        temp_num = ""
        for char in artist_select:
            if (char < '0' or char > '9') and char != ',':
                print("Error: Numbers and commas only")
                temp = True
                temp_artists = []
                temp_num = ""
                break
            else:
                if char == ',':
                    print(temp_num)
                    num = int(temp_num)
                    if num > len(artist_search_results) or num < 1:
                        print("Not a valid selection")
                        temp = True
                        temp_artists = []
                        temp_num = ""
                        break
                    else:
                        temp_artists.append(num)
                        temp_num = ""
                else:
                    temp_num = temp_num + char
        #For the last value that we miss
        should_append = False
        for char in temp_num:
            if (char < '0' or char > '9') and char != ',':
                print("Error: Numbers and commas only")
                temp = True
                temp_artists = []
                break
            elif int(temp_num) > len(artist_search_results) or int(temp_num) < 1:
                print("Not a valid selection")
                temp = True
                temp_artists = []
                break
            else:
                should_append = True
        if should_append:
            temp_artists.append(int(temp_num))
        if len(temp_artists) > 3:
            print("Please choose up to 3 artists")
            temp = True
            temp_artists = []
            temp_num = ""
        else:
            for n in temp_artists:
                if n not in artists:
                    if len(artists) < 3:
                        genres.append(n)
                    else:
                        print("You may only have 3 artists")
                        break

def get_recommendations():
    print('Handle retrieving a list of recommendations here...')
    # 1. Allow user to retrieve song recommendations using the
    #    spotify.get_similar_tracks() function
    # 2. List them below

# Begin Main Program Loop:
while True:
    print_menu()
    choice = input('What would you like to do? ')
    if choice == '1':
        handle_genre_selection()
    elif choice == '2':
        handle_artist_selection()
    elif choice == '3':
        get_recommendations()
        # In addition to showing the user recommendations, allow them
        # to email recommendations to one or more of their friends using
        # the sendgrid.send_mail() function.
    elif choice == '4':
        print('Quitting...')
        break
    else:
        print(choice, 'is an invalid choice. Please try again.')
    print()
    input('Press enter to continue...')
