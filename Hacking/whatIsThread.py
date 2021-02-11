# import time

# def longtime_job(a,b):
#     print('job start')
#     time.sleep(3)
#     print('job result [%d]' %(a*b))
    

# def main():
#     a,b=3,4
#     longtime_job(a,b)
#     print('**run main logic')
#     ret = a+b
#     print('main result [%d]' %ret)
    

# if __name__ == '__main__':
#     main()
    
    
import time
from threading import Thread

def longtime_job(a,b):
    print('job start')
   # time.sleep(3)
    print('job result [%d]' %(a*b))
    

def main():
    a,b=3,4
    t = Thread(target = longtime_job, args= (a,b))
    t.start()
    print('**run main logic')
    ret = a+b
    print('main result [%d]' %ret)
    

if __name__ == '__main__':
    main()
        
#두개 이상의 스레드로 구성된 프로세스를 멀티스레드 프로세스라 부른다.
#longtime_job()은 독립된 스레드에서 main()과는 따로 병렬적으로 동작하게 된다. 