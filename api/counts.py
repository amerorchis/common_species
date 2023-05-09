import requests
import json

class Species:
    def __init__(self, count, id, sci, common=None):
        self.count = count
        self.sci = f'<i>{sci.capitalize()}</i>'
        self.common = common
        self.id = id
    
    def name(self):
        if self.common:
            return f'{self.common.capitalize()}, {self.sci} - {self.count} observations'
        else:
            return f'{self.sci} - {self.count} observations'

    
    def __str__(self):
        return self.name()

def get_glac():
    url1 = 'https://api.inaturalist.org/v1/observations/species_counts?verifiable=true&spam=false&place_id=72841&quality_grade=research&taxon_id=47126&locale=en-US&page=1&per_page=500'
    url2 = 'https://api.inaturalist.org/v1/observations/species_counts?verifiable=true&spam=false&place_id=72841&quality_grade=research&taxon_id=47126&locale=en-US&page=2&per_page=500'

    r1 = requests.get(url1)
    d1 = json.loads(r1.text)
    results = d1['results']

    r2 = requests.get(url2)
    d2 = json.loads(r2.text)
    results2 = d2['results']

    results.extend(results2)

    return [Species(i['count'], i['taxon']['id'], i['taxon']['name'], i['taxon']['preferred_common_name']) for i in results]

def get_me() -> list:
    url = 'https://api.inaturalist.org/v1/observations/species_counts?verifiable=any&hrank=species&iconic_taxa%5B%5D=Plantae&user_id=apsmith10&locale=en&preferred_place_id=1&per_page=500'
    r1 = requests.get(url)
    d1 = json.loads(r1.text)
    results = d1['results']
    return [i['taxon']['id'] for i in results]


def exclude_observed():
    glac = get_glac()
    me = get_me()

    species_supressed = []
    for i in glac:
        if i.id not in me:
            species_supressed.append(i)
    
    sorted_species = sorted(species_supressed, key=lambda x: x.count, reverse=True)
    species = sorted_species[:25]
    return species

def get_species_list():
    top = []
    for i, species in enumerate(exclude_observed()):
        top.append(f'{species.name()}, <a href="https://www.inaturalist.org/observations?place_id=72841&taxon_id={species.id}" target="_blank">link</a>')
    return top

def species_seen():
    url = 'https://api.inaturalist.org/v1/observations/species_counts?verifiable=any&nelat=49.1766936942157&nelng=-112.2055199539685&swlat=46.64680635363439&swlng=-115.32946353584053&user_id=apsmith10&iconic_taxa%5B%5D=Plantae&locale=en&preferred_place_id=1&per_page=500'
    r = requests.get(url)
    data = json.loads(r.text)
    return data['total_results']
