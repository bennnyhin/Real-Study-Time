#this functino takes the average of all the elements in a list
def average(l):
    ret = 0
    for i in l:
        ret += i
    ret /= len(l)
    return ret

# given that n elements were used to create the old avg, the new average with the elemnt k too is:
def newAverage(oldAvg, n, k):
    return (oldAvg * n + k) / (n + 1)

print(newAverage(6, 2, 3))