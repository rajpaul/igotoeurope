from haystack.backends.elasticsearch_backend import ElasticsearchSearchBackend
from haystack.backends.elasticsearch_backend import ElasticsearchSearchEngine

class FuzzyBackend(ElasticsearchSearchBackend):
    DEFAULT_ANALYZER = "whitespace"

    def build_search_kwargs(self, query_string, **kwargs):
        if query_string == '*:*':
            kwargs = {
                'query': {
                    "match_all": {}
                },
            }
        else:
            kwargs = {
                'query': {
                    'fuzzy_like_this': {
                        'like_text': query_string,
                        'prefix_length': 1
                    },
                }
            }
        return kwargs


class ConfigurableElasticSearchEngine(ElasticsearchSearchEngine):
    backend = FuzzyBackend
