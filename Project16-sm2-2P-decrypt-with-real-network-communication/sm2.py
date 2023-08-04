from random import randint
from hashlib import sha256
from hmac import HMAC
# SM2参数
p = int("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF", 16)
a = int("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC", 16)
b = int("28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93", 16)
n = int("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123", 16)
G_x = int("32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7", 16)
G_y = int("BC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0", 16)
# 定义RFC6979中所需的常量
q_hex = "FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF"
q = int(q_hex, 16)
hmac_hash = sha256

# 有限域上的加法
def add(p, x1, y1, x2, y2):
    if x1 == x2 and (y1 == -y2 % p or (y1 == 0 and y2 == 0)):
        return (None, None)
    elif x1 == None:
        return (x2, y2)
    elif x2 == None:
        return (x1, y1)

    if x1 == x2 :
        s = (((3 * x1 * x1 + a)%p) * pow(2 * y1, -1, p)) % p
    else:
        s = ((y1 - y2) * pow(x1 - x2, -1, p)) % p

    x3 = (s * s - x1 - x2) % p
    y3 = (s * (x1 - x3) - y1) % p
    return (x3, y3)

# 有限域上的乘法
def mul(p, x1, y1, n):
    if x1 is None:
        return None
    x = x1
    y = y1
    n = bin(n)[2:]

    for i in range(1,len(n)):
        x, y = add(p, x, y, x, y)
        if n[i]=='1':
            x,y = add(p, x, y, x1, y1)

    return (x,y)
#生成确定性随机数k以满足RFC6979
def generate_k(private_key, message):
    v = b'\x01' * 32
    k = b'\x00' * 32
    d = bytearray.fromhex(private_key.zfill(64))
    m = bytearray.fromhex(message.hex())

    while True:
        k = HMAC(k, v + b'\x00' + d + m, hmac_hash).digest()
        v = HMAC(k, v, hmac_hash).digest()
        k_int = int.from_bytes(k, "big")
        if 1 <= k_int <= q - 1:
            break

    return hex(k_int).lstrip("0x").rstrip("L").zfill(64)
if __name__ == "__main__":
    # 生成私钥d
    d = randint(1, n - 1)
    # 生成公钥P
    print(d)
    P = mul(p, G_x, G_y, d)

    # 生成消息摘要
    msg = input("请输入消息：").encode("utf-8")
    print(type(msg))
    hash_msg = sha256(msg).hexdigest()
    d_hex = hex(d)[2:]  # 移除前缀
    print(d_hex)
    random_k = generate_k(d_hex, msg)
    random_k = int(random_k, 16)
    print("Random number k:", random_k)
    # 签名
    e = int(hash_msg, 16)
    r = s = 0
    while r == 0 or s == 0:
        k = randint(1, n - 1)
        C = mul(p, G_x, G_y, k)
        r = (e + C[0]) % n
        if r == 0:
            continue
        s = (pow((1 + d), -1, n) * (k - d * r)) % n
    print("r:", r)
    print("s:", s)

    # 验证签名
    t = (r + s) % n
    valid = False
    e = int(hash_msg, 16)
    if t != 0:
        GA = mul(p, G_x, G_y, s)
        PA = mul(p, P[0], P[1], t)
        X = add(p, GA[0], GA[1], PA[0], PA[1])
        R = (e + X[0]) % n
        if R == r:
            valid = True

    # 输出结果
    print("公钥：")
    print("x =", hex(P[0])[2:].upper())
    print("y =", hex(P[1])[2:].upper())
    print("签名结果：")
    print("r =", hex(r)[2:].upper())
    print("s =", hex(s)[2:].upper())
    print("验证结果：", valid)
