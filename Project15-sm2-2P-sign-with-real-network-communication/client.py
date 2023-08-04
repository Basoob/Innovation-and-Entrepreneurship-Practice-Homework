# client
import sm2
import socket
import random
import sm3
import time

# SM2参数
p = int("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF", 16)
a = int("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC", 16)
b = int("28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93", 16)
n = int("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123", 16)
G_x = int("32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7", 16)
G_y = int("BC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0", 16)


def generate_K_P1():
    #私钥d1
    d1 = random.randint(1, n - 1)
    temp = pow(d1,-1, n)
    P1 = sm2.mul(p,G_x,G_y,temp)
    return d1, P1


def generate_Q1_e(Z, M):
    M_ = bytes(Z + M, encoding='utf-8')
    #print("M_", M_)
    M_=M_.decode()
    print("M_",M_)
    hex_M_ = ''.join(hex(ord(c))[2:] for c in M_)
    print("hex_M_",hex_M_)
    e = sm3.hash(hex_M_)
    k1 = random.randint(1, n - 1)
    Q1 = sm2.mul(p,G_x,G_y,k1)
    return k1, Q1, e


def Sign(d1, k1, s2, s3, r):
    s = ((d1 * k1) * s2 + d1 * s3 - r) % n
    if s != 0 or s != (n - r):
        return (r, s)
    else:
        return None

if __name__ == "__main__":
    # 建立连接
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("客户端已连接")
    address= ("127.0.0.1", 12345)
    #生成d1和P1
    d1, P1 = generate_K_P1()
    #发送P1
    data = str(P1[0]) + ';' + str(P1[1])
    print("发送信息data:", data)
    s.sendto(data.encode(),address )


    #Z和M
    client_id = 'client'
    server_id = 'server'
    Z = client_id + server_id
    M = input("massage:")
    k1, Q1, e = generate_Q1_e(Z, M)
    data = str(Q1[0]) + ';' + str(Q1[1]) + ';' + e
    print("发送信息data:",data)
    s.sendto(data.encode(), address)

    #开始签名
    data, addr = s.recvfrom(1024)
    data = data.decode()
    print("已接收data...")
    index1 = data.find(';')
    index2 = data.find(';', index1 + 1)
    #print("index1", index1)
    #print("index2", index2)
    r = int(data[:index1])
    s2 = int(data[index1+1:index2])
    s3 = int(data[index2+2:])
    signature = Sign(d1, k1, s2, s3,r)
    print("签名:", signature)

    s.close()
    print("客户端已关闭")