from Wappalyzer import WebPage, Wappalyzer
from bs4 import BeautifulSoup
from mysql.connector.connection_cext import CMySQLConnection
import warnings
import requests
import re

# Suppress warnings
warnings.filterwarnings('ignore')

# SQL insert queries for different tables
INSERT_WEBSITE = "INSERT INTO websites (website_name, website_description) VALUES(%s, %s)"
INSERT_SOCIAL_LINK = "INSERT INTO social_links VALUES(%s, %s)"
INSERT_TECHNOLOGIES = "INSERT INTO technologies VALUES(%s, %s)"
INSERT_PAYMENT_GATEWAY = "INSERT INTO payment_gateways VALUES(%s, %s)"

def scrape_title(soup: BeautifulSoup) -> str:
    """
    Scrapes the title from the BeautifulSoup object.

    Args:
        soup (BeautifulSoup): BeautifulSoup object of the webpage.

    Returns:
        str: The title of the webpage, truncated to 120 characters if longer.
    """
    try:
        title = soup.title.get_text()
    except Exception:
        return "NA"
    return title[:120] if len(title) > 120 else title

def scrape_description(soup: BeautifulSoup) -> str:
    """
    Scrapes the meta description from the BeautifulSoup object.

    Args:
        soup (BeautifulSoup): BeautifulSoup object of the webpage.

    Returns:
        str: The meta description of the webpage, truncated to 500 characters if longer.
    """
    try:
        description = soup.find("meta", attrs={"name": "description"})['content']
    except Exception:
        return "NA"
    return description[:500] if len(description) > 500 else description

def scrape_technologies(website: str) -> list:
    """
    Uses Wappalyzer to identify the technologies used by the website.

    Args:
        website (str): URL of the website.

    Returns:
        list: A list of technologies used by the website.
    """
    webpage = WebPage.new_from_url(website)
    wappalyzer = Wappalyzer.latest()
    return wappalyzer.analyze(webpage)

def scrape_social_links(soup: BeautifulSoup) -> set:
    """
    Scrapes social media links from the BeautifulSoup object based on predefined patterns.

    Args:
        soup (BeautifulSoup): BeautifulSoup object of the webpage.

    Returns:
        set: A set of social media links found on the webpage.
    """
    link_patterns = [
        "https://(www[.])?instagram.com/.+",
        "https://(www[.])?facebook.com/.+",
        "https://(www[.])?twitter.com/.+",
        "https://(www[.])?youtube.com/user/.+",
        "https://(www[.])?tiktok.com/.+",
        "https://(www[.])?linkedin.com/company/.+"
    ]
    social_links = set()
    for pattern in link_patterns:
        result = soup.find_all("a", href=re.compile(pattern))
        for link in result:
            social_links.add(link["href"])
    return social_links

def scrape_payment_gateway(website_url: str, soup: BeautifulSoup) -> set:
    """
    Scrapes potential payment gateway links from the BeautifulSoup object based on predefined patterns.

    Args:
        website_url (str): URL of the website.
        soup (BeautifulSoup): BeautifulSoup object of the webpage.

    Returns:
        set: A set of payment gateway links found on the webpage.
    """
    link_patterns = [
        f"{website_url}/?subscribe.*",
        f"{website_url}/?subscription.*",
        f"{website_url}/?donate.*",
        "https://.*/subscribe/.*",
        "https://.*/donate/.*",
        "https://.*/subscription/.*",
        "https://.*/buy/.*",
        "https://(www[.])?paypal.me/.+",
        "https://(www[.])?razorpay.+",
        "https://(www[.])?stripe.+",
    ]
    payment_portals = set()
    for pattern in link_patterns:
        result = soup.find_all("a", href=re.compile(pattern))
        for link in result:
            payment_portals.add(link["href"])
    return payment_portals

def insert_links(cursor, website_id: int, links: set, query: str, max_length: int):
    """
    Inserts links into the database.

    Args:
        cursor: MySQL cursor object.
        website_id (int): The ID of the website.
        links (set): A set of links to insert.
        query (str): The SQL insert query.
        max_length (int): The maximum length of the links to insert.
    """
    for link in links:
        if len(link) < max_length:
            cursor.execute(query, (website_id, link))

def scrape(website_url: str, database: CMySQLConnection) -> bool:
    """
    Main function to scrape a website, extract relevant information, and store it in the database.

    Args:
        website_url (str): URL of the website to scrape.
        database (CMySQLConnection): Connection object to the MySQL database.

    Returns:
        bool: True if the scraping and database insertion were successful, False otherwise.
    """
    try:
        response = requests.get(website_url)
    except Exception as e:
        print(f"Error connecting to {website_url}: {e}")
        return False
    
    if response.status_code == 200:
        website_source = response.text
        soup = BeautifulSoup(website_source, 'html5lib')
        try:
            title = scrape_title(soup)
            desc = scrape_description(soup)

            with database.cursor() as cursor:
                cursor.execute(INSERT_WEBSITE, (title, desc))
                website_id = cursor.lastrowid

                # Scrape and store social links
                social_links = scrape_social_links(soup)
                insert_links(cursor, website_id, social_links, INSERT_SOCIAL_LINK, 60)

                # Scrape and store technologies
                technologies = scrape_technologies(website_url)
                insert_links(cursor, website_id, technologies, INSERT_TECHNOLOGIES, 60)

                # Scrape and store payment gateways
                payment_gateways = scrape_payment_gateway(website_url, soup)
                insert_links(cursor, website_id, payment_gateways, INSERT_PAYMENT_GATEWAY, 120)

                database.commit()

            if desc == "NA":
                print(f"[WARNING]: Could not find description for {website_url}")
            return True
        except Exception as e:
            print(f"Problem caused by: {website_url}")
            print(f"Problem caused: {e}")
            return False
    else:
        print(f"Error connecting to {website_url}: {response.status_code}")
        return False

if __name__ == "__main__":
    print("Please run main.py")
