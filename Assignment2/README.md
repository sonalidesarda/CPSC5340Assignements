In Assignment 2 -- Page Scrape to SOLR, I had two files, one containing review data and the other containing product data. The format of these files was unusual, with each file having one line per "data row." A data row represented either a single review or a single product, depending on the file.

To convert each line into a Python dictionary, I used the following code:

eval('(' + line + ')')

By iterating over all the lines in the review data file and evaluating each line, I built a list of dictionaries, one per review. This process was similar to scraping the review pages. The same procedure applied to the product pages data file. I utilized the data from these two lists of dictionaries to index my two SOLR collections.

One difference was that when scraping a page, I could select only the attributes relevant to my application. However, when reading these files, they contained additional fields that needed to be removed from the dictionary. This was necessary because those fields were not part of the SOLR schema, and SOLR would raise an error if I included fields not in its schema.

Not all fields were of interest to me for our website. Here is information about the fields' meanings and which ones I kept or discarded:

Reviews Data:

id (UUID): This field was not in the input file and was supplied by SOLR, similar to what I did for Assignment 1.
asin (string): Product ID. It joined with the asin field in the product file.
reviewText (text): Full review body.
overall (integer): Average rating. I truncated the floating-point value.
summary (text): Review summary text.
Unlike the previous assignment, I omitted the review time from our reviews documents.

Products:

asin (string): Unique ID for products. It joined with the asin field in the reviews file.
description (string): Stored but not indexed. It was shown on the product detail page but not searchable.
title (string): The product name. It was stored but not indexed. It appeared on the product detail page, as well as on review search result and detail pages.
price (float): It was displayed in currency format on the product detail page.
For product data, only the ASIN field in products was indexed. This meant that I couldn't perform any searches on products except for an ASIN lookup. In a real e-commerce application, one would typically search for product attributes as well. However, for this assignment, we kept it simple and focused only on searching reviews.

It is important to consider the implications of this decision. For example, if a review search is performed on 'iphone', it will only retrieve reviews that explicitly mention the term 'iphone' in the review summary or the review text, even if the product itself had 'iphone' in the title.

The main deliverables for this assignment were:

A directory containing the configuration for the reviews collection.
A directory containing the configuration for the products collection.
A directory containing my Flask project.
I ensured to name these components exactly as specified:

The directory containing the configuration for the reviews collection was named "reviews."
The name of the SOLR collection was also "reviews."
The directory containing the configuration for the products collection was named "products."
The name of the SOLR collection was also "products."
The name of the directory containing my Flask project was "reviewsite."
This notebook included code to "scrape" the data files and prepare dictionaries for indexing. It is important to note that in this notebook, I only wrote function definitions to prepare the dictionaries, similar to the function "scrapePagesForReviews" written for Assignment 1.

Furthermore, it was crucial to use the exact names
