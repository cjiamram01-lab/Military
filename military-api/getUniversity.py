import requests
from bs4 import BeautifulSoup
import json


def scrape_thai_universities_to_json():
    # URL to scrape
    url = "https://www.lib.ru.ac.th/links/university.php"

    # Send HTTP request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)

        response.raise_for_status()  # Raise exception for HTTP errors

        # Set encoding for Thai language
        response.encoding = 'utf-8'  # Try utf-8 first, might need 'tis-620' for some Thai sites

        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        print(soup)

        # Find university links - adjust selector based on the actual page structure
        # This is a common pattern but might need adjustment after inspecting the page
        university_links = soup.select('div.content a, table a')

        universities = []

        for i, link in enumerate(university_links, 1):
            name = link.text.strip()
            url = link.get('href')

            # Skip empty entries
            if name and url:
                universities.append({
                    'id': i,
                    'name': name,
                    'url': url
                })

        # Write to JSON file
        with open('thai_universities.json', 'w', encoding='utf-8') as f:
            json.dump(universities, f, ensure_ascii=False, indent=4)

        print(f"Scraped {len(universities)} universities and saved to JSON.")

        # Also return the JSON as a string
        json_string = json.dumps(universities, ensure_ascii=False, indent=4)
        return json_string

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return json.dumps({"error": str(e)})


# Run the function if script is executed directly
if __name__ == "__main__":
    json_data = scrape_thai_universities_to_json()
    print("Sample of the JSON data:")
    print(json_data[:500] + "...")  # Print first 500 chars of the JSON