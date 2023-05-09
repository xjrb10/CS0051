import threading
from random import randint
from time import sleep, perf_counter

balance = 250 * 100


def worker(lock: threading.Lock, destination: str, amount_cents: int, transaction_id: int, transaction_time: float):
    global balance

    print(
        f"\n> Sending P{amount_cents / 100:,.2f} to {destination} with "
        f"txn#{transaction_id} est. time: {transaction_time:0.2f}s"
    )
    start_time = perf_counter()
    with lock:
        if balance < amount_cents:
            print(
                f"\n!!! txn#{transaction_id} failed!!! After {perf_counter() - start_time:0.2f}s "
                f"(initial: {transaction_time:0.2f}s)! Current balance: P{balance / 100:,.2f}"
            )
            return
        sleep(transaction_time)
        balance -= amount_cents
        print(
            f"\n>>> txn#{transaction_id} finished after {perf_counter() - start_time:0.2f}s "
            f"(initial: {transaction_time:0.2f}s)! Current balance: P{balance / 100:,.2f}"
        )


def main():
    lock = threading.Lock()

    i = 1
    while True:
        print("")
        destination = input("Enter number to send to: ")
        amount = int(float(input("Enter amount to send: ")) * 100)

        threading.Thread(target=worker, args=(lock, destination, amount, i, randint(5, 10))).start()
        i += 1


if __name__ == '__main__':
    main()
