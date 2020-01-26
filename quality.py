def ToRome(num):
    pattern = ["","0","00","000","01","1","10","100","1000","02"]
    rome = ["I","V","X","L","C","D","M","",""]
    #num = int(input())
    output=""
    i = 0
    if(num<4000):
        while(10**i<=num):
            dig = int(num / (10**i)) % 10
            dig = pattern[dig]
            dig = dig.replace("0",rome[i*2])
            dig = dig.replace("1",rome[i*2+1])
            dig = dig.replace("2",rome[i*2+2])
            output=dig + output
            i=i+1
    else:
        raise Exception("illegal input!")
    return output
