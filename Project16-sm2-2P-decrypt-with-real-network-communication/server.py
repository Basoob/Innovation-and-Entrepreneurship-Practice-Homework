import sm2
import socket
import random

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
def generate_T2(d2,T1):
    d2_inv=pow(d2,-1,n)
    T2=sm2.mul(p,T1[0],T1[1],d2_inv)
    return T2

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
    #利用p1和d2生成公钥P
    d2, P = generate_K_P(P1)
    data=str(P[0]) + ';' + str(P[1])
    s.sendto(data.encode(),addr)

    #发送T2
    data,addr=s.recvfrom(1024)
    data=data.decode()
    print("已接收data-T1")
    index = data.find(';')
    T1_x = int(data[:index])
    T1_y = int(data[index + 1:])
    T1 = (T1_x, T1_y)
    T2=generate_T2(d2,T1)
    data = str(T2[0]) + ';' + str(T2[1])
    print("已发送data-T2")
    s.sendto(data.encode(),addr)

    s.close()
    print("服务端已关闭")