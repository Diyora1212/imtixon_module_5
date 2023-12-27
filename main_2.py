import threading

def printer(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(result)
    return wrapper

@printer
def reverse_number(number):
    teskari_number = int(str(number)[::-1])
    return teskari_number

def teskarisini_hisoblash(numbers):
    threads = []
    
    for number in numbers:
        thread = threading.Thread(target=reverse_number, args=(number,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    numbers = list(map(int, input("Sonlarni probel bilan ajratib kiriting: ").split()))
    teskarisini_hisoblash(numbers)
