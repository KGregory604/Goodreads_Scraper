import requests
from bs4 import BeautifulSoup

def get_description(book_id: str) -> str:
    """Returns the description of the book with book id == book_id
    Args:
        book_id: Goodreads unique identifier for a book
    Returns:
        Description of that book
    """

    url = 'https://www.goodreads.com/book/show/' + book_id

    # Perform an HTTP GET request to the given URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content with Beautiful Soup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the <div> element with class "BookPageMetadataSection"
        div_content = soup.find('div', class_='BookPageMetadataSection')
        if div_content:
            
            # Find all <span> elements within div_content
            spans = div_content.find_all('span', class_='Formatted')
            return spans[0].text
        else:
            return None
    else:
        return None
