# Used Cars Scraper

> ## Website Permissions
>
> This project respects the terms and conditions for the Carwow, Cargiant and Lookers websites at the time of development. The data accessed was strictly for educational purposes, in compliance with ethical scraping practices. For details on what is allowed and disallowed for web crawlers when using these tools, please refer to the latest site terms and robots.txt files.

## Table of Contents

1. [Introduction](#introduction)  
2. [Project Overview](#project-overview)   
3. [Scraping and Data Collection](#scraping-and-data-collection)  
4. [Data Storage and Preparation](#data-storage-and-preparation)
5. [Average Price Generation](#average-price-generation) 
6. [User Interface](#user-interface)  
7. [Running the Code](#running-the-code)  
8. [Future Improvements](#future-improvements)  
9. [Team and Contact](#team-and-contact)
10. [License](#license)

---

## Introduction

Finding a fair price for a used car can be challenging, whether buying or selling. This project provides a data-driven solution by analysing 1,000+ listings from 3 major comparison sites: Carwow, Lookers, and Cargiant, to estimate the average market price for used cars in the UK. By collecting details such as model, make, engine size, and price, it builds a reliable pricing database that helps users make informed decisions.

The python GUI application allows users to input their car preferences and instantly retrieve an estimated market price based on real listings. Various technologies are used to scrape, process, and analyse the data, ensuring that pricing insights remain accurate and up to date. This makes it a valuable tool for anyone looking to gauge the true value of a vehicle before making a purchase or a sale.

---

## Project Overview

A combination of web scraping technologies and database management tools is utilised to extract and process data from targeted websites. The workflow progresses from data acquisition through scraping to data storage and user interaction via a custom application.

### Websites Scraped

-  **Carwow** : https://www.carwow.co.uk/used-cars
-  **Lookers** : https://www.lookers.co.uk/used-cars
-  **Cargiant** : https://www.cargiant.co.uk/search/

Each website offers a unique set of data related to used car listings, including details like model, price, engine size, hp, mpg etc.

### Tech Stack

- **Scrapy**: Orchestrates the web scraping process, data processing, and data storage.  
- **Selenium**: Enables interaction with dynamic content on the websites.  
- **Splash**: Renders pages with JavaScript content in a headless browser before scraping.  
- **PostgreSQL**: Stores and processes the scraped data.  
- **Python**: Powers the scraping scripts, data processing, and dashboard logic.  
- **Tkinter**: Builds an application that allows user interaction with the database.

---

## Scraping and Data Collection
Three spiders were developed, each tailored to efficiently scrape data from a specific website:  

### **Spiders**  

- **lookers.py**:  
  - **Tools Used**: Utilises Scrapy to extract car features directly from AJAX API calls, returning data in JSON format.  
  - **Additional Rendering**: Uses Splash to render JavaScript content, enabling the scraping of dynamically loaded feature lists.  

- **cargiant.py** and **carwow.py**:  
  - **Tools Used**: Employ Scrapy alongside Selenium. This combination is essential for handling complex JavaScript and HTML structures that Splash alone cannot process.  

### **Data Standardisation**  

To integrate scraped data into a unified database schema, the extraction of key features was standardised across all three websites:  

- **Basic Car Information**: Make, Model, Year, Price, Mileage  
- **Specifications**: Fuel Type, Body Style, Engine Size, Horsepower (hp)  
- **Transmission Details**: Type of Transmission  
- **Dealership Data**: Name of the Dealership  
- **Efficiency and Capacity**: Miles Per Gallon (mpg), Number of Doors  
- **Ownership History**: Number of Previous Owners  
- **Additional Details**: Droplet, List of Additional Features

---

## **Data Storage and Preparation**  

The scraped data is processed and stored in a **PostgreSQL** database.  

### **Table Structure and Description**  

| Column Name      | Data Type      | Description                                   |  
|------------------|--------------|-----------------------------------------------|  
| id               | SERIAL       | Primary key, auto-increments with each entry  |  
| make             | VARCHAR(100) | Brand of the car                              |  
| model            | VARCHAR(100) | Model of the car                              |  
| price            | NUMERIC      | Sale price of the car                         |  
| mileage          | NUMERIC      | Total miles driven by the car                 |  
| fuel_type        | VARCHAR(50)  | Type of fuel used (e.g., Diesel, Petrol)      |  
| body_style       | VARCHAR(100) | Style of the car body (e.g., Sedan, SUV)      |  
| engine_size      | NUMERIC      | Engine size (e.g., 2.0)                       |  
| hp               | INT          | Horsepower of the car                         |  
| transmission     | VARCHAR(50)  | Type of transmission (e.g., Manual, Automatic) |  
| year             | INT          | Year of manufacture                           |  
| dealership_name  | VARCHAR(255) | Name of the dealership selling the car        |  
| mpg              | NUMERIC      | Miles per gallon                              |  
| n_doors          | INT          | Number of doors                               |  
| previous_owners  | INT          | Number of previous owners                     |  
| droplet          | VARCHAR(50)  | Colour of the car                             |  
| feature_list     | TEXT         | List of additional features                   |  
| last_updated     | TIMESTAMP    | Timestamp of the last update to the record    |  

### **Handling Missing Values**  

Missing values are retained in the current implementation, as they are automatically excluded when relevant filters are applied. Future updates may introduce imputation techniques to fill these gaps and create a more complete dataset.

### **Database Interaction with Psycopg2**  

The **psycopg2** library is used to execute SQL-like queries directly from Python. When calculating the average price of cars, queries consider only listings within one standard deviation of the user-inputted value for each numeric attribute. For textual attributes, matches must be exact.

---

## Average Price Generation
Calculation Methodology
- Only listings that meet these specified criteria are included in the calculations of the average price. Both the standard deviation and average price functions in psycopg2 inherently exclude rows with missing values in the relevant columns, ensuring that our statistics are computed based on complete and relevant data only.

---

## User Interface
**Use Case**: Comprehensive Feature Input 
- Users can specify all car features, whether they're aiming to buy and want to estimate a fair market price, or they're planning to sell and need to determine a competitive asking price based on detailed vehicle specifications
  - Screenshot: Displays a complete feature input (price excluded) for a comprehensive overview
![image](https://github.com/user-attachments/assets/05c7da5a-fe58-4bc8-a1fe-d5d007a20b56)

Use Case: Partial Feature Input 
- Ideal for users who may not have complete details about a car they wish to buy or sell, our tool allows for flexible input, providing estimates even with incomplete feature sets.
  - Screenshot: Shows an example with partial feature input to demonstrate functionality with incomplete data
![image](https://github.com/user-attachments/assets/179977e5-95f9-418c-ad97-4316e226cc15)

---

## Running the code

- **Installation**
  -To install the required packages, run the following command:
```bash
pip install -r requirements.txt
```

If you prefer to list the commands directly in the README without using a `requirements.txt` file, you can format it like this:

Install the required packages by running:
```bash
pip install scrapy==2.5.0 scrapy-splash==0.7.2 twisted==21.7.0 selenium==4.27.1 webdriver-manager==4.0.2 psycopg2==2.9.10
```

- **Initialise Scrapy-Splash (Note: You need to install docker)**
```bash
docker run -d -p 8050:8050 scrapinghub/splash
docker run -d -p 8052:8050 scrapinghub/splash
```

- **Crawl the Spiders**
```bash
scrapy crawl lookers
scrapy crawl carwow
scrapy crawl cargiant
```
- **Run the Application**
1) Using the Command Line:
  - Open your command prompt or terminal.
  - Navigate to the project directory.
  - Execute the following command, replacing the placeholders with your actual paths:
```bash
& <path_to_python>/python.exe "<path_to_repository>/Used-Cars-Scraper/scrapy_used_cars/GUI.py"
```
2) Using an IDE:
  - Open the project in your preferred Integrated Development Environment (IDE) like PyCharm, VSCode, or any other that supports Python development.
  - Navigate to GUI.py in the project file explorer.
  - Use the Run button typically found in the toolbar or right-click the file and select Run 'GUI.py' to execute the script.

---

## Future Improvements

**Web Scraping**
- Add more sources like AutoTrader and improve anti-bot techniques.
- Implement CAPTCHA handling and proxy rotation for dynamic scraping.

**ETL Processes**
- Automate handling of missing data and clean up inconsistent records.
- Implement daily scheduled scraping to ensure data freshness.

**Machine Learning and Analytics**
- Analyze multi-year trends for pricing and popular models.
- Develop an ML model that handles missing values and calculates average prices.

**User Interface Enhancements**
- Upgrade to a modern web application using Flask or React.
- Add intelligent filtering based on user preferences.

**Natural Language Processing**
- Analyze seller descriptions for tone, sentiment, and key details.

**Advanced Features**
- Predict car depreciation based on age, original price, current price, and number of owners.
- Group average price calculations by location to reflect regional price variations.
- Add a tool to estimate insurance costs based on the car's average price and user age.
- Assess the impact of different car features on price through a linear model after handling missing data.

**System Enhancements**
- Scale up the web scraping using Scrapy Cloud or Scrapyd
- Enhance scraper runtime by loading multiple pages simultaneously with VPN.

---

## Team and Contact

- **Marij Qureshi**: MEng Aeronautical Engineering (Imperial), MSc Data Science (Brunel), ex-EY Parthenon
- **Georgios Gkakos**: MSc Data Science (Brunel), BSc Economics (AUTH)
- **Het Suhagiya**: MSc Data Science (Brunel), BSc Information Technology 

For questions, feel free to reach out via GitHub issues or email any of us.

---

## License
This project is licensed under the MIT License. See the [LICENSE](License) file for more details.

---
