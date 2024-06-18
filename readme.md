### Extract Information from Websites
Extracts and stores the following data into MySQL database
- Social Media Links
- Tech Stack
- Meta Title
- Meta Description
- Payment Gateways (Links where subscription might be asked)
### Requirements:
    - Please check "others/requirements.txt" and ensure all the dependencies are installed.
    - Ensure there is "sites.txt" in "files" folder.
    - Ensure there are 3 python scripts
        1. main.py
        2. scrape_site.py
        3. setup_database.py
    - Ensure you're connected to internet

### Running program:
    - Run pip install -r others/requirements.txt
    - Execute main.py
    - Enter database username and password
    - Scraping should start


### **Dependencies:** The program uses the following libraries

- **Python**: Script is written in python, thus python interpreter is required to run the script.
- **Wappalyzer**: Python library to find technologies used by a website.
- **Requests**: Python library to make requests and fetch HTML from a site.
- **bs4**: Python library to extract information from HTML.
- **html5lib**: Python HTML parser for BeautifulSoup objects.
- **MySQL-connector-python**: Python library to connect python with MySQL database.
- **MySQL**: Database for storage of extracted information

### **Setup:**

- Open the location where the program scrips are stored.
- Make sure Python, MySQL and pip are available on your system.
- Open Powershell and change directory to the directory where program is stored.
- Run ‘pip install -r others/requirements.txt’ in command line to install all the dependencies.
- Place all the 3 scripts in the same directory and create a folder files with sites.txt in it. Put URLs of all the sites into sites.txt.
- Optionally, MySQL database can be set up using the others/setup.sql file.

### **Instructions:** Steps to run the program

- Ensure internet connection is available.
- Install all the python libraries mentioned in the “requirements.txt”.
- Ensure all the 3 scripts, main.py, scrape_site.py and setup_database.py are there in the same folder.
- Put the sites in “sites.txt” in the files folder.
- Run “main.py”.
- Enter credentials for database access.
- Ideally, Scrapping should start.
- The scraped data would be available in ‘scraped_data’ database.

### **Approach:** The approach used to perform the intended task.

- A database with required tables is set up.
- The URLs for sites are fetched from a text file and stored to a list.
- Server requests are made to each URL to get the HTML of the website.
- The page source is searched for specific tags to find the title and description of a website.
- Predefined RegEx patterns are used over the anchor tags in the website to fetch required social links and payment gateways.
- Python library Wappalyzer is used to extract technologies used in the website.
- MySQL connector is used to run SQL queries over MySQL database and store the data obtained by scraping the website.

### **Explanation of Program:** Follows is detailed explanation of working of the program.

- ‘main.py’ is the main script which executes the program. First, main() method is invoked to which performs the following tasks.
  - Invoke setup_dabase.setup() to create essential database and tables.
  - Make a connection with MySQL database.
  - Invoke get_sites() function to fetch sites from ‘files/sites.txt’ and store them in a list. Stops execution if false is returned by the function.
  - For each site fetched, execute scrape_site.scrape() function to scrape the required data from the website and store it into the database. Console messages are printed based on output from the function.
  - Finally, database connection is closed and execution ends.
- ‘setup_database.py’ is a secondary python script which is responsible for creating the required database and tables. It has setup() method which is used to set up the database. It also holds the name to the database in ‘DATABASE_NAME’ variable.
- ‘scrape_site.py’ is the script which is actually responsible for scraping required data from a website. It also holds various methods for scraping data from a website.
  - scape_title() function takes a BeautifulSoup object as argument and tries to extract the title tag from it. If failed, ‘NA’ is returned, else first 120 characters of the title are returned.
  - scrape_description() function takes BeautifulSoup object as argument and tries to extract meta tag with attribute name = ‘description’. If failed, ‘NA’ is returned, else first 500 characters are returned.
  - scrape_technologies() function takes website’s URL as input. A Wappalyzer object is used to analyse WebPage object of the site which returns the technologies used by the website as a list.
  - scrape_social_links() function takes a BeatifulSoup object as argument. Then, for a list of RegEx patterns, The BeautifulSoup object is searched for all the anchor tags whose href attribute matches the given RegEx pattern. The href of found anchor tags is stored into a set. Finally, the set is returned.
  - scrape_payment_gateway() function takes a BeatifulSoup object as argument. Then, for a list of RegEx patterns, The BeautifulSoup object is searched for all the anchor tags whose href attribute matches the given RegEx pattern. The href of found anchor tags is stored into a set. Finally, the set is returned.
  - insert_links() function is used to store links scraped into the database. It takes ‘cursor’, ‘website_id’, ‘links’, ‘query’, and ‘max_length’ as its arguments, then for each ‘link’ in set ‘links’, if the length of ‘link’ is less than ‘max_length’, ‘query’ is executed to store the ‘link’ and ‘website_id’ into database.
  - scrape() function is the most important function which is responsible for invoking other functions to scrape data and store them into the database. It takes website URL and CmySQLConnection object as arguments. It sends website server requests in order to get the HTML source for the page. If successfully fetched, BeautifulSoup object of the website is created. Further, it invokes all the scrapping functions and stores the returned value into the database. A warning message is printed if description was not found in a website. True or False is returned based on success of scraping and inserting.
