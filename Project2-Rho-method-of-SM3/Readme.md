# Pollard Rho攻击
## 实现思路
选取随机值h，计算SM3(h)，并寻找碰撞，如果没找到碰撞则将当前值存入碰撞表，并将函数返回的加密结果作为下一次函数的输入，即计算SM3(SM3(h)),不断计算下去，直到找到碰撞，这代表进入Rho循环，SM3结果会周期性出现。
## 代码实现：
Rho_attack()函数：用于实现攻击的代码，攻击方法类似于生日攻击，但迭代方式为不断哈希。
## 运行指导
将文件夹内全部代码放入项目，直接运行Rho_method.py文件即可
## 补充说明:
SM3实现参考自CSDN,并做了适当修改
CSDN链接:https://blog.csdn.net/qq43710705/article/details/103915133
## 运行结果：
![project2-1](https://github.com/Basoob/Innovation-and-Entrepreneurship-Practice-Homework/assets/141385265/875d374f-c5e4-486f-8d7d-4b38027c7e82)
![project2-2](https://github.com/Basoob/Innovation-and-Entrepreneurship-Practice-Homework/assets/141385265/b21a8f95-2194-4e66-8d1e-749f249e6e59)
![project2-3](https://github.com/Basoob/Innovation-and-Entrepreneurship-Practice-Homework/assets/141385265/31e710b8-baca-43c1-a597-44260a761b0a)



