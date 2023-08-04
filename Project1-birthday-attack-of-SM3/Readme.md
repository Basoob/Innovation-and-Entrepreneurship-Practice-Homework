# 生日攻击
## 基本原理
生日攻击（Birthday Attack）是一种密码学中的碰撞攻击。生日攻击的原理是通过随机生成大量的输入消息，并计算它们的哈希值，然后在已计算的哈希值集合中查找是否存在相同的哈希值。如此重复进行，直到找到一个碰撞。根据生日悖论，当哈希值空间的大小接近实际计算的哈希值数量时，找到碰撞的概率会显著增加。通常来说，对长为n bit的哈希值进行生日攻击，进行O(2^(n/2))次搜索后即有较高的概率找到碰撞。
## 实现思路
不断生成随机数计算哈希值，并寻找碰撞，没有碰撞则将结果存入表格，直至寻找到碰撞。
## 运行指导
直接运行birthday_attack.py文件即可
## 补充说明
哈希值的计算使用SM3算法，SM3的python实现参考自CSDN，链接为：https://blog.csdn.net/qq_43710705/article/details/103915133
## 运行结果
![project1-1](https://github.com/Basoob/Innovation-and-Entrepreneurship-Practice-Homework/assets/141385265/714521c5-fce6-4582-aa52-8d053e452b76)
![project1-2](https://github.com/Basoob/Innovation-and-Entrepreneurship-Practice-Homework/assets/141385265/d65000fc-f366-4a40-8c2f-eb87d5b93e52)
![project1-3](https://github.com/Basoob/Innovation-and-Entrepreneurship-Practice-Homework/assets/141385265/f739381e-42dd-4119-a613-080b0eaf9ae8)
