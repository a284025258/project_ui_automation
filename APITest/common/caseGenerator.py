"""
根据swaggerApi.json文件生成对应py文件的脚本
可能用不到
"""
import json
import os
import time

from config import BASE_DIR


def ApiInfo():
    with open(r"E:\PROJECT\TestAZ\static\apiInfo\swaggerApi.json", encoding="utf8") as f:
        swagger = json.loads(f.read())

    apiObj = swagger["paths"]

    valList = []
    for path, values in apiObj.items():
        valDict = {"apiPath": path}
        for method, _value in values.items():
            if _value['summary'].find("废弃") >= 0:
                continue

            valDict['method'] = method
            valDict['tags'] = _value['tags'][0]
            valDict['summary'] = _value['summary']

            valDict['parameters'] = _value['parameters']
            valDict['responses'] = _value['responses']
            valList.append(valDict)
    return valList


def genFile(_dict):
    """
    生成测试文件
    :param _dict:
    :return:
    """
    fileName = "test" + _dict['apiPath'].replace("/", "_") + ".py"
    fileTemplate = open(r"E:\PROJECT\TestAZ\static\tempate.txt", encoding="utf8").read()

    s = fileTemplate.format(
        time=time.strftime("%Y/%m/%d %H:%M:%S"), tags=_dict["tags"], summary=_dict['summary'],
        apiPath=_dict['apiPath'], method=_dict['method'], parameters=_dict['parameters'],
        responses=_dict['responses']['200'], apiPathR=_dict['apiPath'].replace("/", "_")
    )
    filePath = os.path.join(BASE_DIR, "APITest/testcase/autoGen", fileName)
    with open(filePath, 'w', encoding="utf8") as f:
        f.write(s)


if __name__ == '__main__':
    for info in ApiInfo():
        genFile(info)
