import requests

def (self):
    url = 'https://graphql.anilist.co'
    query = '''
    query ($id: Int) { # Define which variables will be used in the query (id)
      Media (id: $id, type: ANIME) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
        id
        title {
          romaji
          english
          native
        }
      }
    }
    '''

    variables = {
        'id': 15125
    }

    response = requests.post(url, json={'query': query, 'variables': variables})
    return response

