from parsers import RestCountriesParser, EbayParser

if __name__ == "__main__":
    country_scraper = RestCountriesParser()
    country_scraper.scrape_country_info("ukraine")

    ebay_scraper = EbayParser()
    print(ebay_scraper.scrape_item_info("<YOUR ITEM URL FROM EBAY>"))
