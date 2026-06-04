#while True:
#    print("Hello world")
#陷入循环后，在IDLE的交互式环境窗口中，只有两种办法停止这个程序：按下Ctrl-C或从菜单中选择ShellRestart Shell。
print("hello",end="")
print("world")
#这两个字符串出现在独立的两行中，因为print()函数自动在传入的字符串末尾添加了换行符。但是，可以设置end关键字参数，将它变成另一个字符串。
print("dogs","brids","mice",sep=" , ")
#你可以传入sep关键字参数，替换掉默认的分隔字符串。
def func(divideBy):
    try:
        n=42//divideBy
        if n:
            return "It is a factot of 42"

    except :
        return "You can not dividBy zero"
print(func(114))
print(func(0))
print(func(3))
#错误可以由try和except语句来处理。那些可能出错的语句被放在try子句中。如果错误发生，程序执行就转到接下来的except子句开始处。
#except块用于捕获和处理在try块中发生的异常。你可以指定要捕获的特定异常类型，或者使用通用的except来捕获所有异常。
#一旦执行跳到except子句的代码，就不会回到try子句。它会继续照常向下执行。