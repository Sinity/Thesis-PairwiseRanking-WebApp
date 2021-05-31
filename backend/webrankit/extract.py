import requests

def extract_items_from_anilist(username, status):
    query = ''' query ($username: String, $status: MediaListStatus) {
      MediaListCollection(userName: $username, status: $status, type: ANIME) {
        lists {
          status
          entries {
            id
            score
            media {
              title {
                userPreferred
              }
              coverImage {
                extraLarge
                color
              }
            }
          }
        }
      }
    } '''

    variables = {
        'username': username,
        'status': status # [CURRENT,PLANNING,PAUSED,COMPLETED,DROPPED,REPEATING]
    }
    url = 'https://graphql.anilist.co'

    response = requests.post(url, json={'query': query, 'variables': variables})
    if not response.status_code == 200:
        return {} 
        
    medialists = response.json()['data']['MediaListCollection']['lists']
    medialist_entries = [medialist['entries'] for medialist in medialists]
    entries = [item for sublist in medialist_entries for item in sublist]
    return entries
