# Used Cars Scraper
**Authors:**   Georgios Gkakos, Marij Qureshi, Het Suhagiya

## Websites Permissions

This project respects the robots.txt guidelines for the Carwow, Cargiant and Lookers websites. For details on what is allowed and disallowed for web crawlers, please refer to the robots.txt file included in this project.

This project respects the restrictions set in the robots.txt file by avoiding scraping any disallowed paths or content. The data accessed was strictly for educational purposes, in compliance with ethical scraping practices.

## Table of Contents

1. [Introduction](#Introduction)  
2. [Project Overview](#project-overview)   
3. [Scraping and Data Collection](#scraping-and-data-collection)  
4. [Data Storage and Preparation](#data-storage-and-preparation)  
5. [User Interface](#user-interface)  
6. [Running the Code](#running-the-code)  
7. [Future Improvements](#future-improvements)  
8. [Team and Contact](#team-and-contact)
9. [License](#license)

---

## Introduction

In this project, we aimed to collect and analyse car listings from three websites: Carwow, Lookers, and Cargiant. Our objective was to build a database capturing key details such as model, make, engine size, and price and provide a reliable average price for the used car market in the UK, useful for both buyers and sellers. We used various technologies to scrape and process the data. Ultimately, we developed an application that allows users to input their car preferences and retrieve the average price from our database.

## Project Overview

We utilise a combination of web scraping technologies and database management tools to extract and process data from targeted websites. Our workflow moves from data acquisition through scraping to data storage and user interaction via a custom application.

--- Websites Scraped ---

-  **Carwow** : https://www.carwow.co.uk/used-cars
-  **Lookers** : https://www.lookers.co.uk/used-cars
-  **Cargiant** : https://www.cargiant.co.uk/search/

Each website offers a unique set of data related to used car listings, including details like model, price, engine size, hp, mpg etc.

--- Tech Stack ---

- **Scrapy**:  Orchestrated the web scraping process, data processing and data storage.
- **Selenium**: Helped us interact with dynamic content on the websites.
- **Splash**:  Allowed us to render pages with JavaScript content in a headless browser before scraping.
- **PostgreSQL**:  Used to store and process the scraped data.
- **Python**:  Used to write the scraping scripts, data processing, and dashboard logic.
- **Tkinter**: Utilised to build an application that demonstrates user's interaction with the database  

## Scraping and Data Collection
Three spiders were created, one for each website:
- lookers.py: **Scrapy** to scrape most of the cars' features from the ajax api calls of the website that stored the data in json format and **Splash** to render the javascript content and scrape the extra feature list of cars
- cargiant.py, carwow.py: **Scrapy** with **Selenium** to scrape the dynamically loaded data from the corresponding websites as splash could not handle the very deep structure of javascript and html of the two websites.

From all three websites, the data scraping of features was standardised so that the data can be accomodated in a common table in a database.

The following features were scraped: make, model, price, mileage, fuel type, body style, engine size, hp, transmission, year, dealership name, mpg, number of doors, previous owners, droplet, additional features list


## Data Storage and Preparation
   - The scraped data is processed and stored in a **PostgreSQL** database.
   - Data from all three websites is organised into a single table to facilitate querying and analysis

Table's Structure and Description:
| Column Name      | Data Type      | Description                                   |
|------------------|----------------|-----------------------------------------------|
| id               | SERIAL         | Primary key, auto-increments with each entry  |
| make             | VARCHAR(100)   | Brand of the car                              |
| model            | VARCHAR(100)   | Model of the car                              |
| price            | NUMERIC        | Sale price of the car                         |
| mileage          | NUMERIC        | Total miles driven by the car                 |
| fuel_type        | VARCHAR(50)    | Type of fuel used (e.g., Diesel, Petrol)      |
| body_style       | VARCHAR(100)   | Style of the car body (e.g., Sedan, SUV)      |
| engine_size      | VARCHAR(50)    | Engine size (e.g., 2.0L)                      |
| hp               | VARCHAR(50)    | Horsepower of the car                         |
| transmission     | VARCHAR(50)    | Type of transmission (e.g., Manual, Automatic)|
| year             | INT            | Year of manufacture                           |
| dealership_name  | VARCHAR(255)   | Name of the dealership selling the car        |
| mpg              | VARCHAR(50)    | Miles per gallon                              |
| n_doors          | VARCHAR(50)    | Number of doors                               |
| previous_owners  | VARCHAR(50)    | Number of previous owners                     |
| droplet          | VARCHAR(50)    | Colour of the car                             |
| feature_list     | TEXT           | List of additional features                   |
| last_updated     | TIMESTAMP      | Timestamp of the last update to the record    |

## User Interface




## Running the code
explain how to run the code, dependencies and requirements, file/directory structure
ADD versions used 
ADD commands for how to run the code
ADD how the user can use tkinter

## Future Improvements
- Recommendation system
- competitor analysis
- car comparision based on the user inputs
- Car Depreciation Prediction based on the car age, its original price, current price and the no. of owners
- Web-Scraping: Add more sites like AutoTrader; improve anti-bot techniques.
- Web-Scraping: Handle CAPTCHA and use proxy rotation for dynamic scraping.
- ETL: Automate missing data handling; clean inconsistent records.
- ETL: Schedule real-time scraping for fresh data syncs (daily scheduled scrape).
- Analytics: Build ML models to predict car prices using features.
- Analytics: Analyze multi-year trends for pricing and popular models.
- UI: Upgrade GUI to modern web app with Flask or React.
- UI: Add intelligent filters based on user preferences (e.g. combinations of filters)
- NLP: Analyze seller descriptions for tone, sentiment, or key details.
- ⁠Integrate an ML model that can handle missing values on the explanatory features and calculates the average price
- ⁠Create a web application that provides a more attractive UI to the user to use.
- ⁠Run all the scrapers in parallel on a distributed system (such as spark) to enhance the runtime.
- ⁠Incorporate new websites to the database to make the calculation of the average price more representative of the current market.
- ⁠Group the calculations of the average price by location to account for spatial variation in prices of used cars in the UK.
- ⁠Add a tool that will calculate the insurance cost based on the generated average price among with other inputs (such as age of the user)
- ⁠Enhance the runtime of the scrapers that have to load different pages to collect the data using VPN (parallelizing the process)
- ⁠How a difference in features might impact the price (for example a car having a 20mpg less than the other) through a linear model (after handling missing values)

## Team and Contact

## License
This project is licensed under the MIT License. See the [LICENSE](License) file for more details.

