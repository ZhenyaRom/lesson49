from threading import Thread
from time import sleep
from random import randint
import queue


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None


class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        sleep(randint(3, 10))


class Cafe:

    def __init__(self, *tables):
        self.tables = tables
        self.queue = queue.Queue()

    def guest_arrival(self, *guests):
        for guest in guests:
            sat_down = True
            for table in self.tables:
                if table.guest is None:
                    table.guest = guest
                    table.guest.start()
                    print(f'{guest.name} сел(-а) за стол номер {table.number}')
                    sat_down = False
                    break
            if sat_down:
                self.queue.put(guest)
                print(f'{guest.name} в очереди')

    def discuss_guests(self):
        while True:
            no_one = True
            for table in self.tables:
                if table.guest is None:
                    continue
                no_one = False
                if table.guest.is_alive():
                    continue
                table.guest.join()
                print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                table.guest = None
                print(f'Стол номер {table.number} свободен')
                if self.queue.empty():
                    continue
                table.guest = self.queue.get()
                table.guest.start()
                print(f'{table.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')
            if no_one:
                break

tables = [Table(number) for number in range(1, 6)]
guests_names = ['Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra']
guests = [Guest(name) for name in guests_names]
cafe = Cafe(*tables)
cafe.guest_arrival(*guests)
cafe.discuss_guests()
