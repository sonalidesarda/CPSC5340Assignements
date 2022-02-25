import os
from flask import Flask
from flask import render_template
import reviewsite.solrinterface as solr
from flask import request
from reviewsite.forms import ReviewSearchForm
from flask import redirect
from flask import *


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    ###################################
    ## Application code begins
    @app.route('/', methods=['GET'])
    def index():
        review_count = solr.do_query({"q": "*:*", "rows": 0}, collection="reviews").get("response", dict()).get(
            "numFound", -1)
        product_count = solr.do_query({"q": "*:*", "rows": 0}, collection="products").get("response", dict()).get(
            "numFound", -1)
        return render_template('index.html', reviewcount=review_count, productcount=product_count)

    @app.route('/hello/<inputName>', methods=['GET'])
    def hello(inputName):
        return render_template('hello.html', tname=inputName)

    @app.route('/search', methods=['GET', 'POST'])
    def searchForm():
        form = ReviewSearchForm()
        if request.method == 'GET':
            return render_template('reviewsearch.html', form=form)
        elif not form.validate():
            return render_template('reviewsearch.html', form=form)
        else:
            return redirect(url_for('searchResults', k=form.keywords.data, page_number=0))

    @app.route('/searchresults', methods=['GET'])
    def searchResults():
        k = request.args.get('k')
        page_number = request.args.get('page_number', type=int)
        score_facet = request.args.get('score', type=int)
        rows_per_page = 10
        start = page_number * rows_per_page
        reviews = solr.review_search(k, start, score_facet)

        review_search_result = list()
        end = None
        next_url = None
        prev_url = None
        if reviews['response']['numFound'] == 0:
            review_search_result = None
            count = 0
        else:
            # Search Product for given review.
            for review in reviews['response']['docs']:
                product = solr.product_search(review['asin'])
                review_search_entry = dict()
                review_search_entry['reviewSummary'] = review['summary']
                review_search_entry['productName'] = product['title'] if product else "PRODUCT_NOT_FOUND"
                review_search_entry['asin'] = review['asin']
                review_search_entry['reviewScore'] = review['overall']
                review_search_entry['id'] = review['id']

                review_search_result.append(review_search_entry)


            if not score_facet:
                score_facet = None
            next_url = url_for('searchResults', k=k, page_number=page_number + 1, score=score_facet) if reviews['response'][
                                                                                                            'numFound'] > (
                                                                                                                    start + rows_per_page) else None
            prev_url = url_for('searchResults', k=k, page_number=page_number - 1, score=score_facet) if 0 <= (
                        page_number - 1) else None
            count=reviews['response']['numFound']
            end = count if count < ((page_number * rows_per_page)+rows_per_page) else (page_number * rows_per_page)+rows_per_page

        return render_template('searchresults.html', res=review_search_result, start=(page_number*rows_per_page)+1, end = end, \
                               count=count, facet=reviews['facet_counts'], keywords=k,
                               next_url=next_url, prev_url=prev_url)

    @app.route('/idlookup/<reviewid>', methods=['GET'])
    def idLookup(reviewid):
        # idDetail = solr.test_id_search('2c7cf845-cb08-4afe-bbba-2f46b467e99c')
        idDetail = solr.id_search(reviewid)
        doc = idDetail['response']['docs'][0]
        print("doc :: ", doc)
        id = doc['id']
        product = solr.product_search(idDetail['response']['docs'][0]['asin'])
        doc['productName'] = product['title'] if product else "PRODUCT_NOT_FOUND"
        return render_template('reviewdetail.html', id=id, doc=doc)

    @app.route('/asinlookup/<asin>', methods=['GET'])
    def asinLookup(asin):
        product = solr.product_search(asin)
        print("product :: ", product)
        return render_template("productdetail.html", asin=asin, product=product)

    ## Application code ends
    ##############################
    return app
