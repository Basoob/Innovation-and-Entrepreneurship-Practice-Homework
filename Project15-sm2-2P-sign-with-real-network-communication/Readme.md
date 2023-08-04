# SM2-2P-sign-with-real-network-communication
![8LKVD`ZF6`A8T)UK `E{66X](https://github.com/Basoob/Innovation-and-Entrepreneurship-Practice-Homework/assets/141385265/e4fabe72-68cb-4102-974a-df274d7be688)
SM2 two-party sign协议如图
## 代码文件介绍：
client.py -客户端文件
<br>server.py -服务端文件
<br>sm3.py -SM3算法实现
<br>sm2.py -SM2算法实现
## 实现流程：
遵循协议图，分别于client和server文件中定义相关函数，并使用socket进行模拟通讯，具体函数如下：
<br>client：
<br>generate_K_P1()函数：生成私钥d1和P1
<br>generate_Q1_e(Z, M)函数：接收Z和M，生成Q1和哈希值e
<br>Sign(d1, k1, s2, s3, r)函数：客户端签名函数
<br>server：
<br>inverse(a_x,a_y)函数：椭圆曲线的求逆函数
<br>generate_K_P(P1)函数：生成d2和P
<br>generate_r_s2_s3(Q1,d2,e)函数：生成r,s2和s3
## 运行指导
将文件夹内全部代码放入项目，首先运行server.py文件，再运行client.py即可
## 运行结果
![project15-1](https://github.com/Basoob/Innovation-and-Entrepreneurship-Practice-Homework/assets/141385265/4517a505-a79e-45b7-ab33-bc56d3c7b9ad)
![project15-2](https://github.com/Basoob/Innovation-and-Entrepreneurship-Practice-Homework/assets/141385265/1caa79d2-edab-46fe-8969-a1bf1b8e2e98)
