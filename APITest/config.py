# 系统配置
SYS_CONF = {
    # appId:{"key":syskey,"host":ip:port}
    "EXWSP": {"key": "85CCQWE456SXXSD6", "host": "http://10.20.5.176:9020"},
    "EXSEM": {"key": "26955CE335EBB4D8", "host": "http://10.20.5.171:9020"},
    "EXEPM": {"key": "2182BF36BD32ACC9", "host": "http://10.20.5.171:9020"},
    "EXSMS": {"key": "DBCCFDC43E99FE4A", "host": "http://10.4.3.131:8020/EXSMS/service"},
}
# 角色配置
ROLE_CONF = {
    # roleName : (account,password,appID)
    "sys_admin": ("45", "12345678", "EXWSP")
}
