import random
import time

import sm3



def Rho_attck(n):
    h = random.randint(0,2**64)
    h=hex(int(h))[2:]
    #print(type(h))
    #print(h)
    attack_table = {}
    while True:
        # 生成消息
        h_hash = sm3.hash(h)
        # 取前n个bit
        check_hash = h_hash[:n // 4]
        if check_hash in attack_table:
            # 找到碰撞
            original_message = attack_table[check_hash]
            print("碰撞消息1：", original_message)
            print("碰撞消息2：", h)
            print("哈希值：", h_hash)
            break
        else:
            # 没碰撞就存表
            attack_table[check_hash] = h
        # 更新h
        h = h_hash
    return


if __name__ == "__main__":
    n = int(input("需要碰撞多少bit的数据："))
    start_time = time.time()
    for i in range(5):
        Rho_attck(n)
    end_time = time.time()
    #取五次平均值
    time = (end_time - start_time) / 5
    print("平均用时：", time, "s")
