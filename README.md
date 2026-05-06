# panelapp_scraping_work
Scraping data for panel genes not recoverable via PanelApp's API

```
Rscript panelapp_API.R #returns list of genes with tiers of evidence in separate column
```

Certain genes could not be found via the API so I wrote a separate webscraper for such genes to be incorporated into the output from the Rscript:

```
python get_pannel_app_pannels.py scraped_panelapp_data.tsv
```
