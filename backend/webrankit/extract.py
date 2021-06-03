import requests
import json
import re
from bs4 import BeautifulSoup

def extract_items_from_anilist(username, statuses):
    query = ''' query ($username: String, $statuses: [MediaListStatus]) {
      MediaListCollection(userName: $username, status_in: $statuses, type: ANIME) {
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
        'statuses': statuses # [CURRENT,PLANNING,PAUSED,COMPLETED,DROPPED,REPEATING]
    }
    url = 'https://graphql.anilist.co'

    response = requests.post(url, json={'query': query, 'variables': variables})
    if not response.status_code == 200:
        return {} 
        
    medialists = response.json()['data']['MediaListCollection']['lists']
    medialist_entries = [medialist['entries'] for medialist in medialists]
    entries = [item for sublist in medialist_entries for item in sublist]
    return entries

def extract_items_from_steam(steam_id):
    url = f'https://steamcommunity.com/id/{steam_id}/games/?tab=all&sort=playtime'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    p = re.compile(r'var rgGames = (.*);')
    tmp = ''
    for script in soup.find_all('script'):
        if script:
            m = p.search(str(script))
            if m is not None:
                tmp = m.group(1)
                break
    apps = json.loads(tmp)
    result = [] 
    for app in apps:
        result.append({
            'label': app['name'],
            'img_url': app['logo'].replace('capsule_184x69', 'header')
        })
    return result
    

