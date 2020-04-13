import logging

import pytest

from APITest.common.PrepareTestData import PrepareTestData
from runApiTest import RUN_MODULE, RUN_LEVEL, RUN_PATH

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)




ptd = PrepareTestData(RUN_MODULE, RUN_LEVEL, RUN_PATH)


@pytest.fixture(params=ptd.get_data(), ids=ptd.get_case_desc())
def ApiData(request):
    return request.param





def test_api(ApiData):
    assert ApiData.run()








