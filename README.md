# Used-Cars-Scraper

# Website Permissions.
### 1. carwow.co.uk

This project respects the robots.txt guidelines for the Carwow website. For details on what is allowed and disallowed for web crawlers, please refer to the robots.txt file included in this project.

This project respects the restrictions set in the robots.txt file by avoiding scraping any disallowed paths or content. The data accessed was strictly for educational purposes, in compliance with ethical scraping practices.


# 1. Intoduction

In this project, our goal was to gather and analyze car listings from three popular websites: Caewow, Lookers, and Cargaint. By scraping these websites, we aimed to create a database of car listings, including important details such as model, price, and location, to explore trends in the car market. The project involved using a variety of technologies to extract, process, and visualize the data, ultimately providing insights that could be useful for anyone interested in the car market.

# 2. Project Overview

In this section, we provide an overview of the technologies, tools, and websites used in the project. We also outline the flow of the project, from scraping the websites to visualizing the data.

### Scrapers Used
We used **Selenium** and **Splash** for web scraping:

- **Selenium**: A powerful tool for automating web browsers, which helped us interact with dynamic content on the websites.
- **Splash**: A headless browser designed for web scraping, which allowed us to render pages with JavaScript content before scraping.

### Tech Stack
The following technologies were used throughout the project:

- **Selenium**: Web scraping automation.
- **Splash**: Headless browser rendering for dynamic content.
- **Docker**: Containerization to ensure the project can run in any environment consistently.
- **Dash**: Framework for building interactive data visualizations and dashboards.
- **PostgreSQL**: A relational database to store and process the scraped data.
- **Python**: The main programming language used to write the scraping scripts, data processing, and dashboard logic.

### Websites Scraped
We focused on gathering data from the following car listing websites:

1. **Caewow**
2. **Lookers**
3. **Cargaint**

Each website offers a unique set of data related to car listings, including details like model, price, location, and availability. The goal was to compare the listings across these platforms and analyze trends.

### Project Flowchart
The project follows this flow:

1. **Scraping**: 
   - The scraper extracts data from the selected websites using Selenium and Splash.
   - Each website is crawled to gather car details like model, price, and location.

2. **Data Storage**:
   - The scraped data is processed and stored in a **PostgreSQL** database.
   - Data is organized into tables to facilitate querying and analysis.

3. **Data Visualization**:
   - The processed data is presented in interactive dashboards using **Dash**.
   - Visualizations highlight trends, price ranges, and geographical distributions of car listings.

4. **Deployment**:
   - The entire project is containerized using **Docker**, ensuring the environment is reproducible and deployable on any machine.
# 3. UI
gif (one gif will show user gives input and another gif will show skipping some features) that demonstartes how the whole thing works. (full demonstration)

# 4. Running the code (script)
explain how to run the code, dependencies and requirements, file/directory structure

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
open source. anyone can contrbute

