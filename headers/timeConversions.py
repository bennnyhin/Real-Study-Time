# returns a list of hours, minutes, and seconds in s seconds respectively
def SToHMS(s):
    h = s // 3600
    s %= 3600
    m = s // 60
    s %= 60
    return [h, m, s]

def HMSToS(hms):
    return 3600 * hms[0] + 60 * hms[1] + hms[0]