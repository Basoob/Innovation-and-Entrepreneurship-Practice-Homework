import random
import time
m='61626364616263646162636461626364616263646162636461626364616263646162636461626364616263646162636461626364616263646162636461626364'
IV='7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e'
#填充函数
def padding(m):
    #将信息填充为512bit的整数倍
    #最后64bit表示长度
    m_bin_len = len(m)*4
    #m为16进制，乘以四表示二级制长度
    m_new = m + '8'
    #'8'二进制表示为‘1000’，表示填充的首位为1
    #m_new为16进制，需要的长度为512bit=128字节的整数倍
    lenth_0 = 112- (len(m_new) % 128)
    #填充0
    m_new = m_new + '0'*lenth_0
    #在最后64bit填充长度
    padiing_length_m = '{:016x}'.format(m_bin_len)
    m_new = m_new + padiing_length_m
    return m_new

#分组函数
def group(m):
    m = padding(m)
    m_list = []
    #将m划分为若干个512bit的块
    group_num = len(m) / 128
    for i in range(int(group_num)):
        tmp = m[0+128*i:128*(i+1)]
        m_list.append(tmp)
    return m_list

#扩展函数
def expand(m,n):
    #n代表是第几组消息，消息之间没有关系，不用迭代
    m_list = group(m)

    W = ['0' for i in range(68)]
    W_0 = ['0' for i in range(64)]
    ex_num=len(m_list[n])/8
    for i in range(int(ex_num)):
        w = m_list[n][i*8:(i+1)*8]
        W[i] = w
    for j in range(16,68):
        tmp = Xor(W[j - 16], W[j - 9])
        W_j_3 = Shift(W[j - 3], 15)
        tmp = Xor(tmp, W_j_3)
        tmp = P1(tmp)
        W_j_13=Shift(W[j - 13], 7)
        tmp = Xor(tmp, W_j_13)
        tmp = Xor(tmp, W[j - 6])
        W[j]=tmp
    for j in range(64):
        W_0[j]=Xor(W[j], W[j + 4])
    return W,W_0

#置换函数
def P1(X):
    #X为32位字
    X_15 = Shift(X, 15)  #循环移位
    X_23 = Shift(X, 23)
    a = Xor(X, X_15)
    a = Xor(a, X_23)
    return a

#置换函数
def P0(X):
    #X为32位字
    X_9 = Shift(X, 9)
    X_17 = Shift(X, 17)
    a = Xor(X, X_9)
    a = Xor(a, X_17)
    return a

#异或函数
def Xor(A,B):
    A = int(A,16)
    B = int(B,16)
    C = A ^ B
    C = '{:08x}'.format(C)
    return C

#移位函数
def Shift(W,n):
    a = int(W,16)
    a = '{:032b}'.format(a)
    while n>=32:
        n=n-32
    a = a[n:] + a[:n]
    a = int(a,2)
    a = '{:08x}'.format(a)
    return a

#常量Tj
def T_j(j):
    if j<=15:
        T_j='79cc4519'
    else:
        T_j='7a879d8a'
    return T_j

#mod 2^32 算术加运算
def add(x,y):
    x = int(x,16)
    x = '{:032b}'.format(x)
    x = list(x)
    y = int(y, 16)
    y = '{:032b}'.format(y)
    y = list(y)

    a = [0 for _ in range(32)]
    carry = 0
    for i in range(32):
        m = int(x[31-i])+int(y[31-i])+carry
        if m>=2:
            d=m-2
            a[31-i]=str(d)
            carry=1
        else:
            carry=0
            d=m
            a[31 - i] = str(d)

    b=''.join(a)
    b=int(b,2)
    b='{:08x}'.format(b)
    return b

#布尔函数
def FF_j(X,Y,Z,j):
    if j<=15:
        a = Xor(X, Y)
        a = Xor(a, Z)
    else:
        a = and_Cal(X,Y)
        b = and_Cal(X,Z)
        c = and_Cal(Y,Z)
        a = or_Cal(a,b)
        a = or_Cal(a,c)
    return a

#布尔函数
def GG_j(X, Y, Z, j):
    if j <= 15:
        a = Xor(X, Y)
        a = Xor(a, Z)
    else:
        a = and_Cal(X,Y)
        b = qufan(X)
        b = and_Cal(b,Z)
        a = or_Cal(a,b)
    return a

#与运算函数
def and_Cal(a,b):
    a = int(a,16)
    b = int(b,16)
    a_b = a & b
    a_b = '{:08x}'.format(a_b)
    return a_b

#或运算函数
def or_Cal(a,b):
    a = int(a, 16)
    b = int(b, 16)
    a_b = a | b
    a_b = '{:08x}'.format(a_b)
    return a_b

#按位取反函数
def qufan(A):
    A = int(A,16)
    A = '{:032b}'.format(A)
    A = list(A)
    for i in range(32):
        if A[i]=='0':
            A[i]='1'
        else:
            A[i]='0'
    A = ''.join(A)
    A = int(A,2)
    A = '{:08x}'.format(A)
    return A

#压缩函数
m_list = group(m)
m_len = len(m_list)
V = ['0' for i in range(m_len+1)]
V[0]=IV

#压缩函数
def CF(m,n,k):
    w = expand(m, n)
    W = w[0]
    W_0 = w[1]
    A=V[k][0:8]
    B=V[k][8:16]
    C=V[k][16:24]
    D=V[k][24:32]
    E=V[k][32:40]
    F=V[k][40:48]
    G=V[k][48:56]
    H=V[k][56:64]
    #print(W_0)
    all=''
    for j in range(64):
        #print(E)
        b= a = Shift(A, 12)
        #t = b
        T = T_j(j)
        #
        T = Shift(T, j)  #忘记移位了，移位问题
        a = add(a,E)
        a = add(a,T)
        SS1 = Shift(a, 7)
        SS2 = Xor(SS1, b)
        b = FF_j(A,B,C,j)
        b = add(b,D)
        b = add(b,SS2)
        TT1 = add(b,W_0[j]) #
        b = GG_j(E,F,G,j)
        b = add(b, H)
        b = add(b, SS1)
        TT2 = add(b, W[j]) #
        D = C
        C = Shift(B, 9)
        B = A
        A = TT1#
        H = G
        G = Shift(F, 19)
        F = E
        E = P0(TT2)  #
        all = A+B+C+D+E+F+G+H

    V[k+1]= Xor(V[k], all)


def hash(m=m):
    for i in range(m_len):
        v_n=CF(m,i,i)
    print(V[-1])
    return V[-1]

def birthday_attack(bit_num):
    attack_table = {}
    num = int(2 ** (bit_num / 2))
    count=0
    while True:
        #生成随机消息
        message = str(random.getrandbits(512))
        hash_value = hash(message)
        #取前n个bit的字节
        check_hash = hash_value[:bit_num // 4]
        if check_hash in attack_table:
            # 找到碰撞
            original_message = attack_table[check_hash]
            print("碰撞消息1：", original_message)
            print("碰撞消息2：", message)
            print("哈希值：", hash_value)
            break
        else:
            #没碰撞就存表
            attack_table[check_hash] = message
        count=count+1
        if count==num:
            print("没有找到碰撞")
            return
start=time.time()
n=24
birthday_attack(n)
end=time.time()
totaltime=end-start
print("用时",totaltime,"s")
print("前",n,"bit碰撞已完成")