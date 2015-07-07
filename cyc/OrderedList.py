
def findn(list, item, lo, hi):
  
    if hi-lo == 1:
        if abs(list[hi] - item) < abs(list[lo] - item):
            return hi
        return lo
    mid = (hi+lo)/2
    if item < list[mid]:
        return findn(list,item,lo, mid)
    return findn(list,item,mid, hi)


def FindNearest(List,Item):
    """ pre: len(List) >0, (List[i] - Item) is valid for i[0..len(List)-1]
       post: returns index of the item in list nearest to Item"""


    
    return findn(List, Item, 0, len(List)-1)
    

def insert(list,item,left,right): # recursive search and insert
    if item <= list[left]:
        list.insert(left,item)
    elif item >= list[right]:
        list.insert(right+1, item)
    else:
        mid = (left + right) /2
        if item > list[mid]:
            insert(list,item,mid,right-1)
        else:
            insert(list,item,left+1,mid)

def Insert(List,Item):
    """ pre: List is ordered or empty, (Item > List[i], Item < List[i]) valid for i[0..len(List)-1]
       post: Item inserterd in order into list """
        



    lenlist = len(List)
    if lenlist==0:
        List.insert(0,Item)
    else:
        insert(List,Item,0,lenlist-1)
    
#
