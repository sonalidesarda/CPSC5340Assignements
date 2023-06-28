Assignment 1 -- Page Scrape to SOLR


For this assignment, I worked with Amazon product reviews. We had already downloaded approximately 500 product detail pages for movies, which were stored in the pages directory.

In this assignment, I did the following:

Parsed the HTML pages to extract the attributes of interest about the product and reviews (each review was considered as a document).
Created a SOLR collection to store the documents.
Indexed the documents in the SOLR collection.
Developed a Python interface to allow end users to query the documents and retrieve useful results.
I wrote the code to interact with SOLR in such a way that you could grab my notebook and run the code. It would create the SOLR collection, parse and load the documents, and enable you to run queries against the SOLR collection. Additionally, I provided Python functions for you to supply the set of queries for testing.****
