# Scrapy settings for cargiant_scraper_3 project

BOT_NAME = "cargiant_scraper_3"

SPIDER_MODULES = ["cargiant-scraper-3.spiders"]
NEWSPIDER_MODULE = "cargiant-scraper-3.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    'cargiant-scraper-3.middlewares.SeleniumMiddleware': 543,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

# Enable and configure HTTP caching (disabled by default)
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

LOG_LEVEL = 'INFO'  # Set this to 'ERROR' if you only want to see errors.
