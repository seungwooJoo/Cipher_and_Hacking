def frequency_analysis(msg):
    fa = {}
    for c in msg:
        if c in fa:
            fa[c] +=1
        else :
            fa[c] = 1
    print(sorted(fa.items(), key = lambda x : x[1] , reverse = True))
    
if __name__ == '__main__':
    msg = '33783478urh#*&u@*yrf#i#@ruru@rf#@rfru'
    frequency_analysis(msg)