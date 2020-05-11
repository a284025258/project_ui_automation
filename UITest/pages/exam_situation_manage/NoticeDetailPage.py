from UITest.common.po_base import El, Els
from UITest.pages.BasePage import BasePage


class NoticeDetailPage(BasePage):
    back_btn = El("返回按钮", xpath="//span[text()='返回']")
    detail_title = El("详情标题", css=".info-detail-title")
    detail_content = El("详情内容", css=".info-detail-content")
    comment = El("评论", css=".ant-input")
    commit = El("发表评论", xpath="//span[text()='发表']")
    comment_content = Els("评论内容", css=".info-detail-comBox")

    def comment_notice(self, context):
        self.comment.send_keys(context)
        self.commit.click()

    def back(self,page_name):
        if page_name not in ["MyNoticePage","AllNoticePage"]:
            raise ValueError
        self.back_btn.click()
        return self.pm(page_name)(self)
