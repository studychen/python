# python
##说明

此仓库保存笔者的一些 python 项目。

本项目地址 [https://github.com/studychen/python/](https://github.com/studychen/python/)

个人博客，欢迎交流 [http://blog.csdn.net/never_cxb](http://blog.csdn.net/never_cxb)

目前一共有下面几个项目

- webCrawler 爬虫 BBS 用户 id、性别、注册时间、活动时间，统计男女比例

- applyCloudMachine.py 申请云端机器（多线程，基于applyfinal.sh）

- findNinePort.py 多个平台找出连续9个空闲端口

- sumSapLogon.py Windows 机器上登录图形化工具，并执行创建数据库用户、对数据库加负载

- sumPreAuto.py 测试前期工作自动化，主要步骤为：拷贝安装包、安装软件、检验是否成功、复制修改配置文件、打开监听端口、扩展数据库

- installAuto.py 安装自动化，多线程安装，查看端口验证是否安装成功

- cleanHadrEnv.py 暴力卸载软件（删目录文件、清空共享内存），把脚本复制到远程机器上，再远程执行命令

 # shell

此仓库保存个人的一些 shell 脚本，方便自动化工作，提高效率。

项目地址 [https://github.com/studychen/shell/](https://github.com/studychen/shell/)

个人博客，欢迎交流 [http://blog.csdn.net/never_cxb](http://blog.csdn.net/never_cxb)

目前一共有下面几个脚本

- applyCloudMachine.sh	申请云端机器，根据OS（Linux/Windows）、硬盘大小、描述
- changePasswd.sh	挂载硬盘，建立目录、建立 link、修改密码
- cleanHadrEnv.sh	强制删除，杀进程、删除软件相关的目录和文件、删除用户、清理共享内存
- extendDatabase.sh	扩展数据库数据文件和日志文件，后期改用 [https://github.com/studychen/java/tree/master/ExtendDatabase](https://github.com/studychen/java/tree/master/ExtendDatabase) 
- installSapcar.sh	自动化 linux 安装某软件，主要是处理软件提示信息 option、yes/no等等
- manageVolumes.sh	挂载硬盘、建立目录，方便后期自动化
- releaseCloudMachine.sh 删除云端机器，先删除硬盘，再删除机器示例


