import pytest1
#抛出异常   1.创建Excepton("xxx")对象，xxx为异常提示信息    2.raise抛出提示信息
#抛出异常之后，后面的代码不再执行
def bug():
    raise Exception("bug")
#捕获异常：遇到异常后继续执行,需要在可能出现异常的代码上一级使用
try:
    print(bug())
except Exception as e:
    print(e)
#模块：一个py文件就是一个模块
#1.内置模块，如random,time,os,logging
#2.第三方模块，下载：cmd窗口（win+r，输入cmd）输入pip install模块名
#3.自定义，注意明明要遵循标识符规定及变量命名，不要与内置命名冲突，否则将导致无法使用
#导入模块：  #improt 模块名     或     from 模块名  import  功能名
#调用功能：模块名.功能名    或        功能
#as : 起别名   import 模块名  as  别名
#内置全局变量  __name__   语法：if __name__ == "__main__":   作用：控制py文件
pytest1.test()
#包：项目结构中的文件夹/目录，其中含有__init__.py文件，将有联系的文件组合起来，避免模块名冲突
#导入包时，先执行__init__.py文件
#导入方式
from pack_test1 import py_pack_test
py_pack_test.test()
#__all__:本质上是个列表，可以控制引入的东西