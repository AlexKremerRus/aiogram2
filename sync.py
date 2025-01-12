import time


def send_mail(num):
    print(f'Улетело сообщение {num}')
    time.sleep(1)  # Имитация отправки сообщения по сети
    print(f'Сообщение {num} доставлено')


def main():
    for i in range(10):
        send_mail(i)
    

start_time = time.time()
main()
print(f'Время выполнения программы: {time.time() - start_time} с')