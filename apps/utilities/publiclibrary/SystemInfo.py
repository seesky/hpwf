# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/26 14:09'

class SystemInfo(object):
    ServiceUserName = 'HPWFFramework'
    ServicePassword = 'HPWFFramework123456'
    CurrentLanguage = 'zh-CN'
    Themes = ''

    #是否更新访问日期信息
    UpdateVisit = True

    #检查周期[以秒为单位]2分钟内不在线的，就认为是已经没在线了，心跳方式检查
    OnLineTime0ut = 2 * 60 + 20

    #同时在线用户数量限制
    OnLineLimit = 0

    #检查密码强度
    EnableCheckPasswordStrength = False

    #是否检查用户IP地址
    EnableCheckIPAddress = False

    #禁止用户重复登录,只允许登录一次
    CheckOnLine = False

    #服务器端加密存储密码
    EnableEncryptServerPassword = True

    #密码错误锁定次数
    PasswordErrorLockLimit = 5

    #连续输入N次密码后，密码错误锁定周期(分钟),0 表示 需要系统管理员进行审核，帐户直接被设置为无效
    PasswordErrorLockCycle = 30

    #检查密码强度
    EnableCheckPasswordStrength = False

    #是否更新访问日期信息
    UpdateVisit = True

    #启用组织机构权限
    EnableOrganizePermission = True

    # 是否已经成功登录系统

    LogOned = False

    # 用户在线状态

    OnLineState = 0

    # region 客户端的配置信息部分

    # 当前用户名

    CurrentUserName = 'admin'

    # 当前密码

    CurrentPassword = 'admin'

    # 登录是否保存密码，默认能记住密码会好用一些

    RememberPassword = True

    # 是否自动登录，默认不自动登录会好一些

    AutoLogOn = False

    # 客户端加密存储密码，这个应该是要加密才可以

    EncryptClientPassword = True

    # 远程调用Service用户名（为了提高软件的安全性）

    ServiceUserName = "RDIFramework"

    # 远程调用Service密码（为了提高软件的安全性）

    ServicePassword = "RDIFramework654123"

    # 默认加载所有用户用户量特别大时的优化配置项目，默认是小规模用户

    LoadAllUser = True

    # 动态加载组织机构树，当数据量非常庞大时用的参数，默认是小规模用户

    OrganizeDynamicLoading = True

    # 是否采用多语言

    MultiLanguage = False

    # 当前客户选择的语言

    CurrentLanguage = "zh-CN"

    # 当前语言

    Themes = ''

    lockWaitMinute = 60

    # 即时通信指向的网站地址

    WebHostUrl = "WebHostUrl"

    # 显示异常的详细信息?

    ShowExceptionDetail = True

    # 显示操作成功信息？

    ShowSuccessMsg = True

    # 分页大小(默认为每页显示20条数据)

    PageSize = 50

    # 配置文件名称

    ConfigFile = "Config"
    # endregion

    # region 服务器端的配置信息

    # 主机地址
    # Host = "127.0.0.1"

    Host = ''

    # 端口号

    Port = 0

    # 允许新用户注册

    AllowUserToRegister = True

    # 是否启用即时内部消息

    UseMessage = True

    # 是否启用表格数据权限
    # 启用分级管理范围权限设置，启用逐级授权

    EnableUserAuthorizationScope = False

    # 启用按用户权限

    EnableUserAuthorization = True

    # 启用模块菜单权限

    EnableModulePermission = True

    # 启用操作权限

    EnablePermissionItem = True

    # 启用数据表的约束条件限制

    EnableTableConstraintPermission = False

    # 启用数据表的列权限

    EnableTableFieldPermission = False


    # 设置手写签名

    EnableHandWrittenSignature = True

    # 登录历史纪录

    EnableRecordLogOnLog = True

    # 是否进行日志记录

    EnableRecordLog = True

    # 是否更新访问日期信息

    UpdateVisit = True

    # 同时在线用户数量限制

    OnLineLimit = 0

    # 是否检查用户IP地址

    EnableCheckIPAddress = False

    # 是否登记异常

    LogException = True

    # 是否登记数据库操作

    LogSQL = False

    # 是否登记到 Windows 系统异常中

    EventLog = False

    # 系统默认密码

    DefaultPassword = "abcd1234"

    # endregion

    # region 服务器端安全设置

    # 检查密码强度

    EnableCheckPasswordStrength = False

    # 服务器端加密存储密码

    EnableEncryptServerPassword = True

    # 密码最小长度

    PasswordMiniLength = 6

    # 必须字母+数字组合

    NumericCharacters = True

    # 密码修改周期(月)

    PasswordChangeCycle = 3

    # 禁止用户重复登录
    # 只允许登录一次

    CheckOnLine = False

    # 用户名最小长度

    AccountMinimumLength = 4

    # 密码错误锁定次数

    PasswordErrorLockLimit = 5

    # 连续输入N次密码后，密码错误锁定周期(分钟)
    # 0 表示 需要系统管理员进行审核，帐户直接被设置为无效

    PasswordErrorLockCycle = 30


    # 是否加数据库连接

    EncryptDbConnection = False

    # 数据库连接

    RDIFrameworkDbConection = ''

    # 数据库连接的字符串

    RDIFrameworkDbConectionString = ''

    # 业务数据库

    BusinessDbConnection = ''

    # 业务数据库（连接串，可能是加密的）

    BusinessDbConnectionString = ''

    # 工作流数据库

    WorkFlowDbConnection = ''

    # 工作流数据库（连接串，可能是加密的）

    WorkFlowDbConnectionString = ''

    # endregion

    # region 系统性的参数配置

    # 软件是否需要注册

    NeedRegister = True

    # 检查周期[以秒为单位]2分钟内不在线的，就认为是已经没在线了，心跳方式检查

    OnLineTime0ut = 2 * 60 + 20

    # 每过1分钟，检查一次在线状态

    OnLineCheck = 60

    # 注册码

    RegisterKey = ''

    # 当前网站的安装地址

    StartupPath = ''

    # 是否区分大小写

    MatchCase = True

    # 最多获取数据的行数限制

    TopLimit = 200

    # 锁不住记录时的循环次数

    LockNoWaitCount = 5

    # 锁不住记录时的等待时间

    LockNoWaitTickMilliSeconds = 30

    # 是否采用服务器端缓存

    ServerCache = False

    # 最后更新日期

    LastUpdate = "2016.02.18"

    # 当前版本

    Version = "3.0"

    # 每个操作是否进行信息提示。

    ShowInformation = True

    # 时间格式

    TimeFormat = "HH:mm:ss"

    # 日期短格式

    DateFormat = "yyyy-MM-dd"

    # 日期长格式

    DateTimeFormat = "yyyy-MM-dd HH:mm:ss"

    # 当前软件Id

    SoftName = ''

    # 软件的名称

    SoftFullName = ''

    # 根菜单编号

    RootMenuCode = ''

    # 是否采用客户端缓存

    ClientCache = False

    # 当前客户公司名称

    CustomerCompanyName = ''

    # 系统图标文件

    AppIco = "Resource\\App.ico"

    # 插件所在的目录

    AddInDirectory = "AddIn\\"

    # RegistryKey、Configuration、UserConfig 注册表或者配置文件读取参数


    RegisterException = "请您联系：EricHu QQ:406590790 手机：13005007127 电子邮件：406590790@qq.com 对软件进行注册。"

    CustomerPhone = "" # 当前客户公司电话
    CompanyName = "" # 公司名称
    CompanyPhone = "13005007127" # 公司电话

    Copyright = "Copyright 2009-2016 EricHu"

    "http://download.microsoft.com/download/ie6sp1/finrel/6_sp1/W98NT42KMeXP/CN/ie6setup.exe"

    HelpNamespace = ''
    UploadDirectory = "Document/"
    # endregion

    # region 客户端动态加载程序相关

    # 主应用程序集名

    MainAssembly = ''
    MainForm = "FrmRDIFrameworkNav"

    LogOnAssembly = "RDIFramework.NET"
    LogOnForm = "FrmLogOn"

    # 服务实现

    Service = "RDIFramework.BizLogic"

    # 服务映射工厂

    ServiceFactory = "ServiceFactory"

    DbProviderAssmely = "RDIFramework.Utilities"

    # 当前主题样式

    CurrentStyle = "VisualStudio2010Blue"

    # 当前主题颜色

    CurrentThemeColor = ''
    # endregion

    # region 系统邮件错误报告反馈相关

    # 发送给谁，用,符号隔开

    ErrorReportFrom = "406590790@qq.com"

    # 邮件服务器地址

    ErrorReportMailServer = "smtp.126.com"

    # 用户名

    ErrorReportMailUserName = "umplatform@126.com"

    # 密码

    ErrorReportMailPassword = "umplatform2012"

    # 平台博客

    RDIFrameworkBlog = "http://www.cnblogs.com/huyong/"

    # 平台微博（腾讯）

    RDIFrameworkWeibo = "http://t.qq.com/yonghu86"

    # endregion

    # 工作流节点超时时间设置（以小时为单位）

    NodeTimeout = "72"
