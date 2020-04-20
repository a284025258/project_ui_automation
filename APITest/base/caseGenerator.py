"""
根据swaggerApi.json文件生成对应py文件的脚本
可能用不到
"""
import json


def api_info():
    with open(r"E:\PROJECT\TestAZ\static\apiInfo\swaggerApi.json", encoding="utf8") as f:
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


if __name__ == '__main__':
    for info in api_info():
        print(info["apiPath"])
