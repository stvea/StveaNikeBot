# StveaNikeBot
## 前言
断断续续写了一个月左右，基本完成了Bot的功能，并可以正常抽签，也有抽签成功的记录。但是由于抽签时间和上课时间冲突，测试的机会少，所以开源给各位作为一个抛砖引玉吧，希望更多的人可以有自己的私人bot。
其实bot的思路并不难，但其中坑比较多，如果希望联系到我或者到vx群交流可以直接加我vx:SteveWoz
## 如何运行
在第一次运行之前，运行 /Model/SqliteDao.py 中的init方法生成本地的Sqlite数据库，之后向数据库中插入账号。
### 抽签基本流程：
  1.获得账号refreshToken，有效期一个月
  2.使用refreshToken获得accessToken
  3.使用accessToken抽签
