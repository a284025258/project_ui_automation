import pytest


def test_api_response(ApiData):
    if not ApiData.info["enable"]:
        pytest.skip("未完成的接口")
    ApiData.run()
