import requests_with_caching
import json

def get_movies_from_tastedive(movies):
    baseurl = "https://tastedive.com/api/similar"
    parameters = {}
    parameters["q"] = movies
    parameters["type"] = "movies"
    parameters["limit"] = 5 
    movie_resp = requests_with_caching.get(baseurl, params = parameters)
    #print(movie_resp.json())
    return movie_resp.json()

def extract_movie_titles(movieName):
    return [m['Name'] for m in movieName['Similar']['Results']]

def get_related_titles(movie_list):
    lst = []
    for movie in movie_list:
        lst.extend(extract_movie_titles(get_movies_from_tastedive(movie)))
    return list(set(lst))

def get_movie_data(title):
    url = 'http://www.omdbapi.com/'
    param = {}
    param['t'] = title
    param['r'] = 'json'
    this_page_cache = requests_with_caching.get(url, params=param)

    return json.loads(this_page_cache.text)

def get_movie_rating(dic):
    ranking = dic['Ratings']
    for dic_item in ranking:
        if dic_item['Source'] == 'Rotten Tomatoes':
            return int(dic_item['Value'][:-1])
    return 0
