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