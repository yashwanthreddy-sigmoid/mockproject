from flask import Flask,jsonify,json
from elasticsearch import Elasticsearch
import itertools
import pandas as pd
from elasticsearch import helpers
from operator import itemgetter
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import pycountry




app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

@app.route('/Q1',methods=['GET'])
def get_question_1():
    import requests
    import json

    url = "http://elastic:elastic@localhost:9200/covid/_search"
    payload = json.dumps({
        "query": {
        "range": {
            "date": {
            "gte": "now-3M/M",
            "lte": "now/M"
            }
        }
        },
        "aggregations": {
        "country_wise": {
            "terms": {
            "field": "country.keyword"
            }
        }
        }
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    dict1={}
    for row in response.json()['aggregations']['country_wise']['buckets']:
        print(row['key'], row['doc_count'])
        dict1[row['key']]=row['doc_count']
    return  jsonify(dict1,200)

@app.route('/Q2',methods=['GET'])
def get_question_2():
    url = "http://elastic:elastic@localhost:9200/_sql"

    payload = json.dumps({
    "query": "SELECT country,date,COUNT(tweet_id ) AS Total_tweet  FROM covid GROUP BY date,country ORDER BY Total_tweet DESC  "
    })
    headers = {
    'format': 'text',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response = response.json()


    return jsonify(response['rows'],200)



@app.route('/Q3',methods=['GET'])
def get_question_3():

    # Create the client instance
    client = Elasticsearch("http://elastic:elastic@localhost:9200")

    # Successful response!
    print(client.info())

    all_stopwords = ["rt", "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

    n = client.count(index='covid')['count']
    print(n)
    res = client.search(index="covid", body={"query": {"match_all": {}}, "from": 0, "size": n})
    dictionary = {}
    for doc in res['hits']['hits']:
        try:
            if doc["_source"]["message"]:
                # print(doc["_id"], doc["_source"]["new_text"])
                list = doc["_source"]["new_text"].split()
                # print(list)
                for i in list:
                    i.encode(encoding='UTF-8', errors='strict')
                    i = i.lower()
                    i = i.translate({ord('\\'): None})
                    i = i.translate({ord('\"'): None})


                    if i.isnumeric():
                        continue
                    if i not in all_stopwords:
                        if i in dictionary:
                            dictionary[i] += 1
                        else:
                            dictionary.update({i: 1})
        except:
            continue


    dict1 = {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse=True)}

    res = dict(sorted(dict1.items(), key=itemgetter(1), reverse=True)[:100])
    return jsonify(res,200)

@app.route('/Q4',methods=['GET'])
def get_question_4():
    # Create the client instance
    client = Elasticsearch("http://elastic:elastic@localhost:9200")

    print(client.info())
    n = client.count(index='covid')['count']
    print(n)
    res = client.search(index="covid", body={"query": {"match_all": {}}, "from": 0, "size": n})

    all_stopwords = ["rt","didn","take","us","get","got","knew","know","like", "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

    s = {}
    # print(res)

    for doc in res['hits']['hits']:
        try:
            #print(doc["_source"]["country"])
            if doc["_source"]["country"] in s:
                #print(doc["_id"], doc["_source"]["new_text"])
                country = doc["_source"]["country"].lower()
                s[country].append(doc["_source"]["new_text"])
                s[country] = s[country]+" "
            else:
                country = doc["_source"]["country"].lower()
                #print(country)
                s.update({country:doc["_source"]["new_text"]})
                s[country] = s[country]+" "
        except:
            continue

    print(s)

    d ={}
    for k,v in s.items():
        words = v.split()
        dictionary ={}
        for i in words:
            i = i.lower()
            if i not in all_stopwords:
                if i in dictionary:
                    dictionary[i] += 1
                else:
                    dictionary.update({i: 1})

        # print(dictionary)

        dict1 = {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse=True)}

        x = itertools.islice(dict1.items(), 0, 10)
        d.update({k:tuple(x)})


    return jsonify(d, 200)

@app.route('/Q5',methods=['GET'])
def get_question_5():
    def findcountry(text):
        for country in pycountry.countries:
            if country.alpha_2 in text or country.alpha_3 in text or country.name in text:
                # print("inside findcountry: ", text, "returning: ", country.name)
                return country.name
    #es_client = Elasticsearch(hosts=['localhost'], port=9200)

    response_API = requests.get('http://covidsurvey.mit.edu:5000/query?country=all&signal=measures_taken')

    print(type(response_API))
    print(response_API.status_code)
    data = response_API.text


    parse_jason=json.loads(data)

    new_doc={}

    print(parse_jason['AE']['measures_taken']['avoid_sick'])

    for i in parse_jason:

        case={i:parse_jason[i]['measures_taken']}

        new_doc.update(case)




    case4=[]
    case5={}
    for i in new_doc:

        for j in new_doc[i]:

            case2={j:new_doc[i][j]['weighted']['Yes']}

            case5.update(case2)


        case3 = {i: case5}


        for k, v in case3.items():
            country=findcountry(k)
            dict1={}
            dict1[country]=sorted(v.items(), key=lambda item: item[1],reverse=True)
            case4.append(dict1)


    return  jsonify(case4,200)

@app.route('/Q6',methods=['GET'])
def get_question_6():
    es_client = Elasticsearch(hosts=['localhost'], port=9200, http_auth=("elastic", "elastic"))

    response_API = requests.get('https://covidfunding.eiu.com/api/funds')
    # print(type(response_API))
    # print(response_API.status_code)
    data = response_API.text
    doc_list = []
    try:
        parse_json = json.loads(data)
        doc_list = parse_json["funds"]
        print(doc_list)

        resp = helpers.bulk(
            es_client,
            doc_list,
            index="donation_towards_covid19",
            doc_type="_doc"
        )


    except ValueError as error:
        print("Error type:", type(error))
        print("json.loads() ValueError for JSON object:", error)

    url = "http://elastic:elastic@localhost:9200/_sql"

    payload = json.dumps({
    "query": "SELECT targetGeographicalLocation,SUM(amount) as  total_donation_received FROM donation_towards_covid19 GROUP BY targetGeographicalLocation ORDER BY total_donation_received DESC"
    })
    headers = {
    'format': 'text',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    response = response.json()

    return jsonify(response["rows"], 200)


@app.route('/Q7',methods=['GET'])
def get_question_7():
    es_client = Elasticsearch(hosts=['localhost'], port=9200, http_auth=("elastic", "elastic"))

    response_API = requests.get('https://disease.sh/v3/covid-19/historical')
    print(type(response_API))
    print(response_API.status_code)
    data = response_API.text

    try:
        parse_json = json.loads(data)
        doc_list = []
        index = 0
        for row in parse_json:
            for date in row['timeline']['cases']:
                print(row['country'], date, row['timeline']['cases'][date], row['timeline']['deaths'][date])

                doc = {
                    "_id": index,
                    "country": row['country'],
                    "date": datetime.strptime(date, '%m/%d/%y'),
                    "cases": row['timeline']['cases'][date],
                    "deaths": row['timeline']['deaths'][date],
                    "week_no": datetime.date(datetime.strptime(date, '%m/%d/%y')).isocalendar()[1]
                }
                # print(type(datetime.date(datetime.strptime(date, '%m/%d/%y')).isocalendar()[1]))

                doc_list.append(doc)
                index += 1

        resp = helpers.bulk(
            es_client,
            doc_list,
            index="cases_deaths",
            doc_type="_doc"
        )

    except ValueError as error:
        print("Error type:", type(error))
        print("json.loads() ValueError for JSON object:", error)
    url = "http://elastic:elastic@localhost:9200/_sql"

    payload = json.dumps({
        "query": "SELECT country,week_no,SUM(cases) AS total_cases_week_wise_country_wise FROM cases_deaths GROUP BY country,week_no ORDER BY total_cases_week_wise_country_wise DESC"
    })
    headers = {
        'format': 'text',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response = response.json()

    #print(type(response["rows"]))


    return jsonify(response["rows"], 200)



@app.route('/Q8',methods=['GET'])

def get_question_8():

 

    # [50418 rows x 10 columns]
    df = pd.read_csv("/Users/somalayashwanthreddy/Downloads/tweet_airflow 2/files/global_economy.csv", usecols=[0, 1, 2, 7])
    # df1 = df[df.isna().any(axis=1)] # 5712 rows having NaN, mostly in gdp column

    df.dropna(inplace=True)
    df.reset_index(inplace=True)

    #print(df.head())
    #print(len(df))

    fields = ['index', 'iso_code', 'location', 'date', 'gdp_per_capita']
    def filterKeys(document):
        return {key: document[key] for key in fields}

    es_client = Elasticsearch(hosts=['localhost'], port=9200, http_auth=("elastic", "elastic"))

    def doc_generator(df):
        df_iter = df.iterrows()
        for index, document in df_iter:
            yield {
                    "_index": 'economy',
                    "_type": "_doc",
                    "_id": f"{document['index']}",
                    "_source": filterKeys(document),
                }
        # raise StopIteration

    helpers.bulk(es_client, doc_generator(df))

    url = "http://elastic:elastic@localhost:9200/_sql"

    payload = json.dumps({
        "query": "SELECT location,gdp_per_capita as GDP FROM economy  GROUP BY location,gdp_per_capita order by GDP DESC LIMIT 1000 "
    })
    headers = {
        'format': 'text',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response=response.json()


    return jsonify(response["rows"],200)


@app.route('/Q10',methods=['GET'])
def get_question_10():
    html_data = open('/Users/somalayashwanthreddy/Downloads/tweet_airflow 2/files/question10data.html', 'r')
    html_content = html_data.read()
    soup = BeautifulSoup(html_content, "html.parser")
    data = soup.find_all('ol')
    data = data[1].next_sibling
    data = data.findAll('tr')
    data = data[3:]
    age_category = []
    for row in data:

        curr_data = row.find_all('td')
        country = curr_data[0].text
        age_0_to_44 = curr_data[3].text
        age_45_to_54 = curr_data[4].text
        age_55_to_64 = curr_data[5].text
        age_65_to_74 = curr_data[6].text
        age_75_to_84 = curr_data[7].text
        age_above_85 = curr_data[8].text
        curr_dict = {'country': country, 'death % by age-group': [{'age_0_to_44': age_0_to_44,
                                                                   'age_45_to_54': age_45_to_54,
                                                                   'age_55_to_64': age_55_to_64,
                                                                   'age_65_to_74': age_65_to_74,
                                                                   'age_75_to_84': age_75_to_84,
                                                                   'age_above_85': age_above_85}]}
        age_category.append(curr_dict)
    results = {'age_categorisation_data': age_category}

    return jsonify(results,200)



#get_question_4()
#Running the app
app.run(host='0.0.0.0',port=5008)

