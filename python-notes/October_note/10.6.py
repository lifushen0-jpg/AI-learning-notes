import os
print("当前工作目录：", os.getcwd())   #确认vscode的工作目录

"""对文件的操作"""
# #要以任何方式使用文件，那怕仅仅是打印其内容，都得先打开文件，才能访问它
with open('d:\\python_learn\\October_note\\number2.txt') as file_object:  #打开文件,指定绝对路径以防python找不到文件
    contents = file_object.read()   #以字符串形式储存
print(contents)
print(type(contents))     
filename = "pi_digits.txt"   #注意，这样做需要打开的文件在VSCode的工作目录下，而非文件同目录

with open(filename) as file_object:
    for line in file_object:
        print(line.rstrip())     #文本末有一个看不见的换行符，print自动再加一个换行符，可使用rstrip()取消一次换行  

filename = "pi_digits.txt"
with open(filename) as file_object:
    lines = file_object.readlines()   #以列表形式储存
# print(lines)
# for line in lines:
#     print(line.rstrip())

pi_string = ''
for line in lines:
      pi_string += line.rstrip()    #这样输出的字符串会保留每行左边的空格
print(pi_string)
print(len(pi_string))
pi_string = ''
for line in lines:
     pi_string += line.strip()    #使用strip()以删除空格
print(pi_string)
print(len(pi_string))

filename = 'd:\\python_learn\\October_note\\programming.txt'

with open(filename, 'w') as file_object:   #第二个实参'w'表示写入模式
#打开文件时，可指定读取模式（'r'）、写入模式（'w'）、附加模式'a'）或读写模式（'r+'）。如果省略了模式实参，Python将以默认的只读模式打开文件。
#警告！以写入模式（'w'）打开文件时千万要小心，因为如果指定的文件已经存在，Python将在返回文件对象前清空该文件的内容。
    file_object.write("I love programming.")
    file_object.write("I love creating new games.")   #写入文本时python不会主动换行，需要自己添加换行符\n

with open(filename) as file_object:
    contents = file_object.read()
print(f"未加换行符内容为：\n{contents}")

with open(filename, 'w') as file_object:  
    file_object.write("I love programming.\n")
    file_object.write("I love creating new games.\n")   

with open(filename) as file_object:
    contents = file_object.read()
print(f"加入换行符后内容为：\n{contents}\n此外，以写入模式打开文件删除了第一次写入的内容")
#附加模式可在原有内容基础上追加内容
with open(filename, 'a') as file_object:
    file_object.write("I also love finding meaning in large datasets.\n")
    file_object.write("I love creating apps that can run in a browser.")

#practice:
filename = 'd:\\python_learn\\October_note\\practice_feedback.txt'
with open(filename, "w", encoding="utf-8") as file_object:
    file_object.write("以下为用户反馈\n")
terminator=True
feedbacks=[]
while terminator:
    feedback=input("Please share you feel about using our product:  ")
    feedbacks.append(feedback)
    n=input("Is there other users?")
    if n=="yes":
        continue
    else:
        terminator=False
with open(filename,"a") as file_object:
    for line in feedbacks:
        file_object.write(f"{line}\n")
