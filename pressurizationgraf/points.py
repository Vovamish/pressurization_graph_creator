from abc import ABC, abstractmethod
class Point(ABC):
    """Абстрактый класс точки.

    Атрибуты:
        _value (int): Значение точки
        _unit (function -> str): Функция возвращающая единицы измерения в которых принимаются и выдаются значения

    Абстрактные методы:
        from_raw(int|float, str) -> str:
            Должен принимать значения в единицах хранения "raw", возвращает в единицах измерения
        in_raw(int|float, str) -> str:
            Должен принимать значение в единицах измерения, возвращает в единицах хранения "raw"

    Методы:
        get_unit() -> str:
            Возвращает единицы измерения в которых принимаются и выдаются значения
        set(int|float) -> None:
            Присваивает новое значение точке
        get(int) -> int|float:
            Возвращает значение точки

        __init__
        __call__ = get
        __eq__
        __ne__
        __lt__
        __le__
        __gt__
        __ge__
        __add__
        __sub__
        __neg__
        __hash__
    """
    @abstractmethod
    def from_raw(value, unit):
        """Принимает значения в единицах хранения "raw", возвращает в единицах измерения

        Аргументы:
            value (int|float): Значение, которое нужно преобразовать
            unit (str): Единицы измерения в которых нужно вернуть значение

        Возвращает:
            int|float: Преобразованное в единицы измерения значение
        """
        pass

    @abstractmethod
    def in_raw(value, unit):
        """Принимает значение в единицах измерения, возвращает в единицах хранения "raw"

        Аргументы:
            value (int|float): Значение, которое нужно преобразовать
            unit (str): Единицы измерения из которых нужно преобразовать значение

        Возвращает:
            int: Преобразованное в единицы хранения значение
        """
        pass

    def __init__(self, unit='raw', value=0):
        if callable(unit):
            self._unit = unit
            self.set(value)
            self.__call__ = self.get
        else:
            raise TypeError(f'unit должен быть функцией. Переданная переменная имеет тип: {type(unit)}')

    def get_unit(self, unit=None):
        """Возвращает единицы измерения в которых принимаются и выдаются значения
            Аргументы:
                unit:(function|
                    str=("с"|"мин"|"raw")|
                        ("кг"|"МПа"|"raw")): функция возвращающая единицы измерения или сами единицы измерения в которых принимаются и выдаются значения
            Возвращает:
                str: Единицы измерения
        """
        if unit is None or unit is self.get_unit:
            unit = self._unit
        while callable(unit):
            unit = unit()
        return unit

    def set(self, value, unit=None):
        """Присваивает значение точке

        Аргументы:
            value: Присваиваемое значение
            unit: Единицы измерения
        """
        self._value = self.in_raw(value, self.get_unit(unit))

    def get(self, unit):
        """Возвращает значение точки

        Аргументы:
            unit: Единицы измерения

        Возвращает:
            int|float: Значение точки
        """
        return self.from_raw(self._value, self.get_unit(unit))