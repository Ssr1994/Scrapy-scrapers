from selenium import webdriver
from scrapy.http import HtmlResponse
import time

class PhantomJSMiddleware(object):
    
    def process_request(self, request, spider):
        if request.meta.has_key('phantomjs') and request.meta['phantomjs']:
            driver = webdriver.PhantomJS(executable_path='phantomjs', service_args=['--load-images=no'])
            driver.get(request.url)
            if request.meta.has_key('target'):
                if request.meta['target'] == 'wapost':
                    driver.find_element_by_css_selector('div.pb-loadMore').click()
            time.sleep(3)
            content = driver.page_source.encode('utf-8')
            url = driver.current_url.encode('utf-8')
            driver.close()
            return HtmlResponse(url, encoding='utf-8', status=200, body=content)
        else:
            return None