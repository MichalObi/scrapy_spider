import scrapy
class FilmwebItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    rate = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)
