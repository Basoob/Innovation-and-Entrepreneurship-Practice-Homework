import sm2
import socket
import random
import time
# SM2参数
p = int("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF", 16)
a = int("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC", 16)
b = int("28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93", 16)
n = int("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123", 16)
G_x = int("32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7", 16)
G_y = int("BC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0", 16)

def inverse(a_x,a_y):
    a_inv_x = a_x
    a_inv_y=p - a_y
    #print("x:",a_inv_x)
    #print("y",a_inv_y)
    return a_inv_x,a_inv_y

def generate_K_P(P1):
    d2 = random.randint(1, n - 1)
    temp1=pow(d2, -1, n)
    temp2 = sm2.mul(p, P1[0], P1[1], temp1)
    G_inv_x,G_inv_y=inverse(G_x,G_y)
    #print(G_inv_x)
    #print(G_inv_y)
    P = sm2.add(p,temp2[0],temp2[1],G_inv_x,G_inv_y)
    return d2, P


def generate_r_s2_s3(Q1,d2,e):
    e = int(e, 16)
    k2 = random.randint(1, n - 1)
    Q2 = sm2.mul(p, G_x, G_y, k2)
    k3 = random.randint(1, n - 1)
    temp1=sm2.mul(p, Q1[0], Q1[1], k3)
    temp2 = sm2.add(p,temp1[0],temp1[1],Q2[0],Q2[1])
    x1=temp2[0]
    y1=temp2[1]
    r = (x1 + e) % n
    if r == 0:
        return None
    s2 = d2 * k3 % n
    s3 = d2 * (r + k2) % n
    return r, s2, s3

if __name__ == "__main__":

    # 建立连接
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', 12345))
    print("服务端连接已就位...")

    #接收P1
    data, addr = s.recvfrom(1024)
    print("已接受信息data-P1...")
    data = data.decode()
    index = data.find(';')
    P1_x=int(data[:index])
    P1_y=int(data[index+1:])
    P1 = (P1_x,P1_y)
    d2, P = generate_K_P(P1)

    #接收Q1和e
    data, addr = s.recvfrom(1024)
    print("已接收data...")
    data = data.decode()
    index1 = data.find(';')
    index2 = data.find(';',index1+1)
    #print("index1",index1)
    #print("index2", index2)
    Q1_x=int(data[:index1])
    Q1_y=int(data[index1+1:index2])
    Q1 = (Q1_x,Q1_y)
    e = data[index2+1:]
    r, s2, s3 = generate_r_s2_s3(Q1,d2,e)
    #编辑信息data=r+s2+s3
    data = str(r) + ';' + str(s2) + ';' + str(s3)
    print("发送信息data-r+s2+s3:", data)
    s.sendto(data.encode(), addr)
    s.close()
    print("服务端已关闭")