# Scrapy settings for carwow_scrape project

BOT_NAME = "carwow_scrape"

OFFSITE_ENABLED = False

SPIDER_MODULES = ["carwow_scrape.spiders"]
NEWSPIDER_MODULE = "carwow_scrape.spiders"

# Splash setup
SPLASH_URL = 'http://localhost:8050'

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
    "carwow_scrape.middlewares.CarwowScrapeSpiderMiddleware": 543,
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,  # Middleware for Splash to handle cookies
    'scrapy_splash.SplashMiddleware': 725,        # Middleware for Splash rendering
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,  # For gzip/deflate compression
    'scrapy_selenium.SeleniumMiddleware': 800,    # Middleware for Selenium integration
    'carwow_scrape.middlewares.CarwowScrapeDownloaderMiddleware': 543,  # Custom middleware (if applicable)
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None, # Disabling default User-Agent middleware
}

# Configure Splash-aware duplicate filtering
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

# Enable Splash-aware cache storage
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# Configure Selenium settings
SELENIUM_DRIVER_NAME = 'chrome'  # Tells Scrapy to use ChromeDriver
SELENIUM_DRIVER_EXECUTABLE_PATH = '/opt/homebrew/bin/chromedriver'  # Path to ChromeDriver, not Chromium
SELENIUM_DRIVER_ARGUMENTS = ['--headless', '--no-sandbox', '--disable-dev-shm-usage']  # Headless mode & other options

# Path to the Chromium browser
SELENIUM_DRIVER_PATH = '/opt/homebrew/bin/chromium'  # Path to the Chromium executable

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "carwow_scrape (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 1

# Set maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Enable or disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Enable or disable spider middlewares
# SPIDER_MIDDLEWARES = {
#    "carwow_scrape.middlewares.CarwowScrapeSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# DOWNLOADER_MIDDLEWARES = {
#    "carwow_scrape.middlewares.CarwowScrapeDownloaderMiddleware": 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

EXTENSIONS = {
    'scrapy.extensions.closespider.CloseSpider': 1,
}

# Configure item pipelines
ITEM_PIPELINES = {
   "carwow_scrape.pipelines.CarwowScrapePipeline": 300,
}

# Output settings
FEED_FORMAT = 'json'  # Output in JSON format
FEED_URI = './output.json'  # File to save the data
FEED_EXPORT_ENCODING = 'utf-8'

# Enable auto-throttle for managing concurrent requests efficiently
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = False

# Enable HTTP caching to prevent unnecessary downloads
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 86400  # Cache data for 24 hours
HTTPCACHE_DIR = "httpcache"
HTTPCACHE_IGNORE_HTTP_CODES = []

# Save data incrementally with batching
FEED_EXPORT_BATCH_ITEM_COUNT = 100  # Save data every 100 items
FEED_STORE_EMPTY = True

# Enable and configure the AutoThrottle extension (disabled by default)
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"