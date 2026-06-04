import random
#the function random 
seq=[1,2]
nums1=[]
nums2=[]
for i in range(20):
    num1=random.choice(seq)
    num2=random.randint(2,10)    #You must input the start number and the last number
    nums1.append(num1)
    nums2.append(num2)
print(nums1)
print(nums2)

cards=["Q",'K',"J"]
random.shuffle(cards)
print(cards)


import statistics
seq=[1,2,3,4,5,6]
print(statistics.mean(seq))


import sys
print(sys.modules.keys())  # 查看所有已加载的模块
print('os' in sys.modules)  # True

#Class:
class Dog:
    """一次模拟小狗的简单尝试。"""   #class or function 定义以后可以用三重引号添加注释
    def __init__(self, name, age):
        """初始化属性name和age。"""
        self.name = name
        self.age = age
    def sit(self):
        """模拟小狗收到命令时蹲下。"""
        print(f"{self.name} is now sitting.")
    def roll_over(self):
        """模拟小狗收到命令时打滚。"""
        print(f"{self.name} rolled over!") 
my_dog = Dog('Willie', 6)
your_dog = Dog('lucy',3)

print(f"My dog's name is {my_dog.name}.")
print(f"My dog is {my_dog.age} years old.")
my_dog.sit()
my_dog.roll_over()
print(f"your dog {your_dog.name} is {your_dog.age} years old")
your_dog.sit()
your_dog.roll_over()


#课本习题
class User:
    def __init__(self,first_name,last_name,phone_number):
        self.first_name=first_name
        self.last_name=last_name
        self.phone_number=phone_number
    def describe_uesr(self):
        print(f"该用户的名字是{self.first_name}{self.last_name},/n联系方式为{self.phone_number}")
    def greet_user(self):
        print(f"用户{self.first_name}，您好")

user1=User("Li","fushen",114514)
user2=User("Liu","Aihua",1919810)

user1.describe_uesr()
user2.greet_user()
