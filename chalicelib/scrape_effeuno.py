import urllib.request
import re
import json
import sys

URL = 'https://www.effeuno.biz/it/negozio/linea-easy-pizza/easy-pizza-pro/p134ha-509-pro/'

def fetch_html(url):
    """Fetch HTML content from the given URL."""
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching URL: {e}", file=sys.stderr)
        return None

def extract_price(html):
    """Extract the product price from HTML."""
    # Look for the main product price pattern in <p class="price">
    price_pattern = r'<p class="price">.*?<bdi>([0-9,]+)<span class="woocommerce-Price-currencySymbol">'
    match = re.search(price_pattern, html)
    return match.group(1) if match else ''

def extract_promotion(html):
    """Extract the promotion text from HTML."""
    # Look for "SPEDIZIONE GRATUITA SOLO PER AGOSTO. Accessori inclusi: PIETRA EFFEUNO"
    promotion_pattern = r'SPEDIZIONE GRATUITA SOLO PER AGOSTO[^"]*PIETRA EFFEUNO'
    match = re.search(promotion_pattern, html)
    return match.group(0) if match else ''

def scrape_effeuno():
    """Main function to scrape price and promotion from Effeuno website."""
    html = fetch_html(URL)
    if not html:
        return None
    
    price = extract_price(html)
    promotion = extract_promotion(html)
    
    result = {
        'price': price,
        'promotion': promotion
    }
    
    return result

if __name__ == '__main__':
    result = scrape_effeuno()
    if result:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Failed to scrape website", file=sys.stderr)
        sys.exit(1)