#1.装饰器，本质上是个闭包函数，在不修改原有函数基础上更改功能
def outer(x):
    def inner():
        x()
        print("登录")
    return inner
#2.语法糖。格式：@装饰器名
@outer
def t():
    print("114514")
t()
#被装饰的函数与装饰器内函数的形参相同
def outer1(fn):
    def inner2(name):
        print(f"{name}")
        fn(name)
    return inner2
@outer1
def func(name):
    print(114514)
func("451")

ot=outer1(func)
ot("514")