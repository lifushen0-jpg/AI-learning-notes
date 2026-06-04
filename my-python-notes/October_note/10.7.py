def AscendingList_merge_v1(list1,list2):
    result=[]
    if len(list1) < len(list2):
        list1,list2=list2[:],list1[:]
    list3=list1[:]
    for i in range(len(list2)):
        if list3[i] > list2[i]:
            list1.insert(2*i,list2[i])
        else:
            list1.insert(2*i+1,list2[i])
    return list1
print(AscendingList_merge_v1([1,3,4,5,9],[2,6,7,8,10,11]))

