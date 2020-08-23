# city-council-instagram-scraper

A simple Python script to scrape a list of Instagram accounts and see if they contain certain keywords, hashtags, or tagged users.

Requires [Instagram Scraper](https://github.com/arc298/instagram-scraper).

## Usage

* Create a list of names and accounts to be scraped as a TSV file. (See the included file `Helsingin_kaupunginvaltuusto_IG.tsv` which includes the accounts of Helsinki city councillors for reference.)
* Modify the code to include the keywords, hashtags, and/or tagged users you want to look for.
* Comment out the parts of the code which you don’t need.
* Run the code and wait. Scraping 50 to 100 accounts will take about an hour. Be reasonable and don’t try to scrape thousands of accounts at a single go to avoid having your IP address blocked by Instagram.

## Contributing

We are not planning to maintain or further develop this code, but you are free to build on it in your own projects.

## Licence

[Creative Commons Zero 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/)