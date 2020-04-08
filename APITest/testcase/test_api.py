import allure
import requests

from APITest.util.dictUitl import assert_dict_contain


def test_api(ApiData):


    response=requests.request(ApiData["method"],ApiData["url"],json=ApiData["json"])
    assert assert_dict_contain(ApiData["expect"],response.json())


