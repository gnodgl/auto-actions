## 功能
1. 基于NuxusPHP的PT站签到,说谢谢,吼吼箱,投票
2. 基于Discuz的网站 [天使动漫,不移之火...]签到
3. HIFI,贴吧,SMZDM 签到
## 使用
0. Fork仓库
1. 添加环境变量,Settings > Secrets > New secret > 添加如下几个环境变量
2. 配置文件 config.ini [thanks_id] 项下内容删除，这里用来记录已经说谢谢的id
## 环境变量配置
1. CONFIG 下面例子内 所有'#'后的内容删除,不能写注释
````
[
    {
        # 地址
        'name':'网站昵称',
        'url':'https://www.XXX.com', 
        # cookie 执行从浏览器粘贴出来就行，不用处理，包在引号内就行
        'cookie':'__cfduid=d07c2c6b96d23b4a74c9f82b3bb55f9c1598353026; c_secure_uid=MjEwMA%3D; c_secure_pass=a7b591404ca1eb1ce113e26230988db; c_secure_ssl=eWVhaA%3%3D; c_secure_tracker_ssl=bm9wZQ3D%3D; c_secure_login=bm9ZQ%3D%3D',
        #执行哪些任务的列表 签到,说谢谢,吼吼箱,投票
        'tasks':['sign_in','say_thanks','shout','vote'] 
	},
    # 如果还有其他站点，把上面的 配置复制一份,
    {
        'name':'网站昵称',
        'url':'https://www.YYY.com', 
        'cookie':'__cfduid=d07c2c6b96d23b4a74c9f82b3bb55f9c1598353026; c_secure_uid=MjEwMA%3D; c_secure_pass=a7b591404ca1eb1ce113e26230988db; c_secure_ssl=eWVhaA%3%3D; c_secure_tracker_ssl=bm9wZQ3D%3D; c_secure_login=bm9ZQ%3D%3D',
        'tasks':['sign_in',] 
	},
    # discuz类型网站签到
    {
        'name':'网站昵称',
        'url':'https://www.ZZZ.com', 
        'cookie':'__cfduid=d07c2c6b96d23b4a74c9f82b3bb55f9c1598353026; c_secure_uid=MjEwMA%3D; c_secure_pass=a7b591404ca1eb1ce113e26230988db; c_secure_ssl=eWVhaA%3%3D; c_secure_tracker_ssl=bm9wZQ3D%3D; c_secure_login=bm9ZQ%3D%3D',
        'tasks':['sign_in_discuz',] 
	}
]
````
~~2. QMSGAPI 前往[qmsg](https://qmsg.zendee.cn)申请您的KEY填入变量~~

3. BDUSS 值:贴吧签到cookie中的bduss值
4. V2EX_COOKIES 值:V2EX论坛签到cookie
5. SMZDM_COOKIES 值:SMZDM论坛cookie
6. GTAPI telegram机器人通知api
7. CHATID telegram会话id
