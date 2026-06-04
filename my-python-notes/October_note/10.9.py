import numpy as np
import array
import time
# Python 提供了几种将数据存储在有效的、固定类型的数据缓存中的选项。内置的数组（array）模块可以用于创建统一类型的密集数组
L=list(range(10))
A=array.array('i',L)  #这里的 'i'是一个数据类型码，表示数据为整型
print(A)
print(np.array([1,4,6,5,4]))
print(np.array([10,2.1,3.14,40]))  #Numpy要求数据类型相同，否则会向上转换（若可行），这里整型被转换为浮点型
print(np.array([1, 2, 3, 4], dtype='float32'))   #如果希望明确设置数组的数据类型，可以用 dtype关键字：
print(np.array([range(i,i+3) for i in [2,4,6]]))
# 创建一个长度为10的数组，数组的值都是0
print(np.zeros(10, dtype=int))

# 创建一个3×5的浮点型数组，数组的值都是1
print(np.ones((3, 5), dtype=float))

# 创建一个3×5的浮点型数组，数组的值都是3.14 
print(np.full((5,3),3.14))

# 创建一个浮点数组，从0到20，间隔2
print(np.arange(0,20,2))

# 创建从0到1的5项等差数列
print(np.linspace(0,1,5))

# 创建从0到1的均匀随机数列
print(np.random.random(3))   #以整形n输入，生成一个n元列表
print(np.random.random((4,3)))   #以元组(4,3)输入，生成一个3*4矩阵

# 创建均值为0，方差为4的正态分布随机数列
print(np.random.normal(0,1,10))    #第三个元素以整形n输入，生成一个n元列表
print(np.random.normal(0,1,(5,3)))    #第三个元素以元组(4,3)输入，生成一个3*4矩阵

# 创建随即整形列表
print(np.random.randint(0,4,5))   #以整形n输入，生成一个n元列表
print(np.random.randint(0,4,(4,3)))   #以元组(4,3)输入，生成一个3*4矩阵

# 创建单位矩阵
print(np.eye(4))

# 一个求随机数程序
np.random.seed(0)
def compute_reciprocals(values):
    output = np.empty(len(values))
    for i in range(len(values)):
         output[i] = 1.0 / values[i]
    return output
values = np.random.randint(1, 10, size=5)
print(values)
print(compute_reciprocals(values))

start = time.time()
big_array = np.random.randint(1, 100, size=100000000)
end = time.time()
print(f'程序运行了{end - start}秒')

np.random.seed(0)  # 设置随机数种子
x1 = np.random.randint(10, size=6)  # 一维数组
x2 = np.random.randint(10, size=(3, 4))  # 二维数组
x3 = np.random.randint(10, size=(3, 4, 5))  # 三维数组
x4 = np.random.randint(10,size=(3,4,5,6))
print(f'这是一维数组\n{x1}')
print(f'这是二维数组\n{x2}')
print(f'这是三维数组\n{x3}')
print(f'这是四维数组\n{x4}')
# 每个数组属性：nidm（数组的维度）、shape（数组每个维度的大小）和size（数组中总数字数）
print("x3 ndim: ", x3.ndim)
print("x3 shape:", x3.shape)
print("x3 size: ", x3.size)
# 另外一个有用的属性是 dtype，它是数组的数据类型
print("x3 dtype:", x3.dtype)
# 其他的属性包括表示每个数组元素字节大小的 itemsize ，以及表示数组总字节大小的属性 nbytes
print("itemsize:", x3.itemsize, "bytes")
print("nbytes:", x3.nbytes, "bytes")
# 一维数组可用同列表的方式查取元素，多维数组可用对应坐标查取[行数-1,列数-1]
print(x1)
print(x1[3])
print(x2)
print(x2[0,1])  
