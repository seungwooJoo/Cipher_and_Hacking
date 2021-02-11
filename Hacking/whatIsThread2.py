# import time
# from threading import Thread

# answer = 0

# def longtime_job(a,b):
#     global answer  #전역변수를 사용한다는 의미
#     print('++JOB START')
#     time.sleep(5)
#     answer = a*b
#     print('++JOB RESULT [%d]' %answer)
    
# def main():
#     a,b = 3,4
#     t = Thread(target = longtime_job, args=(a,b))
#     t.start()
#     print('**RUN MAIN LOGIC')
#     tmp = a+b
#     final = answer + tmp
#     print('FINAL RESULT [%d]' %final)
    
# if __name__ == '__main__':
#     main()
    
#longtime_job()이 작업을 끝내기 못한 상태에서 main()의 final = answer+tmp를 수행해버려 12가 결과로 나온것이다.
#따라서 제대로 된 결과를 위해서는 스레드로 구동한 longtime_job()이 끝날때까지 기다려줘야 한다. 
#특정 스레드가 종료될 때까지 기다리기 위해 Thread.join()을 이용한다.

import time
from threading import Thread

answer = 0

def longtime_job(a,b):
    global answer  #전역변수를 사용한다는 의미
    print('++JOB START')
    time.sleep(5)
    answer = a*b
    print('++JOB RESULT [%d]' %answer)
    
def main():
    a,b = 3,4
    t = Thread(target = longtime_job, args=(a,b))
    t.start()
    print('**RUN MAIN LOGIC')
    tmp = a+b
    
    t.join()  #스레드 t가 종료할 떄까지 기다림
    
    final = answer + tmp
    print('FINAL RESULT [%d]' %final)
    
if __name__ == '__main__':
    main()