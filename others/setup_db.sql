CREATE DATABASE IF NOT EXISTS scraped_data;

USE scraped_data;

CREATE TABLE IF NOT EXISTS websites(website_id INT AUTO_INCREMENT PRIMARY KEY, website_name VARCHAR(120), website_description TEXT);
CREATE TABLE IF NOT EXISTS social_links(id INT, social_link VARCHAR(60), FOREIGN KEY(id) REFERENCES websites(website_id));
CREATE TABLE IF NOT EXISTS technologies(id INT, technologies VARCHAR(50), FOREIGN KEY(id) REFERENCES websites(website_id));
CREATE TABLE IF NOT EXISTS payment_gateways(id INT, payment_gateway VARCHAR(120), FOREIGN KEY(id) REFERENCES websites(website_id));