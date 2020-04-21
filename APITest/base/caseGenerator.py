"""
根据swaggerApi.json文件生成对应py文件的脚本
可能用不到
"""
import json
import os

from config import STATIC_DIR


def api_info():
    with open(r"E:\PROJECT\TestAZ\static\swaggerApi.json", encoding="utf8") as f:
        swagger = json.loads(f.read())

    apiObj = swagger["paths"]

    valList = []
    for path, values in apiObj.items():
        valDict = {"apiPath": path}
        for method, _value in values.items():
            if _value['summary'].find("废") >= 0:
                continue

            valDict['method'] = method
            valDict['tags'] = _value['tags'][0]
            valDict['summary'] = _value['summary']

            valDict['parameters'] = _value['parameters']
            valDict['responses'] = _value['responses']
            valList.append(valDict)
    return valList


def api_scan_data():
    sql = """INSERT INTO `api_testcase_data` (
        module_id,
        `desc`,
        `level`,
        apipath,
        role_name,
        `order`,
        method,
        req_body,
        status_code,
        exp_res_body
    )
    VALUES
    """
    with open(f"{os.path.join(STATIC_DIR, 'api_path.txt')}",encoding="utf8")as f:
        paths = f.readlines()
    sql_ = r"""('1','api快速扫描%s','0','%s','sys_admin','0','post','{"data": {}}','200','{"code": 200,"message":"OK"}'),"""
    for path in paths:
        r_sql = sql_ % (path.strip(), path.strip())
        sql += r_sql

    print(sql)


if __name__ == '__main__':
    # for info in api_info():
    #     print(info["apiPath"])
    api_scan_data()