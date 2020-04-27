import allure
import pytest


@allure.feature("接口测试")
def test_api_response(ApiData):
    if not ApiData.info["enable"]:
        pytest.skip("未完成的接口")
    ApiData.run()
