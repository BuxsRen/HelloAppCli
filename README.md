# Hello App For Python Cli

> 服务端
>
> https://github.com/BuxsRen/Hello
>

> 安卓客户端端
>
> https://github.com/BuxsRen/HelloApp

#### 介绍

- Hello App Python 命令行版本
- 支持登录
- 在线用户列表
- 用户上线通知
- 接听语音通话

#### 问题
- 音质问题，全损音质(估计是python gzip的问题)

#### 改进
- 后续可能会推出UI页面，实现桌面版本

#### 配置
```shell script
.app.ini
```

#### 登录
```text
在 main.py 中配置登录的邮箱和密码
```

#### 运行
```shell script
python main.py

# 登录成功会提示如下内容
"""
√ 登录成功
---------------------------
       用户列表
---------------------------

[1] Break (441479573@qq.com)
[2] 杰瑞 (474024153@qq.com)
[3] 小冰 (2793469806@qq.com)
[4] ikun (buxsren@qq.com)

---------------------------

在线用户: [1, 2]
"""
```

