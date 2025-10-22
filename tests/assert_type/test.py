from django.test.client import Client
from django.urls import URLPattern, URLResolver, reverse_lazy
from rest_framework import status, test
from rest_framework.response import _MonkeyPatchedResponse
from rest_framework.test import APIClient, APILiveServerTestCase, APISimpleTestCase, APITestCase, APITransactionTestCase
from typing_extensions import assert_type


# case: api_client_returns_proper_responses
class MyTestCase(test.APITestCase):
    client: test.APIClient

    def test_my_code(self) -> None:
        client = test.APIClient()
        assert_type(client.post("http://google.com"), _MonkeyPatchedResponse)

    def test_json_attribute_on_response(self) -> None:
        client = test.APIClient()
        resp = client.get("http://someapi.com/1")
        self.assertTrue(resp.json())


# case: test_testcases_client_api_urlpatterns
class MyTest(test.URLPatternsTestCase):
    urlpatterns: list[URLPattern | URLResolver] = []

    def test_example(self) -> None:
        assert_type(self.client, Client)
        response = self.client.get("/", format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# case: test_testcases_client_api
class MyTest2(test.APITransactionTestCase):
    def test_example(self) -> None:
        assert_type(self.client, APIClient)
        response = self.client.get("/", format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"detail": {"not_found"}})


assert_type(APITransactionTestCase.client, APIClient)
assert_type(APITestCase.client, APIClient)
assert_type(APISimpleTestCase.client, APIClient)
assert_type(APILiveServerTestCase.client, APIClient)


# case: test_requestfactory_http_verbs
url = reverse_lazy("api:example")
request_factory = test.APIRequestFactory()
request_factory.get(url)
request_factory.post(url)
request_factory.put(url)
request_factory.patch(url)
request_factory.delete(url)
request_factory.generic("get", url)


# case: test_apiclient_http_verbs
url = reverse_lazy("api:example")
client = test.APIClient()
client.get(url)
client.post(url)
client.put(url)
client.patch(url)
client.delete(url)
