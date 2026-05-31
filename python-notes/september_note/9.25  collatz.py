try :
    n = int(input("Please input start number"))
except:
    print("你必须输入一个整数")
m=0
while n!=1:
    if n%2==1:
        if n==1:
            print(n)
            break
        n=3*n+1
        print(n)
    else:
        if n/2==1:
            print(int(n/2))
            break
        n=int(n/2)
        print(n)
    m+=1
print(f"共执行了{m}步")