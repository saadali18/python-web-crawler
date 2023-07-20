from queue import Queue
import requests
import socket
from bs4 import BeautifulSoup
import re
import validators


def download_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None


def resolve_dns(url):
    return socket.gethostbyname(url)


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.string
    print("Title:", title)


content_seen = set()


def is_content_seen(content):
    return content in content_seen


def add_content_seen(content):
    content_seen.add(content)


def store_content(content):
    # Store the content in a database or a file system
    print("Storing content:", content)


def extract_urls(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Extract URLs from the HTML content
    urls = []
    for link in soup.find_all('a'):
        url = link.get('href')
        urls.append(url)
    return urls


def is_url_valid(url):
    return True if url and validators.url(url) else False


url_seen = set()


def is_url_seen(url):
    return url in url_seen


def add_url_seen(url):
    url_seen.add(url)


def store_url(url):
    print("Storing URL:", url)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Seed Urls
    seed_urls = [
        'https://webscraper.io/test-sites/e-commerce/static',
    ]

    # URL Frontier
    url_frontier = Queue()
    for url in seed_urls:
        url_frontier.put(url)

    # Running crawler
    while not url_frontier.empty():
        # Retrieve a URL from the URL frontier
        current_url = url_frontier.get()

        # Check if the URL has been visited before
        if is_url_seen(current_url):
            continue

        # Download HTML content of the URL
        html_content = download_html(current_url)

        # Check if the content has been seen before
        if is_content_seen(html_content):
            continue

        # Parse the HTML content
        parse_html(html_content)

        # Store the content
        store_content(html_content)
        add_content_seen(html_content)

        # Extract URLs from the HTML content
        extracted_urls = extract_urls(html_content)

        for url in extracted_urls:
            # Filter the extracted URLs
            if is_url_valid(url):
                # Check if the URL has been visited before
                if not is_url_seen(url):
                    url_frontier.put(url)
                    add_url_seen(url)

        # Store the visited URL
        store_url(current_url)
