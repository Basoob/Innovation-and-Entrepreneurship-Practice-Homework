# client
import sm2
import socket
import random
import sm3
import hashlib


# SM2参数
p = int("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF", 16)
a = int("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC", 16)
b = int("28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93", 16)
n = int("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123", 16)
G_x = int("32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7", 16)
G_y = int("BC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0", 16)

klen=32

def KDF(str, klen):
    derived_key = ""
    counter = 0

    while len(derived_key) < klen:
        current_input = str + bytes([counter]).decode()
        hash_result = sm3.hash(current_input)
        derived_key += hash_result
        counter += 1

    return derived_key[:klen]

def inverse(a_x,a_y):
    a_inv_x = a_x
    a_inv_y=p - a_y
    return a_inv_x,a_inv_y

def generate_K():
    #私钥d1
    d1 = random.randint(1, n - 1)
    temp = pow(d1,-1, n)
    P1 = sm2.mul(p,G_x,G_y,temp)
    return d1, P1
def generate_T1(C1,d1):
    if C1==0:
        return None
    temp = pow(d1, -1, n)
    T1 = sm2.mul(p, C1[0], C1[1], temp)
    return T1

def decrypt(T2,C1,C2,C3):
    C1_inv_x, C2_inv_y = inverse(C1[0], C1[1])
    temp= sm2.add(p,T2[0],T2[1],C1_inv_x,C2_inv_y)
    x2 = hex(temp[0])[2:]
    y2 = hex(temp[1])[2:]
    t=KDF(x2+y2,klen)
    #print("t:",t)
    #t=hex(int(t,2))[2:]
    M = hex(int(C2, 16) ^ int(t, 16))[2:]
    u=sm3.hash(x2+M+y2)
    if u==C3:
        return  M
    else:
        print("解密失败")


def encrypt(message, P):
    k = random.randint(1, n - 1)
    C1=sm2.mul(p,G_x,G_y,k)
    tmp=sm2.mul(p,P[0],P[1],k)
    x2=hex(tmp[0])
    x2=x2[2:]
    y2=hex(tmp[1])
    y2 =y2[2:]
    #print(type(x2))
    #print("x1",x2)
    #print("x2",y2)
    t = KDF(x2 + y2, klen)
    #print(t)
    #t=t[2:]
    #print("t:",t)
    #print(t.decode())
    #t = hex(int(t,2))[2:]
    #print(t)
    C2=hex(int(message, 16) ^ int(t, 16))[2:].zfill(16)
    M_=x2+message+y2
    #print(type(M_))
    #print(M_)
    C3=sm3.hash(M_)
    return C1,C2,C3

if __name__ == "__main__":
    # 建立连接
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("客户端已连接")
    address= ("127.0.0.1", 12345)
    #生成d1和P1
    d1, P1 = generate_K()
    #发送P1
    data = str(P1[0]) + ';' + str(P1[1])
    print("发送信息data:", data)
    s.sendto(data.encode(),address)

    data,addr=s.recvfrom(1024)
    data=data.decode()
    index=data.find(';')
    Public_key_x=int(data[:index])
    Public_key_y=int(data[index+1:])
    Public_key=(Public_key_x,Public_key_y)
    print("成功接收公钥：",Public_key)

    #加密
    message=input("message:")
    C1,C2,C3= encrypt(message, Public_key)
    T1=generate_T1(C1,d1)
    data = str(T1[0]) + ';' + str(T1[1])
    s.sendto(data.encode(),addr)
    #解密
    data,addr=s.recvfrom(1024)
    data=data.decode()
    index=data.find(';')
    T2_x=int(data[:index])
    T2_y=int(data[index + 1:])
    T2=(T2_x,T2_y)
    M=decrypt(T2,C1,C2,C3)
    print("解密的明文为:",M)

    s.close()
    print("客户端已关闭")