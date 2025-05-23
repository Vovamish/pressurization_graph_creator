"""
Поменять описание в методах get_unit
Переделать операции сравнения, добавив сравнения с парой (значение, единицы измерения)
Переделать запись полок в идеальном нагружении
изменение точек, осей и график.
В Graf_Bilder(), в calculate_scale_for_graf нужно создать переменные отвечающие за количество делений на осях.
Нужно добавить подпись к графикам с именем оператора и создателями ПО
"""
import xml.etree.ElementTree as ET
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

    _value = None
    _unit = None

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

    def __init__(self, unit, value):
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
    def __eq__(self, other):
        if type(self) is type(other):
            return self._value == other._value
        else:
            return self._value == self.in_raw(other)
    def __ne__(self, other):
        if type(self) is type(other):
            return self._value != other._value
        else:
            return self._value != self.in_raw(other)
    def __lt__(self, other):
        if type(self) is type(other):
            return self._value < other._value
        else:
            return self._value < self.in_raw(other)
    def __le__(self, other):
        if type(self) is type(other):
            return self._value <= other._value
        else:
            return self._value <= self.in_raw(other)
    def __gt__(self, other):
        if type(self) is type(other):
            return self._value > other._value
        else:
            return self._value > self.in_raw(other)
    def __ge__(self, other):
        if type(self) is type(other):
            return self._value >= other._value
        else:
            return self._value >= self.in_raw(other)
    def __add__(self, other):
        if type(other) is tuple:
            unit = other[1]
            other = other[0]
        else:
            unit = self.get_unit
        if type(self) is type(other):
            new_point = self.__class__(unit=self._unit)
            new_point.set(self('raw') + other('raw'), 'raw')
        else:
            new_point = self.__class__(unit=self._unit)
            new_point.set(self('raw') + self.__class__.in_raw(other), 'raw')
        return new_point
    def __sub__(self, other):
        if type(other) is tuple:
            unit = other[1]
            other = other[0]
        else:
            unit = self.get_unit
        if type(self) is type(other):
            new_point = self.__class__(unit=self._unit)
            new_point.set(self('raw') - other('raw'), 'raw')
        else:
            new_point = self.__class__(unit=self._unit)
            new_point.set(self('raw') - self.__class__.in_raw(other), 'raw')
        return new_point
    def __neg__(self):
        new_point = self.__class__(unit=self._unit)
        new_point.set(-self('raw'),'raw')
        return new_point
    def __hash__(self):
        return hash(self._value)


class TimePoint(Point):
    """Точка времени. Способна выдавать и записывать значения в секундах и минутах.
    Можно получать значение точки при вызове объекта как функции.
    Поддерживает операции сравнения и хеширования

    Атрибуты:
        _value (int): Значение точки. Хранится в секундах.
        _unit (function -> str=("с"|"мин"|"raw")): Функция возвращающая единицы измерения в которых принимаются и выдаются значения

    Методы:
        from_raw(int|float, str=("с"|"мин"|"raw")) -> int|float:
            Принимает значения в единицах хранения "raw", возвращает в секундах или минутах
        in_raw(int|float, str) -> int:
            Принимает значение в секундах или минутах, возвращает в единицах хранения "raw"
        get_unit() -> str:
            Возвращает единицы измерения в которых принимаются и выдаются значения
        set(int|float) -> None
            Присваевает новое значение точке
        get() -> (int|float)
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
    def __init__(self, unit, value=0):
        if callable(unit):
            self._unit = unit
            self.set(value)
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

    def get(self, unit=None):
        """Возвращает значение точки

        Аргументы:
            unit: Единицы измерения

        Возвращает:
            int|float: Значение точки
        """
        return self.from_raw(self._value, self.get_unit(unit))
    def _call_(self, unit=None):
        return self.get(unit)
    @staticmethod
    def from_raw(value, unit=None):
        """Принимает значения в единицах хранения "raw", возвращает в секундах или минутах

        Аргументы:
            value (int|float): Значение, которое нужно преобразовать
            unit (str=("с"|"мин"|"raw")): Единицы измерения в которых нужно вернуть значение

        Возвращает:
            int|float: Преобразованное в единицы измерения значение
        """
        if type(value) != int and type(value) != float:
            raise TypeError(f'Тип value должен быть int или float. Переданная переменная имеет тип: {type(value)}')
        elif type(unit) == str:
            if unit=='с' or unit=='raw':
                return value
            elif unit=='мин':
                return value/60
            else:
                raise ValueError(f'Значение unit должено быть "с", "мин" или "raw". Переданное значение unit: {unit}')
        else:
            raise TypeError(f'Тип unit должен быть str. Переданная переменная имеет тип: {type(unit)}')

    @staticmethod
    def in_raw(value, unit):
        """Принимает значение в секундах или минутах, возвращает в единицах хранения "raw"

        Аргументы:
            value (int|float): Значение, которое нужно преобразовать
            unit (str=("с"|"мин"|"raw")): Единицы измерения из которых нужно преобразовать значение

        Возвращает:
            int: Преобразованное в единицы хранения значение
        """
        if type(value) != int and type(value) != float:
            raise TypeError(f'Тип value должен быть int или float. Переданная переменная имеет тип: {type(value)}')
        elif type(unit) == str:
            if unit=='с' or unit=='raw':
                return round(value)
            elif unit=='мин':
                return round(value*60)
            else:
                raise ValueError(f'Значение unit должено быть "с", "мин" или "raw". Переданное значение unit: {unit}')
        else:
            raise TypeError(f'Тип unit должен быть str. Переданная переменная имеет тип: {type(unit)}')
    def __eq__(self, other):
        if type(self) is type(other):
            return self._value == other._value
        else:
            return self._value == self.in_raw(other, self.get_unit())
    def __ne__(self, other):
        if type(self) is type(other):
            return self._value != other._value
        else:
            return self._value != self.in_raw(other, self.get_unit())
    def __lt__(self, other):
        if type(self) is type(other):
            return self._value < other._value
        else:
            return self._value < self.in_raw(other, self.get_unit())
    def __le__(self, other):
        if type(self) is type(other):
            return self._value <= other._value
        else:
            return self._value <= self.in_raw(other, self.get_unit())
    def __gt__(self, other):
        if type(self) is type(other):
            return self._value > other._value
        else:
            return self._value > self.in_raw(other, self.get_unit())
    def __ge__(self, other):
        if type(self) is type(other):
            return self._value >= other._value
        else:
            return self._value >= self.in_raw(other, self.get_unit())
    def __add__(self, other):
        if type(other) is tuple:
            unit = other[1]
            other = other[0]
        else:
            unit = self.get_unit()
        if type(self) is type(other):
            new_point = TimePoint(unit=self._unit)
            new_point.set(self.get('raw') + other.get('raw'), 'raw')
        else:
            new_point = TimePoint(unit=self._unit)
            new_point.set(self.get('raw') + self.in_raw(other, self.get_unit(unit)), 'raw')
        return new_point
    def __sub__(self, other):
        if type(other) is tuple:
            unit = other[1]
            other = other[0]
        else:
            unit = self.get_unit
        if type(self) is type(other):
            new_point = TimePoint(unit=self._unit)
            new_point.set(self.get('raw') - other.get('raw'), 'raw')
        else:
            new_point = self.TimePoint(unit=self._unit)
            new_point.set(self.get('raw') - self.in_raw(other, self.get_unit(unit)), 'raw')
        return new_point
    def __neg__(self):
        new_point = self.TimePoint(unit=self._unit)
        new_point.set(-self.get('raw'),'raw')
        return new_point
    def __hash__(self):
        return hash(self._value)

class PressurePoint(Point):
    """Точка давления. Способна выдавать и записывать значения в килограммах или мегапаскалях.
    Можно получать значение точки при вызове объекта как функции.
    Поддерживает операции сравнения и хеширования

    Атрибуты:
        _value (int): Значение точки. Хранится в десятых килограмма.
        _unit (function -> str=("кг"|"МПа"|"raw")): Функция возвращающая единицы измерения

    Методы:
        from_raw(int|float, str=("кг"|"МПа"|"raw")) -> int|float
            Принимает значения в единицах хранения "raw", возвращает в килограммах или мегапаскалях
        in_raw(int|float, str=("кг"|"МПа"|"raw")) -> int
            Принимает значение в килограммах или мегапаскалях, возвращает в единицах хранения "raw"
        get_unit() -> str:
            Возвращает единицы измерения в которых принимаются и выдаются значения
        set(int|float) -> None
            Присваевает новое значение точке
        get() -> (int|float)
            Возвращает значение точки
        __init__
        __call__
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
    def __init__(self, unit, value=0):
        if callable(unit):
            self._unit = unit
            self.set(value)
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

    def get(self, unit=None):
        """Возвращает значение точки

        Аргументы:
            unit: Единицы измерения

        Возвращает:
            int|float: Значение точки
        """
        return self.from_raw(self._value, self.get_unit(unit))
    def _call_(self, unit=None):
        return self.get(unit)
    @staticmethod
    def from_raw(value, unit=None):
        """Принимает значения в единицах хранения "raw", возвращает в килограммах или мегапаскалях

        Аргументы:
            value (int|float): Значение, которое нужно преобразовать
            unit (str=("кг"|"МПа"|"raw")): Единицы измерения в которых нужно вернуть значение

        Возвращает:
            int|float: Преобразованное в единицы измерения значение
        """
        if type(value) != int and type(value) != float:
            raise TypeError(f'Тип value должен быть int или float. Переданная переменная имеет тип: {type(value)}')
        elif type(unit) == str:
            if unit=='raw':
                return value
            elif unit=='кг':
                return value /10
            elif unit=='МПа':
                return value/100
            else:
                raise ValueError(f'Значение unit должено быть "кг", "МПа" или "raw". Переданное значение unit: {unit}')
        else:
            raise TypeError(f'Тип unit должен быть str. Переданная переменная имеет тип: {type(unit)}')

    @staticmethod
    def in_raw(value, unit):
        """Принимает значение в килограммах или мегапаскалях или единицах хранения, возвращает в единицах хранения "raw"

        Аргументы:
            value (int|float): Значение, которое нужно преобразовать
            unit (str=("кг"|"МПа"|"raw"): Единицы измерения из которых нужно преобразовать значение

        Возвращает:
            int: Преобразованное в единицы хранения значение
        """
        if type(value) != int and type(value) != float:
            raise TypeError(f'Тип value должен быть int или float. Переданная переменная имеет тип: {type(value)}')
        elif type(unit) == str:
            if unit=='raw':
                return round(value)
            elif unit=='кг':
                return round(value*10)
            elif unit=='МПа':
                return round(value*100)
            else:
                raise ValueError(f'Значение unit должено быть "кг", "МПа" или "raw". Переданное значение unit: {unit}')
        else:
            raise TypeError(f'Тип unit должен быть str. Переданная переменная имеет тип: {type(unit)}')
    def __eq__(self, other):
        if type(self) is type(other):
            return self._value == other._value
        else:
            return self._value == other
    def __ne__(self, other):
        if type(self) is type(other):
            return self._value != other._value
        else:
            return self._value != other
    def __lt__(self, other):
        if type(self) is type(other):
            return self._value < other._value
        else:
            return self._value < other
    def __le__(self, other):
        if type(self) is type(other):
            return self._value <= other._value
        else:
            return self._value <= other
    def __gt__(self, other):
        if type(self) is type(other):
            return self._value > other._value
        else:
            return self._value > other
    def __ge__(self, other):
        if type(self) is type(other):
            return self._value >= other._value
        else:
            return self._value >= other
    def __add__(self, other):
        if type(other) is tuple:
            unit = other[1]
            other = other[0]
        else:
            unit = self.get_unit
        if type(self) is type(other):
            new_point = TimePoint(unit=self._unit)
            new_point.set(self.get('raw') + other.get('raw'), 'raw')
        else:
            new_point = TimePoint(unit=self._unit)
            new_point.set(self.get('raw') + self.in_raw(other, self.get_unit(unit)), 'raw')
        return new_point
    def __sub__(self, other):
        if type(other) is tuple:
            unit = other[1]
            other = other[0]
        else:
            unit = self.get_unit
        if type(self) is type(other):
            new_point = TimePoint(unit=self._unit)
            new_point.set(self.get('raw') - other.get('raw'), 'raw')
        else:
            new_point = self.TimePoint(unit=self._unit)
            new_point.set(self.get('raw') - self.in_raw(other, self.get_unit(unit)), 'raw')
        return new_point
    def __neg__(self):
        new_point = self.TimePoint(unit=self._unit)
        new_point.set(-self.get('raw'),'raw')
        return new_point
    def __hash__(self):
        return hash(self._value)

class AxisPoints():
    """Коллекция точек на оси.
    Может проверить наличие точки в оси, выдавать итератор, значение точки по индексу и индекс по значению.
    Автоматически сортирует передаваемые значения.
    
    Атрибуты:
        _unit (str=("с"|"мин"|"raw")|function)|
              (str=("кг"|"МПа"|"raw"|function):
            единицы измерения в которых принимаются и выдаются значения или функция возвращающая единицы измерения
        PointClass (class): класс, которому будут принадлежать точки на(в) оси

    Методы:
        get_unit() -> (str=("с"|"мин"|"raw")|("кг"|"МПа"|"raw"):
            Возвращает еденицы измерения в которых принимаются и выдаются значения

        set_unit(str=("с"|"мин"|"raw")|function)|
                (str=("кг"|"МПа"|"raw"|function):
            Изменяет еденицы измерения в которых принимаются и выдаются значения

        add_point(int|float, str|None): -> Point:
            Добавляет точку на ось и возвращает её

        index(int|float, str|None) -> int:
            Возвращает индекс точки оси с указанным значением

        __contains__((int|float)|(int|float, str|None)) -> bool:
            Проверяет присутствует ли значение на(в) оси
        
        __init__
        __iter__
        __getitem__
        __len__
    """
        
    def __init__(self, PointClass, unit):
        self.PointClass = PointClass
        self._points = list()
        self.set_unit(unit)

    def get_unit(self, unit = None):
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

    def set_unit(self, unit):
        """Изменяет еденицы измерения в которых принимаются и выдаются значения

        Аргументы:
            unit (function|
                    str=("с"|"мин"|"raw")|
                        ("кг"|"МПа"|"raw")):
                функция возвращающая единицы измерения или сами единицы измерения в которых принимаются и выдаются значения оси
        """
        self._unit = unit

    def add_point(self, value, unit=None):
        """Добавляет точку на ось
        Аргументы:
            value (int|float) Значение
            unit (str|None) Единицы измерения

        Возвращает:
            Point Новая точка
        """
        if type(value) == self.PointClass:
            new_point = value
        else:
            if callable(self._unit):
                new_point = self.PointClass(unit=self._unit)
            else:
                new_point = self.PointClass(unit=self.get_unit)
            new_point.set(value, self.get_unit(unit))
        self._points.append(new_point)
        self._points.sort()
        return new_point

    def index(self, value, unit=None):
        """Возвращает индекс точки оси с указанным значением
        Аргументы:
            value (int|float) Значение
            unit (str|None) Единицы измерения
        """
        return self._points.index(self.PointClass.in_raw(value, self.get_unit(unit)))

    def __iter__(self):
        return iter(self._points)

    def __getitem__(self, key):
        if key is None:
            key = self.get_unit()
        if type(key) == str:
            return tuple(p.get(key) for p in self)
        else:
            return self._points[key]

    def __len__(self):
        return len(self._points)

    def __contains__(self, variable):
        unit = None
        if type(variable) is tuple:
            unit = variable[1]
            variable = variable[0]
        return self.PointClass.in_raw(variable, self.get_unit(unit)) in self._points

class Pressurization():
    def __init__(self, unit_time = 'мин', unit_pressure = 'МПа'):
        self._unit_time = unit_time
        self._unit_pressure = unit_pressure
        self.T_Points = AxisPoints(TimePoint, self.get_unit_time)
        self.P_Points = AxisPoints(PressurePoint, self.get_unit_pressure)
        self._points = list()

    def get_unit_time(self, unit=None):
        """Возвращает единицы измерения в которых принимаются и выдаются значения
            Аргументы:
                unit:(function|
                    str=("с"|"мин"|"raw")|
                        ("кг"|"МПа"|"raw")): функция возвращающая единицы измерения или сами единицы измерения в которых принимаются и выдаются значения
            Возвращает:
                str: Единицы измерения
        """
        if unit is None or unit is self.get_unit_time:
            unit = self._unit_time
        while callable(unit):
            unit = unit()
        return unit
    def set_unit_time(self, unit):
        self._unit_time = unit
    unit_time = property(get_unit_time, set_unit_time)

    def get_unit_pressure(self, unit=None):
        """Возвращает единицы измерения в которых принимаются и выдаются значения
            Аргументы:
                unit:(function|
                    str=("с"|"мин"|"raw")|
                        ("кг"|"МПа"|"raw")): функция возвращающая единицы измерения или сами единицы измерения в которых принимаются и выдаются значения
            Возвращает:
                str: Единицы измерения
        """
        if unit is None or unit is self.get_unit_pressure:
            unit = self._unit_pressure
        while callable(unit):
            unit = unit()
        return unit
    def set_unit_pressure(self, unit):
        self._unit_pressure = unit
    unit_pressure = property(get_unit_pressure, set_unit_pressure)

    def get_units(self):
        return self.unit_time, self.unit_pressure
    def set_units(self, units):
        self.unit_time,  self.unit_pressure = units
    units = property(get_units, set_units)

    def add_point(self, time, pressure, unit_t = None, unit_p = None):
        """
        Добавить в нагружение точку.
        По умалчанию время передаётся в минутах, а давление в мегапаскалях.
        Можно передать время в секундах, а давление в килограммах с указанием единиц измерения в unit_time и unit_pressure соответственно
        """
        new_point = None
        if len(self._points) == 0:
            if time == 0:
                new_time_point = self.T_Points.add_point(time, unit_t)
                new_pressure_point = self.P_Points.add_point(pressure, unit_p)
                new_point = new_time_point, new_pressure_point
            else:
                raise ValueError(f'Время первой точки нагружения должно равняться нуля. Переданное значение time: {time}')
        elif time> 0:
            new_time_point = self.T_Points.add_point(time, unit_t)
            if (pressure, unit_p) in self.P_Points:
                index = self.P_Points.index(pressure, unit_p)
                new_point = new_time_point, self.P_Points[index]
            else:
                new_pressure_point = self.P_Points.add_point(pressure, unit_p)
                new_point = new_time_point, new_pressure_point
        else:
            raise ValueError(f'Время должно быть больше или равно нуля. Переданное значение time: {time}.')
        self._points.append(new_point)
        self._points.sort()
        return new_point

    def __len__(self):
        return len(self._points)

    def add_interval(self, time, pressure, unit_t = None, unit_p = None):
        """
        Добавить в нагружение интервал.
        По умалчанию время передаётся в минутах, а давление в мегапаскалях.
        Можно передать время в секундах, а давление в килограммах с указанием единиц измерения в unit_time и unit_pressure соответственно
        """
        new_point = None
        if len(self.T_Points) == 0:
            zerro_t_point = self.T_Points.add_point(0, unit_t)
            zerro_p_point = self.P_Points.add_point(0, unit_p)
            zerro_point = zerro_t_point, zerro_p_point
            self._points.append(zerro_point)
        if time <= 0:
            raise ValueError(f'Время интервала должно быть больше нуля. Переданное значение time: {time}.')
        else:
            new_time_point = self.T_Points.add_point(self.T_Points[-1] + (time, unit_t))
            pressure_value = pressure + self._points[-1][1].get(unit_p)
            if (pressure_value, unit_p) in self.P_Points:
                index = self.P_Points.index(pressure_value, unit_p)
                new_point = new_time_point, self.P_Points[index]
            else:
                new_p_point = self.P_Points.add_point(pressure_value, unit_p)
                new_point = new_time_point, new_p_point
        self._points.append(new_point)
        return new_point

    def __getitem__(self, key):
        if key == 'time':
            return self.T_Points
        elif key == 'pressure':
            return self.P_Points
        else:
            return self._points[key]

    def __iter__(self):
        return iter(self._points)

    def points(self, unit_t = None, unit_p = None):
        return tuple((point[0].get(unit_t), point[1].get(unit_p)) for point in self)

    def intervals(self, unit_t = None, unit_p = None):
        return tuple((pair[1][0].get(unit_t) - pair[0][0].get(unit_t), pair[1][1].get(unit_p) - pair[0][1].get(unit_p)) for pair in zip(self[:-1], self[1:]))

    def ideal_fill(
            self,
            obj_name, #название объекта
            working_pressure, #рабочее давление
            speed_percentage, #скорость в процентах
            steps = ((60, 25), (10, 50), (10, 75), (10, 100), (10, 125)), #перечисление полок и времени выдержки на них
            standard_time_step = 10,
            test_pressure = None, #пробное давление
            double_pressurization = False, #двойное нагружение
            unit_time = None,
            unit_pressure = None
        ):
        
        self.pressurization_types = 'идеальное'
        if unit_time is not None:
            self.unit_time = unit_time
        if unit_pressure is not None:
            self.unit_pressure = unit_pressure
        self.obj_name = obj_name
        self.working_pressure = self.P_Points.add_point(working_pressure)
        self.speed_percentage = speed_percentage
        speed_in_units = self.working_pressure.get() * self.speed_percentage / 100
        self.speed_in_units = speed_in_units
        i = 0
        self.add_point(0,0)
        prev_perc_press = 0
        if steps[0][1] == 0:
            self.add_interval(*steps[0])
            i = 1
        while i < len(steps):
            if test_pressure is None or steps[i][1] * working_pressure / 100 < test_pressure:
                def_perc_press = steps[i][1] - prev_perc_press
                def_press = def_perc_press * working_pressure / 100
                def_time = def_perc_press / speed_percentage
                self.add_interval(def_time, def_press)
                self.add_interval(steps[i][0],0)
                prev_perc_press = steps[i][1]
                i += 1
            else:
                def_press = test_pressure - self[-1][1].get()
                def_time = def_press * speed_in_units
                self.add_interval(def_time, def_press)
                self.add_interval(5*60, def_press, (raw, None))
                i = len(steps)
        max_pressure = self[-1][1].get()
        self.max_pressure = self[-1][1]
        time_max_step = self[-1][0].get()
        def_press = working_pressure - max_pressure
        def_time = abs(def_press / speed_in_units)
        self.add_interval(def_time, def_press)
        self.add_interval(standard_time_step, 0)
        if double_pressurization:
            self.add_interval(-def_time, def_press)
            self.add_interval(time_max_step, 0)
            self.add_interval(def_time, def_press)
            self.add_interval(standard_time_step, 0)
        def_press = - working_pressure
        def_time = 100 / speed_percentage
        self.add_interval(def_time, def_press)
        self.duration = self.T_Points[-1]

    def real_fill(self, obj_name, working_pressure, points, test_pressure = None, unit_time = 'мин', unit_pressure = 'МПа'):
        self.pressurization_types = 'реальное'
        self.obj_name = obj_name
        self.units = unit_time, unit_pressure
        self.working_pressure = PressurePoint(self.get_unit_pressure, working_pressure)
        if test_pressure is None:
            self.test_pressure = None
        else:
            self.test_pressure = PressurePoint(self.get_unit_pressure, test_pressure)
        for p in points:
            self.add_point(*p)
        self.duration = self.T_Points[-1]
        self.max_pressure = self.P_Points[-1]
 
    def create_nag_text(self):
        """
        Создаёт текст для nag файла. nag файл - это файл, который формирует и принимает
        """
        nag_text = '!\n'
        for p in self.points('raw', 'raw'):
            nag_text += f'{p[0]}\t{p[1]}\t\n'
        return nag_text

class Graf_Bilder():
    @staticmethod
    def get_str_width(string, f_size): #get_str_size_x(string, f_size)
        """
        Принимает строку и размер шрифта в условных единицах. Возвращает ширину строки на изображении в условных единицах.
        Содержит словарь с отношением ширины символов к размеру шрифта.
        """
        symbol_size_dict = {"A": 0.6993006993006993, "B": 0.6451612903225806, "C": 0.6451612903225806, "D": 0.6993006993006993, "E": 0.5952380952380952, "F": 0.5405405405405406, "G": 0.6993006993006993, "H": 0.6993006993006993, "I": 0.3246753246753247, "J": 0.3787878787878788, "K": 0.6993006993006993, "L": 0.5952380952380952, "M": 0.8620689655172413, "N": 0.6993006993006993, "O": 0.6993006993006993, "P": 0.5405405405405406, "Q": 0.6993006993006993, "R": 0.6451612903225806, "S": 0.5405405405405406, "T": 0.5952380952380952, "U": 0.6993006993006993, "V": 0.6993006993006993, "W": 0.9090909090909091, "X": 0.6993006993006993, "Y": 0.6993006993006993, "Z": 0.5988023952095808, "a": 0.43103448275862066, "b": 0.4854368932038835, "c": 0.43103448275862066, "d": 0.4854368932038835, "e": 0.43103448275862066, "f": 0.3067484662576687, "g": 0.4854368932038835, "h": 0.4854368932038835, "i": 0.27100271002710025, "j": 0.27100271002710025, "k": 0.4854368932038835, "l": 0.27100271002710025, "m": 0.7518796992481203, "n": 0.4854368932038835, "o": 0.4854368932038835, "p": 0.4854368932038835, "q": 0.4854368932038835, "r": 0.3246753246753247, "s": 0.3787878787878788, "t": 0.27100271002710025, "u": 0.4854368932038835, "v": 0.4854368932038835, "w": 0.6993006993006993, "x": 0.4854368932038835, "y": 0.4854368932038835, "z": 0.4329004329004329, "А": 0.6993006993006993, "Б": 0.5586592178770949, "В": 0.6493506493506493, "Г": 0.5617977528089888, "Д": 0.6622516556291391, "Е": 0.5952380952380952, "Ё": 0.5952380952380952, "Ж": 0.8695652173913043, "З": 0.4878048780487805, "И": 0.6993006993006993, "Й": 0.6993006993006993, "К": 0.6493506493506493, "Л": 0.6578947368421053, "М": 0.8620689655172413, "Н": 0.6993006993006993, "О": 0.6993006993006993, "П": 0.6993006993006993, "Р": 0.5405405405405406, "С": 0.6493506493506493, "Т": 0.5952380952380952, "У": 0.684931506849315, "Ф": 0.7633587786259542, "Х": 0.6993006993006993, "Ц": 0.6993006993006993, "Ч": 0.6289308176100629, "Ш": 0.970873786407767, "Щ": 0.970873786407767, "Ъ": 0.684931506849315, "Ы": 0.847457627118644, "Ь": 0.5586592178770949, "Э": 0.6410256410256411, "Ю": 0.9900990099009901, "Я": 0.6535947712418301, "а": 0.43103448275862066, "б": 0.49504950495049505, "в": 0.45871559633027525, "г": 0.398406374501992, "д": 0.49504950495049505, "е": 0.43103448275862066, "ё": 0.43103448275862066, "ж": 0.6711409395973155, "з": 0.3952569169960474, "и": 0.5208333333333334, "й": 0.5208333333333334, "к": 0.47393364928909953, "л": 0.4854368932038835, "м": 0.6134969325153374, "н": 0.5208333333333334, "о": 0.4854368932038835, "п": 0.5208333333333334, "р": 0.4854368932038835, "с": 0.43103448275862066, "т": 0.425531914893617, "у": 0.4854368932038835, "ф": 0.6211180124223602, "х": 0.4854368932038835, "ц": 0.5208333333333334, "ч": 0.49019607843137253, "ш": 0.746268656716418, "щ": 0.746268656716418, "ъ": 0.5025125628140703, "ы": 0.6535947712418301, "ь": 0.4444444444444444, "э": 0.41841004184100417, "ю": 0.7246376811594203, "я": 0.4484304932735426, "0": 0.4854368932038835, "1": 0.45045045045045046, "2": 0.4854368932038835, "3": 0.4854368932038835, "4": 0.4854368932038835, "5": 0.4854368932038835, "6": 0.4854368932038835, "7": 0.4854368932038835, "8": 0.4854368932038835, "9": 0.4854368932038835, """!""": 0.3246753246753247, """@""": 0.8928571428571429, """#""": 0.4854368932038835, """$""": 0.4854368932038835, """%""": 0.8064516129032258, """^""": 0.45662100456621, """&""": 0.7518796992481203, """*""": 0.4854368932038835, """(""": 0.3246753246753247, """)""": 0.3246753246753247, """-""": 0.3246753246753247, """_""": 0.4854368932038835, """=""": 0.546448087431694, """+""": 0.546448087431694, """`""": 0.3246753246753247, """~""": 0.5263157894736842, """/""": 0.27100271002710025, """{""": 0.4672897196261682, """}""": 0.4672897196261682, """[""": 0.3246753246753247, """]""": 0.3246753246753247, """:""": 0.27100271002710025, """\"""": 0.3968253968253968, """;""": 0.27100271002710025, """'""": 0.1757469244288225, """<""": 0.546448087431694, """>""": 0.546448087431694, """,""": 0.24390243902439024, """.""": 0.24390243902439024, """?""": 0.43103448275862066, """\\""": 0.2717391304347826, """ """: 0.24390243902439024, """«""": 0.36496350364963503, """»""": 0.36496350364963503}
        width = 0
        for c in string:
            width += symbol_size_dict[c]
        return width*f_size
    @staticmethod
    def get_str_height(f_size): #get_str_size_y(f_size)
        """
        Принимает размер шрифта в условных единицах. Возвращает высоту строки на изображении в условных единицах.
        """
        return f_size*2/3
    @staticmethod
    def round_and_str(num, unit):
        """
        Округляет до заданного знака после запятой, отбрасывает лишние нули, вплоть до удаления точки.
        Результат выводит как строку в которой заменяет '.' на ','
        """
        ndigits_dict = {'с': 0,'raw': 0, 'мин': 1, 'кг': 1, 'МПа': 2}
        str_num = str(round(num, ndigits_dict[unit]))
        if '.' in str_num:
            while str_num[-1] == '0':
                str_num = str_num[:-1]
            if str_num[-1] == '.':
                str_num = str_num[:-1]
        str_num = str_num.replace('.', ',')
        return str_num
    def __init__(self, pressurization, signature = None, unit_time = None, unit_pressure = None):
        self.Pr_n = pressurization
        if unit_time == None:
            self.unit_time = self.Pr_n.get_unit_time
        else:
            self.Pr_n.set_unit_time(unit_time)
            self.unit_time = self.Pr_n.get_unit_time
        if unit_pressure == None:
            self.unit_pressure = self.Pr_n.get_unit_pressure
        else:
            self.Pr_n.set_unit_pressure(unit_pressure)
            self.unit_pressure = self.Pr_n.get_unit_pressure
        self.units = unit_time, unit_pressure
        self.font_size = 15
        self.gap = max(self.gss_x(' '), self.gss_y())
        self.size_x = (297 - 30) * 4
        self.size_y = (210 / 2) * 4
        self.svg = ET.Element('svg')
        self.svg.set('version', "1.1")
        self.svg.set('baseProfile', "full")
        self.svg.set('width', str(self.size_x))
        self.svg.set('height', str(self.size_y))
        self.svg.set('viewBox', '0 0 ' + str(self.size_x) + ' ' + str(self.size_y))
        self.svg.set('xmlns', 'http://www.w3.org/2000/svg')
        self.title = ET.SubElement(self.svg, 'title')
        self.desc = ET.SubElement(self.svg, 'desc')
        self.defs = ET.SubElement(self.svg, 'defs')
        self.g_graph = ET.SubElement(self.svg, 'g')
        self.g_graph.set("id", "entire graph")
        self.name_x_axis = 't, ' + self.Pr_n.unit_time
        self.name_y_axis = 'p, ' + self.Pr_n.unit_pressure
        self.signature = 'АЭ контроль проводили сотрудники ООО «НТЦ «ЭгидА», Сафьяник А.А. и Дмитриев К.А.'
        
    def create_watermark(self):
        watermark_font_size = 16
        watermark = 'ПО написал Мишунин В.'
        t_watermark = ET.SubElement(svg, 'text')
        t_watermark.set("x", str(size_x/4 - gss_x(watermark, watermark_font_size)/2))
        t_watermark.set("y", str(gss_y(watermark_font_size) + 3*gap))
        t_watermark.set("font-size", str(watermark_font_size))
        t_watermark.set("opacity", str(1/8))
        t_watermark.set("fill", "grey")
        t_watermark.text = watermark

    def create_marker(self):
        self.marker = ET.SubElement(self.defs, 'marker')
        self.marker.set("id", "arrowhead")
        self.marker.set("markerWidth", "12")
        self.marker.set("markerHeight", "8")
        self.marker.set("orient", "auto")
        self.marker.set("refX", "9")
        self.marker.set("refY", "4")
        self.marker.set("stroke", "black")
        self.marker_line = ET.SubElement(self.marker, 'polyline')
        self.marker_line.set("points", "3, 2 9, 4 3, 6")
        self.marker_line.set("fill", "none")
        
    def gss_x(self, string):
        """
        Принимает строку и размер шрифта в условных единицах. Возвращает ширину строки на изображении в условных единицах. Задан размер шрифта по умолчанию
        """
        return self.get_str_width(string, self.font_size)
    def gss_y(self):
        """
        Принимает размер шрифта в условных единицах. Возвращает высоту строки на изображении в условных единицах. Задан размер шрифта по умолчанию
        """
        return self.get_str_height(self.font_size)
    def calculate_scale_for_graf(self):
        self.is_draw_coordinates_scale = False

        self.offset_axes_x = 2 * self.gap
        sin_45 = 0.7
        max_time_text_size = max(map(self.gss_x, map(str, self.Pr_n.T_Points[None])))
        self.offset_axes_y = sin_45 * (max_time_text_size + self.gss_y()) + self.gap # + (self.gap + self.gss_y())*2/3
        self.graf_size_x = self.size_x - self.offset_axes_x - self.gss_x(self.name_x_axis) - self.gap*3 #30
        self.graf_size_y = self.size_y - self.offset_axes_y - self.gss_y()*2 - self.gap*3 #14
        self.scale_x = self.graf_size_x / self.Pr_n.duration.get('raw')
        def convert_x(x):
            return self.offset_axes_x + self.scale_x * x
        self.scale_y = self.graf_size_y / self.Pr_n.max_pressure.get('raw')
        def convert_y(y):
            return self.size_y - self.offset_axes_y - self.scale_y * y
        self.convert_x = convert_x
        self.convert_y = convert_y
        for i in range(1, len(self.Pr_n.P_Points)):
            if (self.scale_y * abs(self.Pr_n.P_Points[i].get('raw') - self.Pr_n.P_Points[i-1].get('raw'))) < self.gss_y() * 1.5:
                self.is_draw_coordinates_scale = True
        if not self.is_draw_coordinates_scale:
            for i in range(1, len(self.Pr_n.T_Points)):
                if sin_45 * (self.gss_y() + self.gap*2) > self.scale_x * (self.Pr_n.T_Points[i].get('raw') - self.Pr_n.T_Points[i-1].get('raw')):
                    self.is_draw_coordinates_scale = True
        if self.is_draw_coordinates_scale:
            y_scale_step = int(-(-self.Pr_n.P_Points[-1].get('raw') // 10))
            y_scale_max_val = y_scale_step*10
            x_scale_step = int(-(-self.Pr_n.T_Points[-1].get('raw') // 20))
            x_scale_max_val = x_scale_step*20
            max_pressure_text_size = max(map(self.gss_x, map(str, self.Pr_n.P_Points[None])))
            self.offset_axes_x = 2 * self.gap + max_pressure_text_size
            self.offset_axes_y = sin_45 * (max_time_text_size + self.gss_y()) + self.gap # + (self.gap + self.gss_y())*2/3
            self.graf_size_x = self.size_x - self.offset_axes_x - self.gss_x(self.name_x_axis) - self.gap*3 #30
            self.graf_size_y = self.size_y - self.offset_axes_y - self.gss_y() - self.gap*3 #14
            self.scale_x = self.graf_size_x / x_scale_max_val
            def convert_x(x):
                return self.offset_axes_x + self.scale_x * x
            self.scale_y = self.graf_size_y / y_scale_max_val
            def convert_y(y):
                return self.size_y - self.offset_axes_y - self.scale_y * y
            self.convert_x = convert_x
            self.convert_y = convert_y
            self.X_scale = AxisPoints(TimePoint, self.unit_time)
            self.X_scale.set_unit('raw')
            for i in range(1,21):
                self.X_scale.add_point(i*x_scale_step, 'raw')
            self.Y_scale = AxisPoints(PressurePoint, self.unit_pressure)
            self.Y_scale.set_unit('raw')
            for i in range(1,11):
                self.Y_scale.add_point(i*y_scale_step, 'raw')

    def draw_auxilary_lines(self, auxiliary_lines_width = 1.5):
        self.auxiliary_lines_width = auxiliary_lines_width
        self.g_auxiliary_lines = ET.SubElement(self.g_graph, 'g')
        self.g_auxiliary_lines.set("id","auxiliary-lines")
        self.g_auxiliary_lines.set("stroke","darkgrey")
        self.g_auxiliary_lines.set("stroke-width",str(self.auxiliary_lines_width))
        self.g_auxiliary_lines.set("style","stroke-dasharray: " + str(self.gap) + ' ' + str(self.gap/2))
        self.l_auxiliary_lines_x = list()
        self.l_auxiliary_lines_y = list()
        
        for i in range(0,-len(self.Pr_n.intervals('raw', 'raw')) - 1, -1):
            set_of_y_point = {0}
            if self.Pr_n.points('raw', 'raw')[i-1][1] != 0:
                self.l_auxiliary_lines_x.append(ET.SubElement(self.g_auxiliary_lines, 'line'))
                self.l_auxiliary_lines_x[-1].set("x1", str(self.convert_x(self.Pr_n.points('raw', 'raw')[i-1][0])))
                self.l_auxiliary_lines_x[-1].set("x2", str(self.convert_x(self.Pr_n.points('raw', 'raw')[i-1][0])))
                self.l_auxiliary_lines_x[-1].set("y1", str(self.convert_y(0)))
                self.l_auxiliary_lines_x[-1].set("y2", str(self.convert_y(self.Pr_n.points('raw', 'raw')[i-1][1])))
            if self.Pr_n.intervals('raw', 'raw')[i][1] != 0 and self.Pr_n.points('raw')[i][0] not in set_of_y_point:
                set_of_y_point.add(self.Pr_n.points('raw', 'raw')[i][0])
                self.l_auxiliary_lines_y.append(ET.SubElement(self.g_auxiliary_lines, 'line'))
                self.l_auxiliary_lines_y[-1].set("x1", str(self.convert_x(0)))
                self.l_auxiliary_lines_y[-1].set("x2", str(self.convert_x(self.Pr_n.points('raw', 'raw')[i][0])))
                self.l_auxiliary_lines_y[-1].set("y1", str(self.convert_y(self.Pr_n.points('raw', 'raw')[i][1])))
                self.l_auxiliary_lines_y[-1].set("y2", str(self.convert_y(self.Pr_n.points('raw', 'raw')[i][1])))

        self.g_work_pressure_line = ET.SubElement(self.g_graph, 'g')
        self.l_work_pressure_line = ET.SubElement(self.g_work_pressure_line, 'line')
        self.l_work_pressure_line.set("id","work pressure line")
        self.l_work_pressure_line.set("stroke","grey")
        self.l_work_pressure_line.set("stroke-width",str(2))
        self.l_work_pressure_line.set("x1",str(self.offset_axes_x - self.gap/2))
        self.l_work_pressure_line.set("x2",str(self.size_x - self.gap*2))
        self.l_work_pressure_line.set("y1",str(self.convert_y(self.Pr_n.working_pressure.get('raw'))))
        self.l_work_pressure_line.set("y2",str(self.convert_y(self.Pr_n.working_pressure.get('raw'))))
        self.t_work_pressure_line = ET.SubElement(self.g_work_pressure_line, 'text')
        self.t_work_pressure_line.set("font-size", str(self.font_size))
        text = 'Pраб ' + str(self.Pr_n.working_pressure.get())+', ' + self.unit_pressure()
        self.t_work_pressure_line.text = text
        self.t_work_pressure_line.set("x", str(self.size_x - self.gap*2 - self.gss_x(text)))
        self.t_work_pressure_line.set("y", str(self.convert_y(self.Pr_n.working_pressure.get('raw'))-self.gap/2))
        

    def draw_coordinates_axis(self, axes_stroke_width = 2, axis_points_r = 2.25):
        self.axes_stroke_width = axes_stroke_width
        self.axis_points_r = axis_points_r
        self.g_coordinates_axis = ET.SubElement(self.g_graph, 'g')
        self.g_coordinates_axis.set("id", "coordinates axis")
        self.g_coordinates_axis.set("stroke", "black")
        self.g_coordinates_axis.set("stroke-width", str(axes_stroke_width))
        self.g_coordinates_axis.set("marker-end", "url(#arrowhead)")
        self.l_axis = ET.SubElement(self.g_coordinates_axis, 'line'), ET.SubElement(self.g_coordinates_axis, 'line')
        self.l_axis[0].set("x1", str(self.offset_axes_x))
        self.l_axis[0].set("y1", str(self.size_y-self.gap)) # - (self.gap + self.gss_y())*2/3))
        self.l_axis[0].set("x2", str(self.offset_axes_x))
        self.l_axis[0].set("y2", str(self.gap))
        self.l_axis[1].set("x1", str(self.gap))
        self.l_axis[1].set("y1", str(self.size_y-self.offset_axes_y))
        self.l_axis[1].set("x2", str(self.size_x-self.gap))
        self.l_axis[1].set("y2", str(self.size_y-self.offset_axes_y))

        self.g_axis_points = ET.SubElement(self.g_graph, 'g')
        self.g_axis_points.set("id", "points on axis")
        self.c_axis_points_x = list()
        for x in self.Pr_n.T_Points:
            self.c_axis_points_x.append(ET.SubElement(self.g_axis_points, 'circle'))
            self.c_axis_points_x[-1].set("cx", str(self.convert_x(x.get('raw'))))
            self.c_axis_points_x[-1].set("cy", str(self.convert_y(0)))
            self.c_axis_points_x[-1].set("r", str(self.axis_points_r))
        self.c_axis_points_y = list()
        for y in self.Pr_n.P_Points:
            self.c_axis_points_y.append(ET.SubElement(self.g_axis_points, 'circle'))
            self.c_axis_points_y[-1].set("cx", str(self.convert_x(0)))
            self.c_axis_points_y[-1].set("cy", str(self.convert_y(y.get('raw'))))
            self.c_axis_points_y[-1].set("r", str(self.axis_points_r))
        if self.is_draw_coordinates_scale:
            self.l_axis_points_x = list()
            mini_step_x = self.X_scale[0].get('raw')/2
            for i in range(len(self.X_scale)):
                self.l_axis_points_x.append(ET.SubElement(self.g_axis_points, 'line'))
                self.l_axis_points_x[-1].set("x1", str(self.convert_x(self.X_scale[i].get('raw'))))
                self.l_axis_points_x[-1].set("x2", str(self.convert_x(self.X_scale[i].get('raw'))))
                self.l_axis_points_x[-1].set("y1", str(self.convert_y(0)+self.axes_stroke_width*3))
                self.l_axis_points_x[-1].set("y2", str(self.convert_y(0)-self.axes_stroke_width*3))
                self.l_axis_points_x[-1].set("stroke", "black")
                self.l_axis_points_x[-1].set("stroke-width", str(self.axes_stroke_width))
                self.l_axis_points_x.append(ET.SubElement(self.g_axis_points, 'line'))
                self.l_axis_points_x[-1].set("x1", str(self.convert_x(self.X_scale[i].get('raw')-mini_step_x)))
                self.l_axis_points_x[-1].set("x2", str(self.convert_x(self.X_scale[i].get('raw')-mini_step_x)))
                self.l_axis_points_x[-1].set("y1", str(self.convert_y(0)+self.axes_stroke_width*2))
                self.l_axis_points_x[-1].set("y2", str(self.convert_y(0)-self.axes_stroke_width*2))
                self.l_axis_points_x[-1].set("stroke", "black")
                self.l_axis_points_x[-1].set("stroke-width", str(self.axes_stroke_width))

            self.l_axis_points_y = list()
            mini_step_y = self.Y_scale[0].get('raw')/2
            for i in range(len(self.Y_scale)):
                self.l_axis_points_y.append(ET.SubElement(self.g_axis_points, 'line'))
                self.l_axis_points_y[-1].set("x1", str(self.convert_x(0)-self.axes_stroke_width*3))
                self.l_axis_points_y[-1].set("x2", str(self.convert_x(0)+self.axes_stroke_width*3))
                self.l_axis_points_y[-1].set("y1", str(self.convert_y(self.Y_scale[i].get('raw'))))
                self.l_axis_points_y[-1].set("y2", str(self.convert_y(self.Y_scale[i].get('raw'))))
                self.l_axis_points_y[-1].set("stroke", "black")
                self.l_axis_points_y[-1].set("stroke-width", str(self.axes_stroke_width))
                self.l_axis_points_y.append(ET.SubElement(self.g_axis_points, 'line'))
                self.l_axis_points_y[-1].set("x1", str(self.convert_x(0)-self.axes_stroke_width*2))
                self.l_axis_points_y[-1].set("x2", str(self.convert_x(0)+self.axes_stroke_width*2))
                self.l_axis_points_y[-1].set("y1", str(self.convert_y(self.Y_scale[i].get('raw')-mini_step_y)))
                self.l_axis_points_y[-1].set("y2", str(self.convert_y(self.Y_scale[i].get('raw')-mini_step_y)))
                self.l_axis_points_y[-1].set("stroke", "black")
                self.l_axis_points_y[-1].set("stroke-width", str(self.axes_stroke_width))

        self.g_axis_text = ET.SubElement(self.g_graph, 'g')
        self.g_axis_text.set("font-size", str(self.font_size))

        self.t_name_x_axis = ET.SubElement(self.g_axis_text, 'text')
        self.t_name_x_axis.set("x", str(self.size_x - self.gap - self.gss_x(self.name_x_axis)))
        self.t_name_x_axis.set("y", str(self.convert_y(0)-self.gap))
        self.t_name_x_axis.text = self.name_x_axis
        self.t_name_y_axis = ET.SubElement(self.g_axis_text, 'text')
        self.t_name_y_axis.set("x", str(self.convert_x(0)+self.gap))
        self.t_name_y_axis.set("y", str(self.gap + self.gss_y()))
        self.t_name_y_axis.text = self.name_y_axis

        self.t_axis_point_0 = ET.SubElement(self.g_axis_text, 'text')
        self.t_axis_point_0.set("x", str(self.convert_x(0) - self.gss_x('0') - self.gap/2))
        self.t_axis_point_0.set("y", str(self.convert_y(0) + self.gap/2 + self.gss_y()))
        self.t_axis_point_0.text = '0'

        self.t_axis_point_x = list()
        self.t_axis_point_y = list()
        if not self.is_draw_coordinates_scale:
            self.path_text = list()
            self.tp_axis_point_x = list()
            for i in range(1, len(self.Pr_n.T_Points)):
                self.path_text.append(ET.SubElement(self.defs, 'path'))
                self.path_text[-1].set("id", f"text-path-{i}")
                current_text = self.round_and_str(self.Pr_n.T_Points[i].get(self.Pr_n.unit_time), self.Pr_n.unit_time)
                x2 = self.convert_x(self.Pr_n.T_Points[i].get('raw'))
                x1 = x2 - self.gss_x(current_text) / (2**0.5)
                y2 = self.gap/2 + self.convert_y(0) + self.gss_y() / (2**0.5)
                y1 = y2 + self.gss_x(current_text) / (2**0.5)
                self.path_text[-1].set("d", f"M {x1} {y1} L {x2} {y2}")
                self.t_axis_point_x.append(ET.SubElement(self.g_axis_text, 'text'))
                self.tp_axis_point_x.append(ET.SubElement(self.t_axis_point_x[-1], 'textPath'))
                self.tp_axis_point_x[-1].set('href', f"#text-path-{i}")
                self.tp_axis_point_x[-1].set('y', f"#text-path-{i}")
                self.tp_axis_point_x[-1].text = current_text
            for i in range(1, len(self.Pr_n.P_Points)):
                current_text = self.round_and_str(self.Pr_n.P_Points[i].get(self.Pr_n.unit_pressure), self.Pr_n.unit_pressure)
                self.t_axis_point_y.append(ET.SubElement(self.g_axis_text, 'text'))
                self.t_axis_point_y[-1].set("x", str(self.convert_x(0) + self.gap/2))
                self.t_axis_point_y[-1].set("y", str(self.convert_y(self.Pr_n.P_Points[i].get('raw')) - self.gap/2))
                self.t_axis_point_y[-1].text = current_text
        else:
            self.path_text = list()
            self.tp_axis_point_x = list()
            for i in range(len(self.X_scale)):
                self.path_text.append(ET.SubElement(self.defs, 'path'))
                self.path_text[-1].set("id", f"text-path-{i}")
                current_text = self.round_and_str(self.X_scale[i].get(self.Pr_n.unit_time), self.Pr_n.unit_time)
                x2 = self.convert_x(self.X_scale[i].get('raw'))
                x1 = x2 - self.gss_x(current_text) / (2**0.5)
                y2 = self.gap/2 + self.convert_y(0) + self.gss_y() / (2**0.5)
                y1 = y2 + self.gss_x(current_text) / (2**0.5)
                self.path_text[-1].set("d", f"M {x1} {y1} L {x2} {y2}")
                self.t_axis_point_x.append(ET.SubElement(self.g_axis_text, 'text'))
                self.tp_axis_point_x.append(ET.SubElement(self.t_axis_point_x[-1], 'textPath'))
                self.tp_axis_point_x[-1].set('href', f"#text-path-{i}")
                self.tp_axis_point_x[-1].set('y', f"#text-path-{i}")
                self.tp_axis_point_x[-1].text = current_text
            for i in range(len(self.Y_scale)):
                current_text = self.round_and_str(self.Y_scale[i].get(self.Pr_n.unit_pressure), self.Pr_n.unit_pressure)
                self.t_axis_point_y.append(ET.SubElement(self.g_axis_text, 'text'))
                self.t_axis_point_y[-1].set("x", str(self.convert_x(0) - self.gap - self.gss_x(current_text)))
                self.t_axis_point_y[-1].set("y", str(self.convert_y(self.Y_scale[i].get('raw')) + self.gss_y()/2))
                self.t_axis_point_y[-1].text = current_text

    def draw_graf_line(self, graph_stroke_width = 2):
        self.graph_stroke_width = graph_stroke_width
        self.graf = ET.SubElement(self.svg, 'polyline')
        self.graf.set("stroke", "black")
        self.graf.set("stroke-width",str(self.graph_stroke_width))
        self.graf.set("fill","none")
        g_points = ', '.join(map(lambda p: str(self.convert_x(p[0])) + ' ' + str(self.convert_y(p[1])), self.Pr_n.points('raw', 'raw')))
        self.graf.set("points", g_points)

    def create_pressurization_graph(self):
        self.calculate_scale_for_graf()
        self.create_marker()
        self.draw_auxilary_lines()
        self.draw_coordinates_axis()
        self.svg_tree = ET.ElementTree(self.svg)
        self.draw_graf_line()
        #self.create_signature()
        return self.svg_tree

    def create_signature(self):
        self.t_signature_text = ET.SubElement(self.g_graph, 'text')
        self.t_signature_text.set("font-size", str(self.font_size*2/3))
        self.t_signature_text.set("x", str(self.gap*3))
        self.t_signature_text.set("y", str(self.size_y - self.gap*2/3))
        self.t_signature_text.text = self.signature

