# 测试自动化项目TestAZ

## 项目背景

## 项目结构说明

- APITest 接口测试文件夹
  - APITest\base
    - APITest\base\authentication  鉴权实现
    - APITest\base\caseGenerator 用例生成
    - APITest\base\interface 接口抽象
    - PrepareTestData.py 用例数据准备
    - TestCase.py 用例
  - APITest\util
    - AESUtil.py AES加解密工具类
    - dictUtil.py python字典工具，用于对比两个字典的区别
    - get_session.py 获取数据库连接
  - config.py 接口部分的配置文件
  - congtest.py pytest存放feature的文件
  - module.py 数据库模型
  - testcase.py pytest执行接口测试用例的入口文件
- common
  - exception.py 存放部分异常
  - send_mail.py 发送测试报告
- data 存放测试数据，主要是har文件用于转换
- report 存放测试报告
- static 存放静态文件 allure工具
- UITest 界面测试文件夹
  - controls 存放界面控件
  - pages 存放page对象
  - testcase 存放测试用例
  - utils 存放工具类
  - config.py 界面部分配置文件
  - conftest.py pytest存放feature的位置
- config.py 全局配置文件
- db.sqlite3 sqlite数据库用于便携版的api测试
- manage.py 全局启动文件
- requirements.txt 项目依赖文件

## 快速启动

```shell script
pip install -r requirements.txt
python manage.py s
```