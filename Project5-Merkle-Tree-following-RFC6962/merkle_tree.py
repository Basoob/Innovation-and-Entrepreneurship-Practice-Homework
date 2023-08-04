import hashlib
import math
import time
class node:
    def __init__(self,left_child,right_child,level,value):

        self.left_child = left_child
        self.right_child=right_child
        self.level=level
        self.value=value



def cal_hash(data):
    sha256 = hashlib.sha256()
    sha256.update(data.encode('utf-8'))
    return sha256.hexdigest()


def merkle_tree(data):
    leaf_nodes = []
    # 计算树深度
    level = int(math.log(len(data), 2)) + 1
    # 计算哈希值并创建叶节点
    for item in data:
        hash_value = cal_hash(item)
        new_node=node(None,None,level,hash_value)
        leaf_nodes.append(new_node)

    nodes = leaf_nodes
    level=level-1
    #构建默克树
    while len(nodes) > 1:
        new_level_nodes = []
        #当节点数量为奇数时，复制最后一个节点并插入到这层节点末尾
        if len(nodes) % 2 != 0:
            nodes.append(nodes[-1])

        #构建上一层的节点
        for i in range(0, len(nodes), 2):
            combined_hash = cal_hash(nodes[i].value + nodes[i + 1].value)
            last_node=node(nodes[i],nodes[i+1],level,combined_hash)
            new_level_nodes.append(last_node)

        nodes = new_level_nodes
        level = level - 1

    merkle_root = nodes[0]
    return merkle_root
#打印
def print_tree(root):
    if root==None:
        return
    print(root.value, ";", root.level)
    print_tree(root.left_child)
    print_tree(root.right_child)


start=time.time()
data = ['item']*1000
merkle_root = merkle_tree(data)
print("Merkle Root:", merkle_root)
print("1000个节点的Merkel Tree已生成")
end=time.time()
totaltime=end-start
print("用时",totaltime,"s")
print("整棵树递归打印为：")
print_tree(merkle_root)

