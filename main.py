from scraper import fetch_page, parse_page, get_next_page
from bs4 import BeautifulSoup
import json

def main():
    base_url = 'https://scrapeme.live/shop/'
    url = base_url  
    all_pokemon = []
    while url:
        page_content = fetch_page(url)
        if page_content: 
            page_pokemon = parse_page(page_content)
            all_pokemon.extend(page_pokemon)
            soup = BeautifulSoup(page_content, 'html.parser')
            url = get_next_page(soup, base_url)
        else:
            print(f"Finished scraping. No more content or failed to fetch page for URL: {url}")
            break

    unique_pokemon = remove_duplicates(all_pokemon)
    write_to_json(unique_pokemon)

def remove_duplicates(pokemon_list):
    #the function removes duplicate elements by checking their ids
    unique_list = []
    seen = set()
    for pokemon in pokemon_list:
        if pokemon['id'] not in seen:
            seen.add(pokemon['id'])
            unique_list.append(pokemon)
    return unique_list

def write_to_json(pokemon_list, filename='result.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(pokemon_list, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()