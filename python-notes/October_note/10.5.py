#给属性添加默认值
class Car:
    def __init__(self, make, model, year):
          """初始化描述汽车的属性。"""
          self.make = make
          self.model = model
          self.year = year
          self.odometer_reading = 0
          self.gas_tank = 100

    def get_descriptive_name(self):
        """返回整洁的描述性信息。"""
        long_name = f"{self.year} {self.make} {self.model}"
        return long_name.title()
    def read_odometer(self):
          """打印一条指出汽车里程的消息。"""
          print(f"This car has {self.odometer_reading} miles on it.")

    def update_odometer(self, mileage):   #通过创建方法改变默认值，实现更多功能。
        """
        将里程表读数设置为指定的值。
        禁止将里程表读数往回调。
        """
        if mileage >= self.odometer_reading:
              self.odometer_reading = mileage
        else:
             print("You can't roll back an odometer!")
        self.odometer_reading = mileage
    def increment_odometer(self, miles):
        """累计行走里程"""
        self.odometer_reading += miles
    def fill_gas_tank(self):
         print(f"This car has a {self.gas_tank}L gas tank")
my_new_car = Car('audi', 'a4', 2019)
print(my_new_car.get_descriptive_name())
my_new_car.read_odometer()
my_new_car.fill_gas_tank()

my_new_car.odometer_reading = 23   #直接重新赋值
my_new_car.read_odometer()

my_new_car.update_odometer(23)
my_new_car.read_odometer()

my_used_car = Car('subaru', 'outback', 2015)
print(my_used_car.get_descriptive_name())
my_used_car.update_odometer(23500)
my_used_car.read_odometer()
my_used_car.increment_odometer(100)
my_used_car.read_odometer()

#子类
class ElectricCar(Car):  #()内存放父类名称
    """电动汽车的独特之处。"""

    def __init__(self, make, model, year):   #接收父类信息
        """初始化父类的属性。"""
        super().__init__(make, model, year)   #super()函数可以调用父函数的方法
                                              #此处方法__init__()让ElectricCar实例包含这个方法中定义的所有属性
        self.battery_size = 75
    def describe_battery(self):
        """打印一条描述电瓶容量的消息。"""
        print(f"This car has a {self.battery_size}-kWh battery.")
    def fill_gas_tank(self):          #重写父类的方法：创建同名的类
        """电动汽车没有油箱。"""
        print("This car doesn't need a gas tank!")

my_tesla = ElectricCar('tesla', 'model s', 2019)
print(my_tesla.get_descriptive_name())
my_tesla.describe_battery()
my_tesla.fill_gas_tank()

from class_learn import Car
my_new_car = Car('audi', 'a4', 2019)
print(my_new_car.get_descriptive_name())

import class_learn

my_tesla = class_learn.ElectricCar('tesla', 'model s', 2019)
print(my_tesla.get_descriptive_name())
my_tesla.battery.describe_battery()
my_tesla.battery.get_range()