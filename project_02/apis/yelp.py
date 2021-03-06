import urllib.request
from urllib.request import urlopen
import json
from apis import authentication, utilities
import pandas as pd


get_image_html = utilities.get_image_html
flatten_for_pandas = utilities.flatten_for_pandas
get_dataframe = utilities.get_dataframe
get_jupyter_styling = utilities.get_jupyter_styling


# https://www.yelp.com/developers/documentation/v3/business_search
def get_categories():
    '''
    Returns all of the available restaurant categories that the user
    can filter by on Yelp.
    '''
    categories = list(set([
        'mexican', 'sandwiches', 'breakfast_brunch', 'restaurants', 
        'food', 'mexican', 'sandwiches', 'breakfast_brunch', 'nightlife', 
        'bars', 'chinese', 'pizza', 'coffee', 'burgers', 'cafes', 'newamerican', 
        'hotdogs', 'japanese', 'tradamerican', 'foodtrucks', 'sushi', 'salad', 
        'vietnamese', 'delis', 'thai', 'seafood', 'italian', 'indpak', 
        'asianfusion', 'bbq', 'vegan', 'korean', 'noodles', 'bakeries', 
        'chicken_wings', 'mediterranean', 'cocktailbars', 'desserts', 
        'eventservices', 'vegetarian', 'foodstands', 'hotdog', 'latin', 
        'ethiopian', 'soup', 'juicebars', 'catering', 'gluten_free', 
        'soulfood', 'beerbar', 'himalayan', 'mideastern', 'ramen', 'tacos', 
        'sportsbars', 'tapasmallplates', 'wine_bars', 'french', 'grocery', 
        'gourmet', 'arts', 'comfortfood', 'diners', 'dimsum', 'southern', 
        'cajun', 'cantonese', 'caribbean', 'chickenshop', 'pubs', 'buffets', 
        'icecream', 'pakistani', 'poke', 'popuprestaurants', 'shopping', 
        'bagels', 'brazilian', 'donuts', 'gastropubs', 'greek', 'halal', 
        'streetvendors', 'hawaiian', 'creperies', 'filipino', 'venues', 
        'beer_and_wine', 'cheesesteaks', 'salvadoran', 'szechuan', 
        'waffles', 'african', 'bubbletea', 'fishnchips', 'peruvian', 
        'beergardens', 'burmese', 'falafel', 'musicvenues', 'spanish', 
        'convenience', 'german', 'izakaya', 'laotian', 'lounges', 'meats', 
        'tapas', 'breweries', 'cafeteria', 'hotpot', 'kebab', 'steak', 
        'taiwanese', 'tex-mex'
    ]))
    categories.sort()
    return categories

def get_categories_abridged():
    # feel free to modify this as you like
    categories = [
        'mexican', 'chinese', 'pizza', 'italian', 'thai', 'japanese',
        'vietnamese', 'asianfusion', 'ethiopian', 'korean', 'indpak',
        'mideastern', 'tapas', 'pakistani', 'brazilian', 'filipino',
        'african', 'greek', 'coffee', 'dessert'
    ]
    categories.sort()
    return categories

# retrieves data from any Spotify endpoint:
def _issue_get_request(url:str):
    token = authentication.get_token('https://www.apitutor.org/yelp/key')
    request = urllib.request.Request(url, None, {
        'Authorization': 'Bearer ' + token
    })
    try:
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read().decode())
            return data
    except urllib.error.HTTPError as e:
        error_message = e.read()
        error_message = '\n' + str(e) + '\n' + str(json.loads(error_message)) + '\n'
        raise Exception(error_message)

def _simplify_businesses(data:list):
    def get_alias(item):
        return item['alias']
    simplified = []
    for item in data['businesses']:
        business = {
            'id': item['id'],
            'name': item['name'],
            'rating': item['rating'],
            'image_url': item['image_url'],
            'display_address': '., '.join(item['location']['display_address']),
            'coordinates': item['coordinates'],
            'review_count': item['review_count'],
            'share_url': item['url'].split('?')[0],
            'categories': ', '.join(list(map(get_alias, item['categories'])))
        }
        try:
            business['price'] = item['price']
        except:
            pass
        simplified.append(business)
    return simplified

def _simplify_comments(data:list):
    simplified = []
    for item in data['reviews']:
        review = {
            'id': item['id'],
            'rating': item['rating'],
            'text': item['text'].replace('\n', ' '),
            'time_created': item['time_created'].split(' ')[0],
            'url': item['url']
        }
        simplified.append(review)
    return simplified

def get_businesses(location:str='Evanston, IL', limit:int=20, term:str=None, categories:str=None, sort_by:str=None, price:int=None, open_now:str=None, simplify:bool=True):
    '''
    Searches for Yelp businesses based on various search criteria, including:
    
        * location (str):   Location of the search
        * limit (int):      An integer indicating how many records to return. Max of 50.
        * term (str):       A search term
        * categories (str): One or more comma-delimited categories to filter by.
        * sort_by (str):    How to order search results. Options are: 
                            best_match, rating, review_count, distance
        * price (int):      How expensive 1, 2, 3, 4 or comma-delimited list, e.g.: 1,2
        * open_now (str):   Set to 'true' if you only want the open restaurants
        * simplify (bool):  Indicates whether you want to simplify the data that is returned.

    Returns a list of businesses matching your search / ordering / limit criteria.
    '''

    url = 'https://api.yelp.com/v3/businesses/search?location=' + \
        urllib.parse.quote_plus(location) + '&limit=' + str(limit)
    if term:
        url += '&term=' + urllib.parse.quote_plus(term)
    if categories:
        url += '&categories=' + categories
    if sort_by:
        if sort_by not in ['best_match', 'rating', 'review_count', 'distance']:
            raise Exception(sort_by + " not in ['best_match', 'rating', 'review_count', 'distance']")
        url += '&sort_by=' + urllib.parse.quote_plus(sort_by)
    if price:
        url += '&price=' + str(price)  #1, 2, 3, 4 -or- 1,2 (for more than one)
    if open_now:
        url += '&open_now=true' 

    print(url)       

    data = _issue_get_request(url)
    if not simplify:
        return data
    return _simplify_businesses(data)

def get_reviews(business_id:int, simplify:bool=True):
    '''
    Retrieves a list of Yelp reviews for a particular business.
        * business_id (int): [Required] An integer corresponding to the business id.
        * simplify (bool):   Indicates whether you want to simplify the data that is returned.
    Returns a list of reviews.
    '''
    # https://www.yelp.com/developers/documentation/v3/business_reviews
    url = 'https://api.yelp.com/v3/businesses/' + business_id + '/reviews'
    data = _issue_get_request(url)
    if not simplify:
        return data
    return _simplify_comments(data)

def get_formatted_business_table(business:dict, reviews:list=None, to_html=True):
    '''
    Makes a nice formatted HTML table of tracks. Good for writing to an 
    HTML file or for sending in an email.
        * tracks(list): [Required] A list of tracks
    Returns an HTML table as a string 
    '''
    if not business:
        print('A business is required.')
        return
    pd.set_option('display.max_colwidth', -1)
    
    # business table:
    keys = ['name', 'rating', 'price', 'review_count', 'display_address', 'categories', 'share_url']
    business_transposed = []
    for key in keys:
        business_transposed.append({
            'name': key,
            'value': str(business[key])
        })
    if to_html:
        # show image:
        business_transposed.append({
            'name': 'image',
            'value': '<img style="max-width: 300px;" src="' +  business['image_url'] + '" />'
        })
    df_business = get_dataframe(business_transposed)

    business_formatters={
        'name': '{{:<{}s}}'.format(df_business['name'].str.len().max()).format,
        'value': '{{:<{}s}}'.format(df_business['value'].str.len().max()).format
    }
    
    # reviews table:
    df_reviews = get_dataframe(reviews)
    df_reviews = df_reviews[['time_created', 'rating', 'text']]
    review_formatters={
        'time_created': '{{:<{}s}}'.format(df_reviews['time_created'].str.len().max()).format,
        'text': '{{:<{}s}}'.format(df_reviews['text'].str.len().max()).format
    }

    if to_html:
        table_1 = df_business.to_html(formatters=business_formatters, escape=False, header=None, index=False)
        table_2 = df_reviews.to_html(formatters=review_formatters, escape=False, index=False)
    
        html = '<h1>' + business['name'].upper() + '</h1>' + \
            table_1 + '<h2>Reviews</h2>' + table_2
        html = html.replace('style="text-align: right;"', '')
        html = html.replace('<tr>', '<tr style="border: solid 1px #CCC;">')
        html = html.replace(
            '<table border="1" class="dataframe">', 
            '<table style="border-collapse: collapse; border: solid 1px #CCC;width:700px;">'
        )
        return html
    else:
        table_1 = df_business.to_string(formatters=business_formatters, justify='left', index=False, header=None)
        table_2 = df_reviews.to_string(formatters=review_formatters, justify='left', index=False, header=None)
        row_len = 72
        pd.set_option('display.max_colwidth', 80)
        return (
            '-' * row_len + '\n' + 
            business['name'].upper() + '\n' +
            '-' * row_len + '\n' + 
            table_1 + 
            '\n\n Reviews:\n' + 
            table_2 +
            '\n' + '-' * row_len
        )