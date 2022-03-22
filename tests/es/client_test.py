import unittest

from codesearch.es.client import ElasticSearchClient


class ClientTest(unittest.TestCase):
    def setUp(self):
        """
        Set up test environment first - the test class calls elastic
        """
        self.es = ElasticSearchClient()

    def test_create_delete_index(self):
        """
        Create and delete index test
        """
        response = self.es.create("test_index")
        assert 'acknowledged' in response and response['acknowledged'], response

        response = self.es.delete("test_index")
        assert response['status'] == 'ok'


if __name__ == "__main__":
    unittest.main()
