# SM2-2P-decrypt-with-real-network-communication
![0)8VGPC2G64TSLJR(LEXF F](https://github.com/Basoob/Innovation-and-Entrepreneurship-Practice-Homework/assets/141385265/c262c40a-ce78-4fdc-91ac-3f23aa8f96d4)
SM2 two-party decrypt算法如上图
## 文件介绍：
client.py -客户端文件
<br>server.py -服务端文件
<br>sm3.py -SM3算法实现
<br>sm2.py -SM2算法实现
## 实现流程：
遵循协议图，分别于client和server文件中定义相关函数，并使用socket进行模拟通讯，具体函数如下：
<br>client：
<br>KDF(str, klen):密钥派生函数
<br>inverse(a_x,a_y)：椭圆曲线的求逆函数
<br>generate_K()：生成私钥d1和P1
<br>generate_T1(C1,d1)：接收C1，生成T1
<br>encrypt(message, P)：加密函数
<br>decrypt(T2,C1,C2,C3):解密函数
<br>server：
<br>inverse(a_x,a_y)：椭圆曲线的求逆函数
<br>generate_K_P(P1)：生成d2和P
<br>generate_T2(d2,T1):接收T1，生成T2
## 运行指导
将文件夹内全部代码放入项目，首先运行server.py文件，再运行client.py即可
## 运行结果
![project16-1](https://github.com/Basoob/Innovation-and-Entrepreneurship-Practice-Homework/assets/141385265/2518b105-0dda-41f1-a184-7c35cee3b6d8)
![project16-2](https://github.com/Basoob/Innovation-and-Entrepreneurship-Practice-Homework/assets/141385265/9ead870c-f0d5-4dad-b7ff-5e0cb7d15829)
