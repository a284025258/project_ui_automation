import logging

from APITest.base.authentication.ABCTokenAuth import ABCTokenAuth
from APITest.base.badconfexc import BadConfException
from APITest.base.interface.JF_CEMS_4_0.authapi import JF_CEMS_4_0AuthABCAPI
from APITest.config import ROLE_CONF

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
        if not self.args[0]:
            return ""
        # 通过配置文件中的role_name读取配置
        role_name = self.args[0]
        try:
            account = ROLE_CONF[role_name][0]
            password = ROLE_CONF[role_name][1]
            appID = ROLE_CONF[role_name][2]
        except (KeyError, IndexError):
            raise BadConfException(f"请检查配置文件中->{role_name}<-是否存在问题")

        token = JF_CEMS_4_0AuthABCAPI(account, password, appID).token
        return token
