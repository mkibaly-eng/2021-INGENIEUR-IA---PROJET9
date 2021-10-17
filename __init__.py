import logging
from pandas.core.indexes import base
import azure.functions as func
import pandas as pd
import random


def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info('Python HTTP trigger executed!')

    userId = req.params.get('userId')
    user_articles = pd.read_csv("./rec_train.csv", sep=",")
    articles = pd.read_csv("./articles.csv", sep=",")
    my_dict = dict() 
    for index, row in user_articles.iterrows():
        my_dict[row.user_id] = row.article_list

    if not userId:
            try:
               req_body = req.get_json()
            except ValueError:
                pass
            else:
                userId = req_body.get('userId')


    if userId:
        list_art = []
        my_dict[userId] = my_dict[userId].replace('[', '').replace(']', '').replace(',', '').split()
        for elt in my_dict[userId]:
            articles_id = articles[articles.category_id == int(elt)]['article_id'].values
            list_art.append(int(random.choice(articles_id)))
        return func.HttpResponse(f"{list_art}")
    else:
        return func.HttpResponse("Please pass a user on the query string or in the request body", status_code=200)
