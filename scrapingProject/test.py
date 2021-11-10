from tasks import add

add.delay(1,2) # 비동기 실행
add.apply_async(args(1,2), eta='언제시작 오늘부터 +일 시간 분') # 비동기 실행 예약
add.apply_async(args(1,2), link='other task') # 다른 task과 링크도 가능
print(type(add))
for i in range(10):
    print(add(0,i))
