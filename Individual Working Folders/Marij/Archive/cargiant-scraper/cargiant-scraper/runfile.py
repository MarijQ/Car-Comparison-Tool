import os
from scrapy import cmdline

# Ensure we are in the correct directory before running the Scrapy command
target_dir = './Marij/cargiant_scraper'
current_dir = os.getcwd()

if current_dir != os.path.abspath(target_dir):
    os.chdir(target_dir)

# Execute the Scrapy command
cmdline.execute("scrapy crawl cargiant -O cargiant_data.json".split())
