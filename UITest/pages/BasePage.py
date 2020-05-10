import logging

from UITest.common.page_manage import PageManage
from UITest.common.po_base import Page

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class BasePage(Page):
    """
    页面元素类根类
    """
    m = PageManage
    pass
