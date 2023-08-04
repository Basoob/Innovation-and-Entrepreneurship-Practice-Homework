import sm3
import time

start=time.time()
#原明文
message = '202100460115'
print('原明文为',message)
print('原哈希值为',sm3.hash(message))
#扩展信息
extend = '20030811'
print("拓展信息为",extend)
padding_msg=sm3.padding(message)
attack_msg=padding_msg+extend
#最后64bit要表示的长度
lenth_attack_msg=len(attack_msg)*4
#print(len(padding_msg))
print("padding_msg:",padding_msg)
#拓展信息开始填充，‘8’=‘1000’
attack_msg=attack_msg+'8'
lenth_0 = 112- (len(attack_msg) % 128)
#开始填充0
attack_msg = attack_msg + '0'*lenth_0
#在最后64bit填充长度
padiing_length = '{:016x}'.format(lenth_attack_msg)
padding_attack_msg=attack_msg+padiing_length
#print(len(padding_attack_msg))
print("新消息为:", padding_attack_msg)
print("新消息的哈希值为:", sm3.hash(padding_attack_msg))
end=time.time()
totaltime=end-start
print("用时",totaltime,"s")

