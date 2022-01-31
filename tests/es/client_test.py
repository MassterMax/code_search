import unittest
from pprint import pprint

from codesearch.es.client import ElasticSearchClient


# Для работы надо запустить docker эластика - test_env_up
class ClientTest(unittest.TestCase):
    def setUp(self):
        self.es = ElasticSearchClient()

    def test_create_delete_index(self):
        response = self.es.create("test_index")
        assert 'acknowledged' in response and response['acknowledged'], response

        response = self.es.delete("test_index")
        assert response['status'] == 'ok'


if __name__ == "__main__":
    unittest.main()
