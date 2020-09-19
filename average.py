#this functino takes the average of all the elements in a list
def average(l):
    ret = 0
    for i in l:
        ret += i
    ret /= len(l)
    return ret

print(average([3,2,5,6]))