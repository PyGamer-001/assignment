import mysql.connector as msc
import scrape_site
import setup_database

# List to store site URLs from the sites.txt file
sites_list = []

def get_sites() -> bool:
    """
    Reads site URLs from 'files/sites.txt' and stores them in sites_list.
    
    Returns:
        bool: True if the sites are read successfully, False otherwise.
    """
    try:
        # Open the file containing the site URLs
        with open('files/sites.txt') as sites:
            # Read each site and add to the sites_list
            for site in sites:
                sites_list.append(site.strip())
        return True
    except Exception:
        # Print an error message if the file does not exist or cannot be read
        print("Please ensure that site.txt exists in files folder.")
        return False

def main(db_user: str, db_password: str):
    """
    Main function to set up the database, connect to it, and scrape sites.
    
    Args:
        db_user (str): Database username.
        db_password (str): Database password.
    """
    try:
        # Set up the database using the provided credentials
        setup_database.setup(db_user, db_password)
        print("Database setup successful")
    except Exception as e:
        # Print an error message if database setup fails
        print("We encountered some problem while setting up your database, follows is the error: \n")
        print(e)
        print("\nPlease refer to the readme file.")
        return
    
    try:
        # Connect to the database
        database = msc.connect(
            host="localhost",
            user=db_user,
            password=db_password,
            database=setup_database.DATABASE_NAME
        )
    except Exception:
        # Print an error message if the connection fails
        print("Could not connect to the database.")
        return

    # Read the sites from the sites.txt file
    if not get_sites(): 
        return
    
    # Iterate over each site URL in the sites_list and scrape it
    for site in sites_list:
        if not scrape_site.scrape(site, database):
            print("- Could not scrape")
        else:
            print(f"Successfully scraped: {site}")

    # Close the database connection
    database.close()

if __name__ == "__main__":
    # Prompt the user for database credentials
    db_user = input("Enter database username: ")
    db_password = input("Enter password to the database: ")
    # Run the main function with the provided credentials
    main(db_user, db_password)
