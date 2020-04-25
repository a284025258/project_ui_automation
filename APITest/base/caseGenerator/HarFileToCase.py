"""
har文件转case
"""
import base64
import json
import logging

from jsonpath import jsonpath

from APITest.util.get_session import get_session
from APITest.config import SYS_CONF
from APITest.module import ApiTestCaseData, Product

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Har2Case:
    """
    针对post接口的json发送，解析har文件生成用例
    todo 数据库重复数据处理
    todo restful格式接口处理 eg /path/api/{id}
    todo 重复性校验：使用url与postdata进行校验
    """
    hosts = {SYS_CONF[k]["host"]: k for k in SYS_CONF}  # { host : appid } eg {'http://10.20.5.176:9020': 'EXWSP'}

    def __init__(self, har_file_path):
        """

        @param har_file_path: har文件路径
        """
        self.result = self.load_file(har_file_path)
        self._conn = get_session()
        self.product_info = self._get_product_info()

    def _get_product_info(self):
        """
        返回产品表，{ app_id : id }
        @return:
        """
        res = self._conn.query(Product).all()
        self._conn.close()
        info = {p.appid: p.id for p in res}
        return info

    @staticmethod
    def load_file(har):
        """
        返回文件内容的迭代器
        @param har: har文件
        @return:
        """
        with open(har, encoding="utf8")as f:
            _ = json.loads(f.read())
        version = _["log"]["version"]
        if "1.2" > version or version > "2":
            # todo 其他版本的har文件
            raise ValueError(f"不支持的har版本->{version}")
        result = _["log"]["entries"]
        del _
        return iter(result)

    def parse(self, to_db=False, role_name="sys_admin", exclude_node=None):
        """
        转化har文件
        @param to_db:是否存入数据库
        @param role_name:角色名，用于有权限时，插入数据库的角色名
        @param exclude_node:排除节点，需要排除的response data 的节点
        @return:
        """

        for res in self.result:
            method = res["request"]["method"]
            appid, url = self._parse_url(res["request"]["url"])
            auth = self.check_auth(res["request"]["headers"])
            post_data = res["request"]["postData"]["text"]
            status = res["response"]["status"]
            response_data = self._parse_response_data(res["response"]["content"], exclude_node)
            atc = ApiTestCaseData(module_id="1", desc=f"【har自动生成】->{url}", level="3",
                                  apipath=url, role_name=role_name if auth else "", order="0", method=method,
                                  req_headers="", req_body=post_data, status_code=status,
                                  exp_res_body=response_data, enable="1")
            if to_db:
                self._conn.add(atc)
        if to_db:
            self._conn.commit()

    def _parse_url(self, url):
        """
        url转换为api path 和对应的 项目host
        @param url:
        @return: appid和切割后的url
        """
        api_path = url
        appid = ""

        for host in self.hosts:
            if host in url:
                api_path = url[len(host):]
                appid = self.hosts[host]
                break
        else:
            logger.warning(f">{url}>在配置文件中不存在匹配项.\n当前配置文件为{self.hosts}")

        return appid, api_path

    @staticmethod
    def _parse_response_data(data, exclude_node):
        """
        转换response的字符串，
        @param data:
        @param exclude_node: 需要排除的节点
        @return:
        """
        response = data["text"]
        encrypt = bool(data.get("encoding", ""))
        if encrypt:
            response: str = base64.b64decode(response).decode("utf8")
        if exclude_node:
            _ = json.loads(response)
            _.pop(exclude_node, f"没有可以删除的节点->{exclude_node}")
            response = json.dumps(_)
        return response

    @staticmethod
    def check_auth(data) -> bool:
        """
        判断是否有权限
        @param data:
        @return:
        """
        if isinstance(data, str):
            data = json.loads(data)
        result = jsonpath(data, "$[?(@.name=='Token')].value")

        if not result:
            return False

        return bool(result[0])


if __name__ == '__main__':
    Har2Case(r"E:\PROJECT\testaz\data\har\test.har").parse()
