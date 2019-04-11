from elasticsearch import Elasticsearch


class ScalerHttpService:
    def __init__(self, url="http://204.209.76.168:9200"):
        self.response_time = 0
        self.es = Elasticsearch([url])

    def get_response_time(self):
        return self.response_time

    def set_response_time(self, response_time):
        self.response_time = response_time

    def update_response_time(self, duration="now-20s"):
        res = self.es.search(index="apm-*transaction-*",
                             body={"query": {"range": {"@timestamp": {"gte": duration}}},
                                   "aggs": {"avg_response_time": {"avg": {"field": "transaction.duration.us"}}}})
        self.response_time = res["aggregations"]["avg_response_time"]["value"]
