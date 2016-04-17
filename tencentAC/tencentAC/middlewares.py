from selenium import webdriver
from scrapy.http import HtmlResponse
import time

class PhantomJSMiddleware(object):
    
    def process_request(self, request, spider):
        if request.meta.has_key('phantomjs') and request.meta['phantomjs']:
            driver = webdriver.PhantomJS(executable_path='phantomjs', service_args=['--load-images=no'])
            driver.get(request.url)
            driver.execute_script('var h = document.getElementsByClassName("main_control")[0].offsetTop; var sh = 0; window.setInterval(function(){ if (sh < h) {sh += 700; window.scrollTo(0, sh);} }, 300);')
            time.sleep(8)
            content = driver.page_source.encode('utf-8')
            url = driver.current_url.encode('utf-8')
            driver.close()
            return HtmlResponse(url, encoding='utf-8', status=200, body=content)
        else:
            return None