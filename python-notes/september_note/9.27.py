spam = ['cat', 'bat', 'rat', 'elephant']  #这是个列表
print(spam[-1])
print(spam[1:3])
print(spam[0:-2])
a=["x","Y","Z"]
b=[1,2,3,4]
print(a+b)
test=[1,2,3,4,5,6]  # 链接列表
del test[2]   #从0开始计数
print(test)
test=[1,2,3,4,5,6]
print(test.index(2))    #查找元素是否在列表中，找到返回编号，否则报错
try:
    print(test.index(114))
except:
    print("不可以这样")

test=[1,2,3,4,5,6]
print(test.pop())    #输出被删除元素
test.pop()     #删除元素，括号内为空删除最后一个，有数字删除对应编号元素
print(test)

test=[1,2,3,4,5,6]
print(test.pop(4))
test.pop(4)
print(test)

test=[1,2,3,4,5,6]
print(test.append(7))    #无意义 
test.append(7)        #在列表末尾追加一个元素
print(test)

test=[1,2,3,4,5,6]    #移除特定的值    
test.remove(3)
print(test)

test=[1,2,3,4,5,6]      #在指定位置插入元素，其后元素依次后延
print(test.insert(1,8))     #无意义
test.insert(1,8)
print(test)

#print以内的方法依然会生效
test=[3,2,8,6,7]    
test.sort()    #对原列表内的元素进行排序，按字母表顺序或数字大小升序排列
print(test)
test=['bmw', 'audi', 'toyota', 'subaru']
test.sort()
print(test)
try:
    test=[2,1,"car"]    #列表中不能同时有数字和字符串
    test.sort()
    print(test)
except:
    print("这样不行")
test=['bmw',"曹操", '李','audi', 'toyota',"滋养", 'subaru','1',"14"]   #字符串排序，数字在最前，其次是英文，其次中文
test.sort()
print(test)

test=['bmw', 'audi','toyota', 'subaru',]
test.sort(reverse=True)   #倒叙排列
print(test)

test=['bmw', 'audi' ,'toyota', 'subaru',]
print(sorted(test))   #使用函数排序不改变原列表
print(test)

test=[1,2,3,4,5,6]  #列表
test1=test[:]   #复制列表
print(test1)
test1.pop()
test.append(7)   #两者拥有不同命名空间
print(test)
print(test1)

test=[1,2,3,4,5,6]
test2=test
test.append(8)
test2.remove(1)
print(test)  
print(test2)  #两者拥有相同的命名空间