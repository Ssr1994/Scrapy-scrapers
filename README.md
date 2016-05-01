# Scrapy-scrapers

For now, under keywordsearch, change the keyword to search in keywordsearch/settings.py, and use:
  ./getMeData
which fetches webpages (stored under ./webpages) and scrapes data (stored in keywordsearch.db in table 'search');

under yahoofinance, change the ticker to search in yahoofinance/spiders/yfnc.py, use:
  scrapy crawl yfnc
which fetches historical prices from Yahoo! Finance (stored in yahoofinance.db in table 'yahoo')
