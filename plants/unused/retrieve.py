import requests
import json
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

# set up the API endpoint URL and query parameters for Glacier National Park observations
glacier_url = 'https://api.inaturalist.org/v1/observations'
glacier_params = {
    'per_page': 200, # maximum number of results per page
    'place_id': 6804, # Glacier National Park place ID
    'taxon_id': 47126, # plant taxon ID
    'order': 'desc',
    'order_by': 'observed_on',
    'quality_grade': 'research'
}

# set up the API endpoint URL and query parameters for the user's observations
user_url = 'https://api.inaturalist.org/v1/observations'
user_params = {
    'per_page': 200, # maximum number of results per page
    'user_id': 'apsmith10', # replace with your iNaturalist user ID
    'order': 'desc',
    'order_by': 'observed_on',
    'taxon_id': 47126, # plant taxon ID

}

# function to retrieve observations from the API
def get_observations(url, params):
    results = []
    page = 1
    total_results = float('inf')
    while len(results) < total_results:
        params['page'] = page
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            print(f'Encountered MaxRetryError: {e}')
            break
        except requests.exceptions.RequestException as e:
            print(f'Request failed with error: {e}')
            break
        response_json = response.json()
        total_results = response_json['total_results']
        results.extend(response_json['results'])
        page += 1
    return results

# use ThreadPoolExecutor to retrieve observations in parallel
with ThreadPoolExecutor(max_workers=2) as executor:
    glacier_future = executor.submit(get_observations, glacier_url, glacier_params)
    user_future = executor.submit(get_observations, user_url, user_params)

glacier_results = glacier_future.result()
user_results = user_future.result()
print(f'Len glac: {len(glacier_results)}')
print(f'User glac: {len(user_results)}')

# Extract the scientific names of the plant species from the API response
plant_species = []
for result in glacier_results['results']:
    if 'Plantae' in result['taxon']['iconic_taxon_name']:
        if result['taxon']['id'] not in user_results:
            plant_species.append(f"{result['taxon']['name']}, {result['taxon']['preferred_common_name']}")

# Find the 10 most observed from this list
string_counts = Counter(plant_species)
common_obs = [f'{string}, {count}'  for string, count in string_counts.most_common(10)]

# Print the top 10 most observed plant species in Glacier National Park, MT
print('Top 10 Most Observed Plant Species in Glacier National Park, MT (excluding species observed by you):')
for i, species in enumerate(common_obs[:10]):
    print(f'{i+1}. {species}')
