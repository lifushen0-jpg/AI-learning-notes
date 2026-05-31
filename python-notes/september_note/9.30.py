# test=(1,2,3,4)          #这是个元组
# print(test)
# print(test[2])
# try:
#     test[1]=10
# except:
#     print("元组中的值不可修改")

# # break只退出当前所在的循环，不会影响外层循环
# for i in range(3):
#     print(f"外层循环: i = {i}")
#     for j in range(5):
#         print(f"  内层循环: j = {j}")
#         if j == 2:
#             print("   跳出内层循环")
#             break
#         print("这里不会执行")
#     print("这里会执行")


# import prime_number
# print(prime_number.judge(91))
# print(prime_number.judge(97))
# print(prime_number.search(100))

# print("hello\nworld")             #反斜杠以换行
# print('hello \\n world')          #双\\输出\n
# print(r'hello\nworld')            #或者使用r" "

# requested_toppings = ["salt"]    
# if requested_toppings:              #检测是否非空，若非空，执行下级代码。
#     for requested_topping in requested_toppings:
#           print(f"Adding {requested_topping}.")
#     print("\nFinished making your pizza!")
# else:
#     print("Are you sure you want a plain pizza?")