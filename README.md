# 微信爬虫
__⚠️⚠️⚠️该方法因为是抓包模拟操作，因此有一定的风险⚠️⚠️⚠️__
以下为部署文档

## 功能：

- [x] 检测公众号每日新发文章
- [x] 抓取公众号信息
- [x] 抓取文章列表
- [x] 抓取文章信息
- [x] 抓取阅读量、点赞量、评论量
- [x] 抓取评论信息
- [x] 临时链接转永久链接

## 特色：

1. **免安装**：一键部署运行
2. **自动化**：只需要配置好待监控的公众号列表，启动软件后即可每日自动抓取公众号及文章等信息
3. **好对接**：抓取到的数据使用mysql存储，方便处理数据
4. **不漏采**：采用任务状态标记的方式，防止遗漏每一个公众号、每一篇文章

## 所需环境

1. mysql：用来存储抓取到的数据以及任务表
2. redis：任务缓存，减少操作mysql的次数

## 安装配置

> 以下安装说明安需查看，仅作为参考。因每个人环境不同，可能安装会有些差异，可参考网上的资料

### 1. 安装mysql并且运行
### 2. 安装redis-server
### 3. 安装mitmproxy证书，具体步骤参照官网https://mitmproxy.org/
#### 3.1 window
 2. 双击运行
 3. 安装到本地计算机
 4. 需要密钥时跳过
 5. 选择“将所有的证书都放入下列存储”，接着选择“受信任的根证书颁发机构”
 6. 最后，弹出警告窗口，直接点击“是”

#### 3.2 mac
2. 下载完双击安装
3. 打开Keychain Access.app
4. 选择login(Keychains)和Certificates(Category)中找到mitmproxy
5. 点击mitmproxy，在Trust中选择Always Trust


### 4. 配置代理

> 如果使用手机，需要确保手机和运行wechat-spider的电脑连接在同一个路由器上

#### 3.1 iphone

打开设置-无线局域网-所连接的Wifi-配置代理-手动
填上该安装服务器的IP和端口8080

#### 3.2 android

打开设置-WLAN-长按所连接的网络-修改网络-高级选项-手动
填上该安装服务器的IP和端口8080

#### 3.3 window
打开chrome 设置->高级
![A580D0082CCEE0621F98FAF003C5530E](media/A580D0082CCEE0621F98FAF003C5530E.png)
![95AE10B3227FDE0637AB227A5A8267E3](media/95AE10B3227FDE0637AB227A5A8267E3.png)

#### 3.4 mac

打开系统配置（System Preferences.app）- 网络（Network）- 高级（Advanced）- 代理（Proxies）- Secure Web Proxy(HTTPS)
填上该安装服务器的IP和端口8080

![-w668](media/15584581938431.jpg)
![-w667](media/15584582326072.jpg)



## 使用说明

### 1. 安装如上说明安装好证书及配置好代理
### 2. 正确配置config.yaml

主要是配置mysql及redis的链接信息，确保能正确链接上

### 3. 创建数据库 wechat

![-w418](media/15610827417503.jpg)


### 4. 启动wechat-spider

进入wechat-spider目录，运行`python(3) run.py`

此步骤如果config里的auto_create_tables值为true时，会自动创建mysql数据表。建议首次启动时设置为true，创建完表后设置为false

### 5. 点击任意一公众号，查看历史消息（需要关注，以mac为例）

![-w637](media/15584585019970.jpg)

当出现如上红框中的提示信息时，说明大功告成了，过一会可以去数据库里验证数据了

第一次启动时 需要逐个访问需要爬取的公众号历史消息界面 添加成功后 每次需要爬取时只需要打开其中一个的公众号详情即可爬取所有公众号消息

### 6. 导出公众号数据为excel文档

运行utils文件下的`export_excel.py`

```shell script
python(3) export_excel.py
```
![-w637](media/export_as_excel.png)

如上图所示 依照指示完成即可

## 常见问题

### 1. mysql 链接问题

问题：链接时打印object supporting the buffer api required异常
![](media/15610832298058.jpg)
解决: 如果密钥是整形的，如123456，需要在配置文件中加双引号，如下：

    mysqldb:
      ip: localhost
      port: 3306
      db: wechat
      user: root
      passwd: "123456"
      auto_create_tables: true # 是否自动建表 建议当表不存在是设置为true，表存在是设置为false，加快软件启动速度

### 2. 正确配置完代理后提示证书或安全问题

原因是我那个证书失效了，可参考 https://www.cnblogs.com/yunlongaimeng/p/9617708.html 安装数据

### 3. 提示无任务

检查 wechat_account_task 表中是否下发了__biz(微信公众号的唯一标识)。可多下发几个测试

### 4. Exception:DISCARD without MULTI

使用管理员模式启动redis

### 5. 正常启动后抓不到包

1. 检是否设置代理
2. 检查端口是否被占用
