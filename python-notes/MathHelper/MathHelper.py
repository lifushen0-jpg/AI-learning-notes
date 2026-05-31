class MathHelper:
    
    def PrimeNumber_judge(n):
        for i in range (2,int(n**0.5)+1):
            if n%i==0:
                return "这不是个素数"
        return "这是个素数"
    
    def PrimeNumber_search(n):
        list1=[]
        m=0
        if n==1:
            return f"没有小于{n}的素数"
        for x in range (2,n):
            z=0
            for y in range(2,int(x**0.5)+1):
                if x%y==0:
                    z=z+1
                    break
            if z==0:
                list1.append(x)
                m=m+1
        return f"{n}以内共有{m}个素数，他们是：\n{list1}"
    
    def ascending_order(list1):
        if type(list1)!=list:
            return "请输入列表"
        n=len(list1)
        list2=[]
        while len(list2)<n:
            j=list1[0]
            for i in list1:
                if i>j:
                    j=i
            list2.append(j)
            list1.remove(j)
        return list2
    
    def descending_order(list1):
        if type(list1)!=list:
            return "请输入列表"
        n=len(list1)
        list2=[]
        while len(list2)<n:
            j=list1[0]
            for i in list1:
                if i<j:
                    j=i
            list2.append(j)
            list1.remove(j)
        return list2
    
    def maximum(list1):
        if type(list1)!=list:
            return "请输入列表"
        j=list1[0]
        for i in list1:
            if i>j:
                j=i
        return j
    
    def minimum(list1):
        if type(list1)!=list:
            return "请输入列表"
        j=list1[0]
        for i in list1:
            if i<j:
                j=i
        return j
    
    def ascending_order_2(list1):
        n=len(list1)
        for i in range(1,n):
            key=list1[i]
            j=i-1
            while j>=0 and list1[j]>key:
                list1[j+1]=list1[j]
                j=j-1
            list1[j+1]=key
        return list1
    print(ascending_order_2([31, 1, 9, 26, 41, 8]))