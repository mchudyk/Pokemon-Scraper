import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status() 
        return response.text
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return ''  #returning an empty string instead of None


def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    pokemon_list = []
    product_list_items = soup.find_all('li', class_='product')

    for product in product_list_items:
        pokemon = {}

        #Extracting the ID
        product_classes = product.get('class', [])
        product_id_classes = [cls for cls in product_classes if cls.startswith('post-')]
        if product_id_classes:
            pokemon_id_str = product_id_classes[0].split('-')[1]
            pokemon['id'] = int(pokemon_id_str)  #converting to int

        #Extracting the name
        name_tag = product.find('h2', class_='woocommerce-loop-product__title')  # Updated class for the name tag
        if name_tag:
            pokemon['name'] = name_tag.text.strip()
        
        #Extracting the price
        price_tag = product.find('span', class_='woocommerce-Price-amount amount')
        if price_tag:
            currency_symbol = price_tag.find('span', class_='woocommerce-Price-currencySymbol').text
            pokemon['price'] = currency_symbol + price_tag.text.strip().replace(currency_symbol, '').strip()
        
        #Extracting the image URL
        image_tag = product.find('img', class_='wp-post-image')
        if image_tag:
            pokemon['image_url'] = image_tag['src']

        #Extracting the sku
        sku_tag = product.find('a', class_='add_to_cart_button') 
        if sku_tag and 'data-product_sku' in sku_tag.attrs:
            pokemon['sku'] = sku_tag['data-product_sku']      

        #Ideally, I could also check if there is no missing data 
        pokemon_list.append(pokemon)
        
    return pokemon_list


def get_next_page(soup, base_url):
    # This function returns the URL of the next page, if it exists
    next_button = soup.find("a", class_="next")
    if next_button and 'href' in next_button.attrs:
        next_page_url = urljoin(base_url, next_button['href'])
        return next_page_url
    else:
        return None