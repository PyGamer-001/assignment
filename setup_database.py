import mysql.connector as msc

# Define the name of the database
DATABASE_NAME = "scraped_data"

# Define the SQL commands to create tables
TABLES = {
    "websites": """
        CREATE TABLE IF NOT EXISTS websites(
            website_id INT AUTO_INCREMENT PRIMARY KEY,
            website_name VARCHAR(120),
            website_description TEXT
        )
    """,
    "social_links": """
        CREATE TABLE IF NOT EXISTS social_links(
            id INT,
            social_link VARCHAR(60),
            FOREIGN KEY(id) REFERENCES websites(website_id)
        )
    """,
    "technologies": """
        CREATE TABLE IF NOT EXISTS technologies(
            id INT,
            technologies VARCHAR(50),
            FOREIGN KEY(id) REFERENCES websites(website_id)
        )
    """,
    "payment_gateway": """
        CREATE TABLE IF NOT EXISTS payment_gateways(
            id INT,
            payment_gateway VARCHAR(120),
            FOREIGN KEY(id) REFERENCES websites(website_id)
        )
    """
}

def setup(user: str, password: str):
    """
    Sets up the database and creates necessary tables.

    Args:
        user (str): Database username.
        password (str): Database password.
    """
    # Connect to the MySQL server
    database = msc.connect(
        host="localhost",
        user=user,
        password=password
    )

    # Create a cursor object to interact with the database
    cursor = database.cursor()

    # Create the database if it doesn't exist
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")

    # Select the database
    database.database = DATABASE_NAME

    # Create a new cursor object for executing table creation queries
    cursor = database.cursor()

    # Execute each table creation query defined in TABLES
    for query in TABLES.values():
        cursor.execute(query)

    # Close the database connection
    database.close()

if __name__ == "__main__":
    # Inform the user to run the main.py script
    print("Please run main.py")
