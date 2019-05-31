from apis import spotify
from apis import sendgrid

def print_menu():
    print('''
---------------------------------------------------------------------
Settings / Browse Options
---------------------------------------------------------------------
1 - Select your favorite genres
2 - Select your favorite artists
3 - Discover new music
4 - Quit
---------------------------------------------------------------------
    ''')

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



        # if user input is clear, then clear

def handle_artist_selection():
    # 1. Allow user to search for an artist using
    #    spotify.get_artists() function
    # 2. Allow user to store / modify / retrieve artists
    #    in order to get song recommendations

    user_artist = str(input('Enter the name of an artist: '))
    artist_search_results = spotify.get_artists(user_artist)
    #list_of_artist_names = artist_search_results
    i = 0
    while len(artist_search_results) > i:
        num = i+1
        print(str(num) + '. ' + str(artist_search_results[i]['name']))
        i += 1
    print('Please select up to three artists as a comma-delimited list of numbers. Type "clear" to clear out artists.')
    

# make sure it's simplified??

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
