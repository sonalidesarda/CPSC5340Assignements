import requests
from importlib import reload

"""
This is our only interface with the SOLR service for the amzn-reviews collection
built for the first assignment.

It is simplified as follows
  * We will use only review search and ID (UUID) search
  * And within review search we will filter on score only
"""


##################################


def review_search(kw, start=0, score_facet=None):
    reviews = do_query(review_query_dictionary(kw, start=start, score_facet=score_facet), collection="reviews")
    return reviews


def product_search(asin):
    products = do_query(product_query_dictionary(asin), collection="products")

    if products['response']['numFound'] > 1:
        raise Exception(f"Multiple products found for asin: {asin}")
    elif products['response']['numFound'] == 0:
        return

    return products['response']['docs'][0]


def id_search(id):
    return do_query(id_query_dictionary(id), collection="reviews")


def do_query(params, port="8983", collection="reviews"):
    param_arg = "&".join(list(map(lambda p: f"{p[0]}={p[1]}", list(params.items()))))
    query_string = f"http://localhost:{port}/solr/{collection}/select"
    param_arg += "&facet=true"

    r = requests.get(query_string, param_arg)
    if (r.status_code == 200):
        return r.json()
    else:
        raise Exception(f"Request Error: {r.status_code}")


def id_query_dictionary(id):
    return {"q": f"id:{id}"}


def review_query_dictionary(kw="", start=0, score_facet=None):
    qvalue = "(summary:" + "(" + " OR ".join(kw.split()) + ") OR reviewText:"+ "(" + " OR ".join(kw.split()) + "))"
    if score_facet and score_facet <= 5 and score_facet >= 1:
        qvalue += f" AND overall:{score_facet}"
    return {"q": qvalue, "start": start, "facet.field": "overall", "facet.sort":"index"}


def product_query_dictionary(kw=""):
    return {"q": f"asin:{kw}"}


def build_score_string(s):
    if (len(s) == 0):
        return None
    else:
        dir, val = s.split()
        if (int(val) < 1 or int(val) > 5):
            raise Exception("Bad score value " + s)
        if dir == "<=":
            return f"overall:[0 TO {val}]"
        elif dir == ">=":
            return f"overall:[{val} TO *]"
        else:
            raise Exception("Bad direction value " + s)



