import requests

MAG_API_KEY = "c6c5efdaac704c90b6c3f151d1e7dd8a"


def query(topic_1, topic_2):
    url = "https://api.labs.cognitive.microsoft.com/academic/v1.0/evaluate?expr=And(Composite(F.FN='{}'),Composite(" \
          "F.FN='{}'))&count=50000&attributes=F.FId,F.FN,Id,Y,AA.AuN".format(
        topic_1, topic_2)

    headers = {"Ocp-Apim-Subscription-Key": MAG_API_KEY}

    payload = {}

    response = requests.request("GET", url=url, headers=headers, data=payload)

    data = response.json()

    return data
