# AES算法实现
## AES实现原理
AES（Advanced Encryption Standard）是一种对称加密算法，使用128位密钥进行数据加密和解密。下面是AES-128的实现原理：

* 初始化密钥扩展：将128位的密钥扩展为一系列轮密钥，每个轮密钥的长度也是128位。这些轮密钥将用于加密和解密过程中的轮函数。
* 初始轮（AddRoundKey）：将输入数据与第一个轮密钥进行异或运算。
* 轮函数（SubBytes、ShiftRows和MixColumns）：在每一轮中，对输入数据进行一系列替换和置换操作。首先，通过SubBytes操作将输入数据中的每个字节替换为预定义的S盒中对应的字节。然后，通过ShiftRows操作对每一行进行循环左移操作。最后，通过MixColumns操作将每一列进行线性变换。
* 轮密钥加（AddRoundKey）：将经过轮函数处理后的数据与当前轮的轮密钥进行异或运算。
<br>重复进行第3步和第4步，直到达到最后一轮。在最后一轮中，不进行MixColumns操作。
* 最终轮（SubBytes、ShiftRows和AddRoundKey）：在最后一轮中，将经过轮函数处理后的数据进行SubBytes和ShiftRows操作，然后再与最后一个轮密钥进行异或运算。
* 解密：对加密后的数据进行逆向操作，将轮密钥的顺序逆序应用于解密过程。
流程图如下：
![project9-1](https://github.com/Basoob/Innovation-and-Entrepreneurship-Practice-Homework/assets/141385265/8998a2be-7dbf-4109-ac9e-8e3baa8f1f7e)

* 流程图摘自知乎，链接：https://zhuanlan.zhihu.com/p/78913397
## 代码介绍：
* LowtoUpper() 小写字母转大写字母
* BintoHex() 二进制转十六进制
* HextoBin() 十六进制转二进制
* HextoDec() 十六进制字符转十进制数字
* DectoHex() 十进制数字转十六进制字符
* HexXor() 等长的十六进制数异或
* create_key() 生成密钥
* show_arr() 输出数组中的各个元素
* transfer() 将一维数组转二维
* show_arr4() 输出4x4数组中的各个元素
* show_arr4_11() 输出4x8数组中的各个元素
* SubBytes() 字节代换
* ShiftRows() 行移位
* MixColumn_mul_02() 列混合
* MixColumn_mul() 列混合中的乘法
* MixColumn() 列混合 
* T_shiftwords() T函数中的字循环
* SubBytes() T函数中的字节代换
* HexXor() T函数中的异或 
* key_extend_T() 轮密钥扩展的T函数
* key_extend() 轮密钥扩展
* Round() 轮函数
* Final_Round() 最后一轮轮函数

## 补充说明：
该代码实现的版本为AES_128算法，由小组完成，小组成员：班世博，郭梦涵，贾成志，姜万瑞
## 运行结果：
![project9-2](https://github.com/Basoob/Innovation-and-Entrepreneurship-Practice-Homework/assets/141385265/453080d2-d0b9-4583-999a-0ff0d23c09e2)
![project9-3](https://github.com/Basoob/Innovation-and-Entrepreneurship-Practice-Homework/assets/141385265/311e5188-9da1-45ef-8646-0f6af6fb3bfe)
![project9-4](https://github.com/Basoob/Innovation-and-Entrepreneurship-Practice-Homework/assets/141385265/19ac7abc-4e34-4ab9-a3b4-d076cd7040cf)
