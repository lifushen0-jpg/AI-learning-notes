#递归函数：在函数内部调用它自己
#条件：1.必须有明确的终止。  2.递归对解决问题有进展
def add(n):
    if n==1:
        return 1
    return n+add(n-1)
print(add(100))
def funa(n):
    if n<=1:
        return n
    return funa(n-1)+funa(n-2)
print(funa(10))
#有点：简洁， 更有思路      缺点：占内存，效率低
#闭包：1条件：   1，函数嵌套    2.内层函数使用外层函数的局部变量    3.外层函数的函数的返回值是内层函数的函数名
def outer(m):
    n=10
    def inner(w):
        print(n+m+w)
    return inner
outer(1)(2)
a=outer(10)
a(10)
#函数引用：函数名（），函数名保存了函数位置的引用
#每次开启内涵上都在使用同一份闭包变量
def outer1(m):
    print("outer's",m)
    def inner2(n):
        print("inner's",n)
        return m+n
    return inner2
ot=outer1(1)
print(ot(2))
print(ot(3))
#装饰器：1.不修改原函数代码    2.不改变函数或程序的调用
def test2():
    print("1919")
def test(fn):
    print("114")
    print("514")
    fn()
test(test2)