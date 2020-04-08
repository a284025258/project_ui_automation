#!/usr/bin/env sh
# 加载虚拟环境
BASE_DIR=$(dirname "$PWD")

[ -n "${1}" ] || runcase="all" && echo "no input param set \$1 as all"




# 路径设置
APITESTCASE_HOME="${BASE_DIR}/APITest/testcase"
UITESTCASE_HOME="${BASE_DIR}/UITest/testcase"
REPORT_XML_DIR="${BASE_DIR}/report/xml/"
REPORT_HTML_DIR="${BASE_DIR}/report/html/"



    # 判断执行的范围
case ${runcase} in
"all")
  TESTCASE_HOME="${APITESTCASE_HOME} ${UITESTCASE_HOME}"
  ;;
"ui")
  TESTCASE_HOME=${UITESTCASE_HOME}
  ;;
"api")
  TESTCASE_HOME=${APITESTCASE_HOME}
  ;;
*)
  echo "pleace input all or api or ui"
  exit 1
esac



# 选项设置
PYTEST_OPTION="${TESTCASE_HOME} --color=no --alluredir=${REPORT_XML_DIR} -rerun=2"
ALLURE_OPTION="generate --clean ${REPORT_XML_DIR} -o ${REPORT_HTML_DIR}"


# 运行提示
echo $PATH

echo "TESTCASE_HOME ${TESTCASE_HOME}"

pytest ${PYTEST_OPTION}
allure ${ALLURE_OPTION}
echo "finish"

