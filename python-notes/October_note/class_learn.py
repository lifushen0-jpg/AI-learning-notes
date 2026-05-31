"""用于10.5的class学习"""
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
class Battery:
    """一次模拟电动汽车电瓶的简单尝试。"""

    def __init__(self, battery_size=75):
        """初始化电瓶的属性。"""
        self.battery_size = battery_size

    def describe_battery(self):
        """打印一条描述电瓶容量的消息。"""
        print(f"This car has a {self.battery_size}-kWh battery.")
    def get_range(self):
        """打印一条消息，指出电瓶的续航里程。"""
        if self.battery_size == 75:
              range = 260
        elif self.battery_size == 100:
              range = 315

        print(f"This car can go about {range} miles on a full char")
class ElectricCar(Car):
    """电动汽车的独特之处。"""

    def __init__(self, make, model, year):
        """
        初始化父类的属性。
        再初始化电动汽车特有的属性。
        """
        super().__init__(make, model, year)
        self.battery = Battery(100)       #在ElectricCar类中创建Battery实例

# my_tesla = ElectricCar('tesla', 'model s', 2019)
# print(my_tesla.get_descriptive_name())
# my_tesla.battery.describe_battery()
# my_tesla.battery.get_range()