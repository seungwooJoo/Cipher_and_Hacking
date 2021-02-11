def makePattern(p):                  # 인자로 입력된 문장 p
    tmp = {}                          #문자에 부여한 번호를 임시로 저장하기 위한 사전 자료
    res = []                          # 패턴결과를 담을 리스트 자료
    index=0                            # 문자에 부여할 번호
    
    for c in p:                        #p문장의 알파벳 하나하나에 대하여 반복하겠음
        if c in tmp:                    # c가 tmp에 있으면,
            res.append(tmp[c])           #tmp[c]에 해당하는 번호를 res 리스트에 추가하라
        else:                            #c가 tmp 에  없으면,
            tmp[c] = str(index)        #tmp[c]에 index의 문자형을 넣는다. >> 'c' : '0'
            res.append(str(index))    #res리스트에 index의 문자형을 추가한다.
            index+=1
    return ';'.join(res)

def findPattern(msg,p):
    pattern = makePattern(p)        #알고 있는 문장인 p의 패턴을 저장한다
    blocksize = len(p)                #p의 블록사이즈를 계산해보고,
    pos = 0
    while True:
        data = msg[pos:pos+blocksize] #data는 블록사이즈 만큼의 암호문을 발췌해서 계속 볼것/
        if len(data) < blocksize:
            break
            
        ptrn = makePattern(data)
        if ptrn == pattern:
            return data
        pos+=1
        
if __name__ == '__main__':
    msg = '53%%#305))6*t4e26)4%='
    known_plaintext = ['goodglass', 'mainbranch']
    for p in known_plaintext:
        ret = findPattern(msg,p)
        print('[%s] = [%s]' %(p,ret))