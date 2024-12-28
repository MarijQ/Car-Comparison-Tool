# Used Cars Scrapers
**Authors:**   Georgios Gkakos, Marij Qureshi, Het Suhagiya

## Websites Permissions

This project respects the robots.txt guidelines for the Carwow, Cargiant and Lookers websites. For details on what is allowed and disallowed for web crawlers, please refer to the robots.txt file included in this project.

This project respects the restrictions set in the robots.txt file by avoiding scraping any disallowed paths or content. The data accessed was strictly for educational purposes, in compliance with ethical scraping practices.

## Table of Contents

1. [Introduction](#Introduction)  
2. [Project Overview](#project-overview)   
3. [Scraping and Data Collection](#scraping-and-data-collection)  
4. [Data Storage and Preperation](#data-storage-and-management)  
5. [User Interface (UI)](#user-interface-(ui))  
6. [Running the Code](#running-the-code)  
7. [Future Improvements](#future-improvements)  
8. [Team and Contact](#team-and-contact)
9. [License](#license)

---

## Introduction

In this project, we aimed to collect and analyse car listings from three websites: Carwow, Lookers, and Cargiant. Our objective was to build a database capturing key details such as model, make, engine size, and price. This information helps provide a reliable average price for the used car market in the UK, useful for both buyers and sellers. We used various technologies to scrape and process the data. Ultimately, we developed an application that allows users to input their car preferences and retrieve the average price from our database.

## Project Overview

We utilise a combination of web scraping technologies and database management tools to extract and process data from targeted websites. Our workflow moves from data acquisition through scraping to data storage and user interaction via a custom application.

#### Websites Scraped

-  **Carwow** : https://www.carwow.co.uk/used-cars
-  **Lookers** : https://www.lookers.co.uk/used-cars
-  **Cargiant** : https://www.cargiant.co.uk/search/

Each website offers a unique set of data related to used car listings, including details like model, price, engine size, hp, mpg etc.

#### Tech Stack

- **Scrapy**:  Orchestrated the web scraping process, data processing and data storgage.
- **Selenium**: Helped us interact with dynamic content on the websites.
- **Splash**:  Allowed us to render pages with JavaScript content in a headless browser before scraping.
- **PostgreSQL**: The relational database used to store and process the scraped data.
- **Python**: The main programming language used to write the scraping scripts, data processing, and dashboard logic.
- **Tkinter**: 

## Scraping and Data Collection

1. **Scraping**: 
   - The spiders extract data from the selected websites using Selenium and Splash.
   - Each website is crawled to gather car details like model, price, and location.

2. **Data Storage**:
   - The scraped data is processed and stored in a **PostgreSQL** database.
   - Data from all three websites is organised into a single table to facilitate querying and analysis.

3. **Interactions with Tkinter**: FIX SECTIONS

# 3. UI
gif (one gif will show user gives input and another gif will show skipping some features) that demonstartes how the whole thing works. (full demonstration)



# 4. Running the code (script)
explain how to run the code, dependencies and requirements, file/directory structure
ADD versions used 
ADD commands for how to run the code
ADD how the user can use tkinter





# 5. Data Prep
table of features used, explain missing values handling 

# 6. Future Work
what else can be done, new methods (if any), potential improvements in the current work.

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

# 7. Licence
This project is licensed under the MIT License. See the [LICENSE](License) file for more details.

