#!/bin/bash
rm -rf webpages
mkdir webpages

scrapy crawl cnn &
scrapy crawl foxnews &
scrapy crawl latimes &
scrapy crawl nytimes &
scrapy crawl wapost &
scrapy crawl wsj &