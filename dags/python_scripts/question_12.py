def get_question_12():

    import pandas as pd
    import requests
    import json

    url = "http://elastic:elastic@localhost:9200/covid/_search"

    payload = json.dumps({
      "query": {
        "match_all": {}
      },
      "_source": [
        "tweet_id",
        "country",
        "date"
      ]
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    df = pd.DataFrame(columns=['tweet_id', 'country', 'date'])

    for row in response.json()['hits']['hits']:
        data = row['_source']
        df.loc[len(df.index)] = [data['tweet_id'][1:], data['country'], data['date']]


    def mask(num):
        return (len(num)-4)*'x' + str(num)[-4:]


    df.loc[:, 'tweet_id'] = df['tweet_id'].apply(mask)

    print(df.head())



get_question_12()