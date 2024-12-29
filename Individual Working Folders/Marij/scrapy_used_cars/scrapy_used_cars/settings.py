
BOT_NAME = "scrapy_used_cars"

SPIDER_MODULES = ["scrapy_used_cars.spiders"]
NEWSPIDER_MODULE = "scrapy_used_cars.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

LOG_LEVEL = 'INFO'
CONCURRENT_REQUESTS = 60
DOWNLOAD_DELAY = 0

ITEM_PIPELINES = {
    "scrapy_used_cars.pipelines.CargiantFinalPipeline": 300,
}

import scrapy_splash


# Splash Setup
SPLASH_URLS = ['http://localhost:8050',
    'http://localhost:8051',]

SPLASH_LOG_400 = True

# Enable Splash Deduplicate Args Filter
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
    "scrapy_used_cars.middlewares.CargiantFinalSpiderMiddleware": 543,
}

# Define the Splash DupeFilter
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 20
CONCURRENT_REQUESTS_PER_IP = None

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Splash configuration
SPLASH_SLOT_POLICY = scrapy_splash.SlotPolicy.PER_DOMAIN  # Assign separate slots for each domain
SPLASH_COOKIES_DEBUG = True  # Debug cookies handled by Splash

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
    "User-Agent" :"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "scrapy_used_cars.middlewares.CargiantFinalDownloaderMiddleware": 543,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "scrapy_used_cars.pipelines.CargiantFinalPipeline": 300,
}

# Adjust thread pool size for Scrapy's reactor
REACTOR_THREADPOOL_MAXSIZE = 40  # Increase thread pool size to handle more requests

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
#The initial download delay
AUTOTHROTTLE_START_DELAY = 0.1
#The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 5
#The average number of requests Scrapy should be sending in parallel to
#each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 20
#Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True

# Retry Middleware
RETRY_ENABLED = True
RETRY_HTTP_CODES = [400, 429, 500, 503]
RETRY_TIMES = 3

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
