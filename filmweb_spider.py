import scrapy
import logging
import time
import os
from items import FilmwebItem
from scrapy.spiders import CrawlSpider
from scrapy.utils.log import configure_logging
from scrapy.selector import Selector

try:
    os.remove('filmweb.json, log.txt')
except OSError:
    pass

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='log.txt',
    level=logging.INFO)

class FilmwebSpider(CrawlSpider):
    name = 'filmweb'
    start_urls = ['https://ssl.filmweb.pl/login']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'j_username': 'User', 'j_password': 'pass', '_prm': 'true'},
            callback=self.login
        )

    def login(self, response):

        #SAVE RESPONS TO FILE - FOR DEBUG ONLY !
        # text_file = open("Output.txt", 'w')
        # text_file.write('Response: %s' % response.bod)
        # text_file.close()

        if '/user/NeVrea' in response.body:
            self.logger.info('Login ok!')
            return scrapy.Request(url='http://www.filmweb.pl/user/User/films',
            callback=self.movie_parse)
        else:
            self.logger.info('Login failed!')
            return

    def movie_parse(self, response):
        self.logger.info("After parse ok!: %s" % response.body)
        sel = Selector(response)
        sites = sel.xpath("//div[@class='votesPanel']/div")
        items = []
        root = "//div[@class='votePanel']"
        titleLink = "%s/div[@class='voteFilmTitle']/a" % root

        for site in sites:
            movie = FilmwebItem()
            movie['last_updated'] = time.strftime("%Y-%m-%d %H:%M")
            movie['title'] = site.xpath("%s/text()" % titleLink).extract()
            movie['link'] = site.xpath("%s/@href" % titleLink).extract()
            movie['rate'] = site.xpath("""%s/div[@class='votingPanel']
            /div[@class='rateText']/span/text()""" % root).extract()
            items.append(movie)
        return items
