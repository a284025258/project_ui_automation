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
    sql = """INSERT INTO `api_testcase_data` (module_id,`desc`,`level`, apipath, role_name, `order`, 
    method,req_body,status_code,exp_res_body )
    VALUES
    """
    with open(f"{os.path.join(STATIC_DIR, 'api_path.txt')}", encoding="utf8")as f:
        paths = f.readlines()
    sql_ = r"""('1','校验响应码为200_%s','0','%s','sys_admin','0','post','{"data": {}}','200','{}'),"""
    for path in paths:
        r_sql = sql_ % (path.strip(), path.strip())
        sql += r_sql

    print(sql)


def har_to_case(file, url_spilt=5, data_exclude=False):
    """
    har文件自动生成用例
    """
    import json
    import base64
    import jsonpath

    # 入库sql_base
    sql_base = """
    INSERT INTO `api_testcase_data` (module_id,`desc`,`level`, apipath, role_name, `order`, 
    method,req_body,status_code,exp_res_body )
    VALUES"""

    # todo url分割采用改代码的方式，可能需要自动
    url_spilt = url_spilt
    with open(file, encoding="utf8")as f:
        d_ = json.loads(f.read())
    result = d_["log"]["entries"]

    list_ = []

    for api in result:

        # request
        method = jsonpath.jsonpath(api, "$.request.method")[0]
        url = jsonpath.jsonpath(api, "$.request.url")[0]
        if url_spilt:
            url = "/" + url.split("/", url_spilt).pop()
        has_token = bool(jsonpath.jsonpath(api, "$.request.headers[?(@.name=='Token')]"))
        post_data = jsonpath.jsonpath(api, "$.request.postData.text")[0]
        post_data_encode = jsonpath.jsonpath(api, "$.request.postData.encoding")
        # todo 默认base64解密，这里用的Charles导出的har文件,可能存在其他方式的加密
        if post_data_encode:
            post_data = base64.b64decode(post_data_encode).decode("utf8")

        # 重复性校验：使用url与postdata进行校验
        if (url, post_data) in list_:
            continue
        list_.append((url, post_data))

        # response
        status = jsonpath.jsonpath(api, "$.response.status")[0]
        content = jsonpath.jsonpath(api, "$.response.content.text")[0]
        content_encode = jsonpath.jsonpath(api, "$.response.content.encoding")

        if content_encode:
            # 存在加解密需要解析
            content = base64.b64decode(content).decode("utf8")

        if data_exclude:
            # 排除掉data的干扰
            cont = json.loads(content)
            cont.pop("data", None)
            content = json.dumps(cont)

        value_sql = f"('1','{url}_har_排除data_自动生成','0','{url}','{'sys_admin' if has_token else ''}','0','{method}'," \
                    f"'{post_data}','{status}','{content}'),"
        # print(value_sql)
        # break
        sql_base += value_sql

    print(sql_base[:-1])


if __name__ == '__main__':
    # import json
    #
    # l = api_info()
    # for i in range(len(api_info())):
    #     s = json.dumps(l[i], ensure_ascii=False)
    #     print(s)
    #     break

    # api_scan_data()

    har_to_case(r"E:\PROJECT\testaz\static\exsem_api.har", 4,True)
