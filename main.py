from abc import abstractmethod, ABC


class Storage(ABC):
    @abstractmethod
    def add(self, name, count):
        pass

    @abstractmethod
    def remove(self, name, count):
        pass

    @abstractmethod
    def _get_free_space(self):
        pass

    @abstractmethod
    def get_items(self):
        pass

    @abstractmethod
    def get_unique_items_count(self):
        pass


class Store(Storage):
    def __init__(self, items: dict, capacity=100):
        self.__items = items
        self.__capacity = capacity

    @property
    def capacity(self):
        return self.__capacity

    @capacity.setter
    def capacity(self, count):
        self.__capacity = count

    def add(self, name, count):
        """
        Метод увеличивает запас items с учетом лимита capacity
        (добавляет наименование товара с количеством, с учётом лимита на складе)
        """
        if name in self.__items.keys():
            if self._get_free_space() >= count:
                print("Товар добавлен!")
                self.__items[name] += count
                return True
            else:
                if isinstance(self, Shop):
                    print("Недостаточно место в магазине!")
                elif isinstance(self, Store):
                    print("Недостаточно место на складе!")
                return False
        else:
            if self._get_free_space() >= count:
                print("Товар добавлен!")
                self.__items[name] = count
                return True
            else:
                if isinstance(self, Shop):
                    print("Недостаточно место в магазине!")
                elif isinstance(self, Store):
                    print("Недостаточно место на складе!")
                return False

    def remove(self, name, count):
        """
        Метод уменьшает запас items, но не ниже 0
        (уменьшает количество товара на складе, с учётом наличия количества)
        """
        if self.__items[name] >= count:
            print("Нужное количество есть на складе!")
            self.__items[name] -= count
            return True
        else:
            print("Недостаточно место на складе!")
            return False

    def _get_free_space(self):
        """
        Метод возвращает количество свободных мест
        """
        current_free_space = 0
        for value in self.__items.values():
            current_free_space += value
        return self.__capacity - current_free_space

    @property
    def get_items(self):
        """
        Метод возвращает содержание склада в словаре {товар: количество}
        """
        return self.__items

    def get_unique_items_count(self):
        """
        Метод возвращает количество уникальных товаров
        """
        return len(self.__items.keys())

    def __str__(self):
        st = "\n"
        for key, value in self.__items.items():
            st += f"{key}: {value}\n"
        return st


class Shop(Store):
    def __init__(self, items, capacity=20):
        super().__init__(items, capacity)

    def add(self, name, count):
        """
        Метод увеличивает запас items с учетом лимита capacity
        (добавляет наименование товара с количеством, с учётом лимита в магазине)
        """
        if self.get_unique_items_count() >= 5:
            print("Больше 5 различных наименований товара!")
            return False
        else:
            super().add(name, count)


def cast(word):
    """
    Метод переводит наименование переменной с русского на английский
    """
    if word == "склад_1":
        return "storage_1"
    if word == "склад_2":
        return "storage_2"
    if word == "магазин_1":
        return "shop_1"
    if word == "магазин_2":
        return "shop_2"


class Request:
    def __init__(self, request_str):
        """
        Метод обрабатывает ввод пользователя
        """
        reg_list = request_str.split()
        action = reg_list[0]
        self.__count = int(reg_list[1])
        self.__item = reg_list[2]
        if action == "доставить":
            self.__from = cast(reg_list[4])
            self.__to = cast(reg_list[6])
        elif action == "забрать":
            self.__from = cast(reg_list[4])
            self.__to = None
        elif action == "привезти":
            self.__from = None
            self.__to = cast(reg_list[4])

    def move(self):
        """
        Метод добавляет товар и его количество к количеству в "куда"
        уменьшает товар и его количество от количества "откуда"
        """
        if self.__to and self.__from:
            if eval(self.__from).remove(self.__item, self.__count):
                eval(self.__to).add(self.__item, self.__count)
        elif self.__to:
            eval(self.__to).add(self.__item, self.__count)
        elif self.__from:
            eval(self.__from).remove(self.__item, self.__count)


storage_1 = Store(items={"печеньки": 10, "собачки": 10, "коробки": 10})
storage_2 = Store(items={"собачки": 10, "коробки": 10, "елки": 10})
shop_1 = Shop(items={"печеньки": 3, "собачки": 3, "коробки": 3})
shop_2 = Shop(items={"собачки": 3, "коробки": 3, "елки": 3})

print("Привет!")

while True:
    print("Текущее наличие мест")
    print(f"СКЛАД_1: {storage_1}\nСКЛАД_2: {storage_2}\nМАГАЗИН_1: {shop_1}\nМАГАЗИН_2: {shop_2}")
    print(f"Команда 1: Доставить _ __ из ___ в ___;\nКоманда 2: Забрать _ __ из ___;\nКоманда 3: Привезти _ __ на ___;")
    print("Вставьте вместо нижних подчёркиваний выбранные слова!")
    print("'_'            - любое число;\n'__'           - одно из слов: 'печеньки', 'собачки', 'коробки', 'елки'"
          "\n'___' и '____' - одно из слов: 'склад_1', 'склад_2', 'магазин_1', 'магазин_2'")

    user_text = (input("Выберите команду и вставьте нужные слова!:\n")).lower()

    if user_text == "стоп":
        break
    else:
        try:
            reg = Request(user_text)
            reg.move()
        except Exception as e:
            print(f"Ошибка {e}, повторите попытку")
