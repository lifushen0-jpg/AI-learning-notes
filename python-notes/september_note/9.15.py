#zip()的应用
li=[1,2,3]
lis=['a','b']
for i in zip(li,lis):
    print(i)
li=[1,2,3]
lis=['a','b','c']
for i in zip(li,lis):
   print(i)


#map()的应用
li=[1,2,3]
def funa(x):
    return x*5
mp= map(funa,li)
print(list(mp))


#reduce（）的应用
from functools import reduce
li=[1,2,3,4]
def add(x,y):
    return x*y
z=reduce(add,li)
print(z)

#sum()的应用
li=[1,2,3,4]
print(sum(li))

#拆包
tua=(1,2,3,4)
a,b,c,d=tua
x,*y=tua
print(a,b,c,d)
print(x,y)