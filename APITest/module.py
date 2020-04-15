# coding: utf-8
from sqlalchemy import Column, String, Text, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class ApiTestCaseData(Base):
    __tablename__ = 'api_testcase_data'

    id = Column(INTEGER(11), primary_key=True)
    module_id = Column(INTEGER(11), index=True, server_default=text("'0'"), comment='模块id')
    desc = Column(String(255), server_default=text("''"), comment='用例描述')
    level = Column(String(255), server_default=text("''"), comment='用例等级')
    apipath = Column(String(255), server_default=text("''"), comment='接口地址')
    order = Column(INTEGER(11), server_default=text("'0'"), comment='用例执行顺序，越高越先执行')
    method = Column(String(255), server_default=text("'post'"), comment='请求方法')
    req_headers = Column(String(255), server_default=text("''"), comment='请求头，以json格式添加，例如{"token":${token}}')
    req_body = Column(Text, comment='请求头，以json格式添加，例如{"data":{}}')
    status_code = Column(INTEGER(3), server_default=text("'200'"), comment='响应码')
    exp_res_body = Column(Text, comment='期望响应体，以json添加')
    last_excute_body = Column(Text, comment='上一次成功执行的返回值')

    def __str__(self):
        return "<{}: apipath={}, desc={}>".format(self.__class__.__name__, self.apipath, self.desc)

    __repr__ = __str__


class Module(Base):
    __tablename__ = 'module'

    id = Column(INTEGER(11), primary_key=True)
    product_id = Column(INTEGER(11), comment='项目名')
    appid = Column(String(255), server_default=text("''"), comment='模块名')
    module_path = Column(String(255), server_default=text("''"))

    def __str__(self):
        return "<{}: module={}, module_path={}>".format(self.__class__.__name__, self.module, self.module_path)

    __repr__ = __str__


class Param(Base):
    """
    参数表，用于替换接口数据中${param}的值,因为是替换为json,所以需要在表中数据构造时,进行限制,
    对string数据需要增加"",如"data"
    对bool数据需要转换为json,如true,false
    对None数据需要转化为json,如null
    """
    __tablename__ = 'param'

    id = Column(INTEGER(11), primary_key=True)
    key = Column(String(255), nullable=False, unique=True)
    value = Column(String(255))
    desc = Column(String(255))

    def __str__(self):
        return "<{}: key={}, value={}>".format(self.__class__.__name__, self.key, self.value)

    __repr__ = __str__


class Product(Base):
    __tablename__ = 'product'

    id = Column(INTEGER(11), primary_key=True)
    product_name = Column(String(255), server_default=text("''"))
    appid = Column(String(11), server_default=text("''"))
    host = Column(String(255), server_default=text("''"))

    def __str__(self):
        return "<{}: product_name={}, value={}, host={}>".format(self.__class__.__name__,
                                                                 self.product_name, self.appid, self.host)

    __repr__ = __str__
