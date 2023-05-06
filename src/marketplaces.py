from bs4 import BeautifulSoup
import requests
import numpy as np

import statistics
import re
import json


class eBay:
    def __init__(self, item):
        self.item = item.replace(' ', '+')

    def _currency(self, string):
        pattern = r'([A-Za-z€£$¥₹])([\d,.]+(?:\.\d{1,2})?)'
        match = re.search(pattern, string)
        
        if match is None:
            raise ValueError("No currency value found in string")
        
        currency_value = float(match.group(2).replace(',', ''))
        return currency_value

    def get_current_prices(self):
        current_listings = []
        for page in range(1, 5):
            try:
                url = f'https://www.ebay.com/sch/i.html?_nkw={self.item}&_ipg=200&_pgn={page}'
                html = requests.get(url=url)
                soup = BeautifulSoup(html.text, 'html.parser')
                for product in soup.find_all('div', {'class': 's-item__wrapper clearfix'}):
                    price = product.find('span', {'class': 's-item__price'}).text
                    try:
                        price = self._currency(price)
                        current_listings.append(price)
                    except:
                        price = price.replace(' to', '')
                        price = price.split()
                        prices = [self._currency(item) for item in price]
                        current_listings.append(statistics.mean(prices))
            except requests.exceptions.HTTPError as e:
                pass
        return np.mean(current_listings)


    def get_sold_prices(self):
        sold_listings = []
        for page in range(1, 5):
            try:
                url = f'https://www.ebay.com/sch/i.html?_nkw={self.item}&_ipg=200&rt=nc&LH_Sold=1&_pgn={page}'
                html = requests.get(url=url)
                soup = BeautifulSoup(html.text, 'html.parser')
                for product in soup.find_all('div', {'class': 's-item__wrapper clearfix'}):
                    price = product.find('span', {'class': 's-item__price'}).text
                    try:
                        price = self._currency(price)
                        sold_listings.append(price)
                    except:
                        price = price.replace(' to', '')
                        price = price.split()
                        prices = [self._currency(item) for item in price]
                        sold_listings.append(statistics.mean(prices))
            except requests.exceptions.HTTPError as e:
                pass
        return np.mean(sold_listings)



class StockX:
    def __init__(self, item):
        self.item = item.replace(' ', '%20')

    def get_prices(self):
        url = f'https://stockx.com/api/browse?_search={self.item}'

        headers = {
            'accept': 'application/json',
            'accept-encoding': 'utf-8',
            'accept-language': 'en-GB,en;q=0.9',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'x-requested-with': 'XMLHttpRequest',
            'app-platform': 'Iron',
            'app-version': '2022.05.08.04',
            'referer': 'https://stockx.com/'
            }

        html = requests.get(url=url, headers=headers)
        output = json.loads(html.text)
        return output['Products'][0]



class Goat:
    def __init__(self, item):
        self.item = item.replace(' ', '%20')

    def get_prices(self):
        try:
            html = requests.post(
                url='https://2fwotdvm2o-dsn.algolia.net/1/indexes/ProductTemplateSearch/query', 
                headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0"}, 
                params={
                    'x-algolia-agent': 'Algolia for vanilla JavaScript 3.25.1',
                    'x-algolia-api-key': 'ac96de6fef0e02bb95d433d8d5c7038a',
                    'x-algolia-application-id': '2FWOTDVM2O'
                }, 
                json={"params": "query={}&facetFilters=(status%3Aactive%2C%20status%3Aactive_edit)%2C%20()&page=0&hitsPerPage=20".format(self.item)}
            )
            return json.loads(html.text)['hits'][0]
        except IndexError:
            headers = {
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                    'dnt': '1',
                    'origin': 'https://www.goat.com',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'cross-site',
                    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
            }
            url = f'https://ac.cnstrc.com/search/{self.item}?c=ciojs-client-2.27.9&key=key_XT7bjdbvjgECO5d8&i=0d562b86-f8cf-4b44-8277-ca435324260e&s=2&num_results_per_page=25&_dt=1653046311601'
            html = requests.get(url=url, headers=headers)
            output = json.loads(html.text)
            return output['response']['results'][0]['data']
        else:
            raise Exception



class Depop:
    def __init__(self, item):
        self.item = item.replace(' ', '+')

    def _return_mean(self, products):
        prices = []
        for product in products:
            prices.append(float(product['price']['priceAmount']))
        return np.mean(prices)

    def get_prices(self):
        url = f'https://webapi.depop.com/api/v2/search/products/?what={self.item}&itemsPerPage=200&country=us&currency=USD&sort=relevance'

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            }

        html = requests.get(url=url, headers=headers)
        output = json.loads(html.text)
        return self._return_mean(output['products'])



class Grailed:
    def __init__(self, item):
        self.item = item.replace(' ', '%20')
        self.raw_query = item

    def get_prices(self):
        html = requests.post(
            url='https://mnrwefss2q-dsn.algolia.net/1/indexes/*/queries', 
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
                'x-algolia-api-key': 'bc9ee1c014521ccf312525a4ef324a16',
                'x-algolia-application-id': 'MNRWEFSS2Q'
            }, 
            params={
                'x-algolia-agent': 'Algolia for JavaScript (4.14.3); Browser; JS Helper (3.11.3); react (18.2.0); react-instantsearch (6.24.3)',
                'x-algolia-api-key': 'bc9ee1c014521ccf312525a4ef324a16',
                'x-algolia-application-id': 'MNRWEFSS2Q'
            }, 
            json={"requests":[{"indexName":"Listing_production","params":f"analytics=true&clickAnalytics=true&enableABTest=true&enablePersonalization=true&facets=%5B%22department%22%2C%22category_path%22%2C%22category_size%22%2C%22designers.name%22%2C%22price_i%22%2C%22condition%22%2C%22location%22%2C%22badges%22%2C%22strata%22%5D&filters=&getRankingInfo=true&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&highlightPreTag=%3Cais-highlight-0000000000%3E&hitsPerPage=40&maxValuesPerFacet=100&numericFilters=%5B%22price_i%3E%3D0%22%2C%22price_i%3C%3D200000%22%5D&page=0&personalizationImpact=99&query={self.item}&tagFilters=&userToken=6e226728-7e73-4418-b2c0-697740a1d15a"},{"indexName":"Listing_production","params":f"analytics=false&clickAnalytics=false&enableABTest=true&enablePersonalization=true&facets=price_i&filters=&getRankingInfo=true&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&highlightPreTag=%3Cais-highlight-0000000000%3E&hitsPerPage=0&maxValuesPerFacet=100&page=0&personalizationImpact=99&query={self.item}&userToken=6e226728-7e73-4418-b2c0-697740a1d15a"},{"indexName":"Listing_sold_production","params":f"analytics=true&clickAnalytics=true&enableABTest=true&enablePersonalization=true&facets=%5B%22department%22%2C%22category_path%22%2C%22category_size%22%2C%22designers.name%22%2C%22price_i%22%2C%22condition%22%2C%22location%22%2C%22badges%22%2C%22strata%22%5D&filters=&getRankingInfo=true&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&highlightPreTag=%3Cais-highlight-0000000000%3E&hitsPerPage=40&maxValuesPerFacet=100&numericFilters=%5B%22price_i%3E%3D0%22%2C%22price_i%3C%3D200000%22%5D&page=0&personalizationImpact=99&query={self.item}&tagFilters=&userToken=6e226728-7e73-4418-b2c0-697740a1d15a"},{"indexName":"Listing_sold_production","params":f"analytics=false&clickAnalytics=false&enableABTest=true&enablePersonalization=true&facets=price_i&filters=&getRankingInfo=true&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&highlightPreTag=%3Cais-highlight-0000000000%3E&hitsPerPage=0&maxValuesPerFacet=100&page=0&personalizationImpact=99&query={self.item}&userToken=6e226728-7e73-4418-b2c0-697740a1d15a"}]}
        )
        return json.loads(html.text)['results'][0]
    
    def get_url(self):
        html = requests.post(
            url='https://www.grailed.com/api/searches',
            headers={
                'accept': 'application/json',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                'content-type': 'application/json',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
                'x-amplitude-id': '1683378837634'
            }, 
            json={"index_name":"Listing_sold_production","query":self.raw_query,"filters":{}}
        )
        return 'https://www.grailed.com/shop/' + json.loads(html.text)['data']['uuid']
