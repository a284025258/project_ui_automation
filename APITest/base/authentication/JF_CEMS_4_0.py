import logging

from APITest.base.authentication.ABCTokenAuth import ABCTokenAuth
from APITest.base.interface.JF_EXWSP_4_0 import JF_EXWSP_4_0AuthApi
from APITest.config import ROLE_CONF
from common.exception import BadConfException
JF_EXWSP_4_0AuthApi
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class JF_CEMS_4_0_TokenAuth(ABCTokenAuth):
    """
    综合考务管理系统4.0鉴权实现
    """

    def _get_token(self):
        """
        获取token
        """
        if not self.role_name:
            return ""
        # 通过配置文件中的role_name读取配置
        role_name = self.role_name
        try:
            account = ROLE_CONF[role_name][0]
            password = ROLE_CONF[role_name][1]
            appID = ROLE_CONF[role_name][2]
        except (KeyError, IndexError):
            raise BadConfException(f"请检查配置文件中->{role_name}<-是否存在问题")

        token = JF_EXWSP_4_0AuthApi(account, password, appID).token
        return token