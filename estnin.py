# coding: utf-8

import datetime

from datetime import date
from collections import namedtuple

__author__ = "Anti Räis"


class _estnin(namedtuple('ESTNIN', 'century date sequence checksum')):
    def __str__(self):
        return str(int(self))

    def __int__(self):
        date = self.date
        return (
            self.century * 10**10
            + date.year % 100 * 10**8
            + date.month * 10**6
            + date.day * 10**4
            + self.sequence * 10
            + self.checksum
        )


class estnin(object):
    """
    Provides an representation for Estonian national identity number.
    """

    #: First valid value (minimum as a number).
    MIN = 10001010002
    #: Last valid value (maximum as a number).
    MAX = 89912319991

    #: Value used by :class:`estnin.create <estnin.create>` method to indicate that the new EstNIN should be created for a male.
    MALE = 0
    #: Value used by :class:`estnin.create <estnin.create>` method to indicate that the new EstNIN should be created is for a female.
    FEMALE = 1

    def __init__(self, estnin, set_checksum=False):
        """
        Create a new instance from given value.

        :param estnin: value to create an EstNIN representation for.
        :type estnin: :py:func:`str` or :py:func:`int`

        :param set_checksum: if set to :py:const:`True` then recalculate and set the checksum value.
        :type set_checksum: :py:const:`bool`

        :return: :class:`estnin <estnin>` object
        :rtype: estnin.estnin

        :raises: :py:exc:`ValueError <ValueError>` if invalid value is given.

        **Usage:**
            >>> from estnin import estnin
            >>> estnin(37001011233)
            37001011233
            >>> estnin("37001011230", set_checksum=True)
            37001011233
        """
        self._estnin = self._validate_format(estnin, set_checksum=set_checksum)

    @classmethod
    def create(cls, sex, birth_date, sequence):
        """
        Create a new instance by providing the sex, birth date and sequence.

        :param sex: use *falsy* for male and *truthy* value for female
        :type sex: :class:`estnin.MALE <estnin.MALE>` or :class:`estnin.FEMALE <estnin.FEMALE>`

        :param birth_date: date of birth
        :type birth_date: :py:func:`datetime.date`

        :param sequence: value in ``[0 - 999]`` specifing the sequence number on given day
        :type sequence: :py:func:`int`

        :return: :class:`estnin.estnin <estnin.estnin>` object
        :rtype: estnin.estnin

        :raises: :py:exc:`ValueError <ValueError>` if invalid value is provided

        **Usage:**
            >>> from estnin import estnin
            >>> from datetime import date
            >>> estnin.create(estnin.MALE, date(1970, 1, 1), 123)
            37001011233
        """
        cls._validate_year(birth_date.year)
        cls._validate_sequence(sequence)

        century = ((birth_date.year - 1800) // 100) * 2 + 1 + bool(sex)
        return cls(_estnin(century, birth_date, sequence, 0), set_checksum=True)

    def __repr__(self):
        return str(self._estnin)

    def __int__(self):
        return int(self._estnin)

    def __lt__(self, other):
        return int(self) < int(other)

    def __le__(self, other):
        return int(self) <= int(other)

    def __eq__(self, other):
        return int(self) == int(other)

    def __neg__(self):
        if self.is_male:
            self.century += 1
        else:
            self.century -= 1

        return self

    def __add__(self, other):
        days, sequence = divmod(self.sequence + other, 1000)
        date = self.date + datetime.timedelta(days=days)
        self._validate_year(date.year)
        century = self._calculate_century(date.year)
        self._estnin = self._estnin._replace(century=century, date=date, sequence=sequence)
        self._update_checksum()
        return self

    def __sub__(self, other):
        return self + (-other)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            value = estnin(self)
            self += 1
            return value
        except ValueError:
            raise StopIteration

    def __reversed__(self):
        try:
            while True:
                value = estnin(self)
                self -= 1
                yield value
        except ValueError:
            return

    @classmethod
    def _validate_year(self, year):
        if not 1800 <= year <= 2199:
            raise ValueError('year not in range [1800..2199]')

    @classmethod
    def _validate_sequence(self, sequence):
        if not 0 <= sequence <= 999:
            raise ValueError('sequence not in range [0..999]')

    @classmethod
    def _validate_century(self, century):
        if not 1 <= century <= 8:
            raise ValueError('century not in range [1..8]')

    def _calculate_century(self, year):
        century = (year - 1800) // 100 * 2 + 1
        return century if self.is_male else century + 1

    @classmethod
    def _calculate_year(self, century, year):
        return 1800 + 100 * ((century - 1) // 2) + year % 100

    def _validate_format(self, estnin, set_checksum=False):
        estnin = int(estnin)

        if set_checksum:
            if not self.MIN // 10 * 10 <= estnin <= self.MAX // 10 * 10 + 9:
                raise ValueError('value is out of range')

            checksum = self._calculate_checksum(estnin)

        else:
            if not self.MIN <= estnin <= self.MAX:
                raise ValueError('value is out of range')

            checksum = self._validate_checksum(estnin)

        return _estnin(
            estnin // 10**10,
            self._validate_date(estnin),
            (estnin // 10) % 1000,
            checksum,
        )

    def _validate_date(self, estnin):
        century = estnin // 10**10
        birth_year = self._calculate_year(century, (estnin % 10**10) // 10**8)
        birth_month = (estnin % 10**8) // 10**6
        birth_day = (estnin % 10**6) // 10**4

        return datetime.date(birth_year, birth_month, birth_day)

    def _validate_checksum(self, checksum):
        calculated = self._calculate_checksum(checksum)

        if checksum % 10 != calculated:
            raise ValueError('invalid checksum')

        return calculated

    def _update_checksum(self):
        checksum = self._calculate_checksum(self._estnin)
        self._estnin = self._estnin._replace(checksum=checksum)

    @classmethod
    def _calculate_checksum(self, estnin):
        _estnin = str(estnin)
        checksum = sum(int(k) * v for k, v in zip(_estnin, [1, 2, 3, 4, 5, 6, 7, 8, 9, 1])) % 11

        if checksum == 10:
            checksum = sum(int(k) * v for k, v in zip(_estnin, [3, 4, 5, 6, 7, 8, 9, 1, 2, 3])) % 11
            checksum = 0 if checksum == 10 else checksum

        return checksum

    @property
    def is_male(self):
        """
        Returns :py:const:`True` if the EstNIN represents a male.

        :rtype: :py:const:`bool`
        """
        return self._estnin.century % 2 == 1

    @property
    def is_female(self):
        """
        Returns :py:const:`True` if the EstNIN represents a female.

        :rtype: :py:const:`bool`
        """
        return self._estnin.century % 2 == 0

    @property
    def century(self):
        """
        Century property that returns the century digit in the EstNIN or sets it accordingly.

        :getter: return the century digit as :py:func:`int`.
        :setter: update the century digit given as :py:func:`int` or :py:func:`str`.
        :modifies: checksum
        :raises: :py:exc:`ValueError <ValueError>` if century value is not in range ``[1..8]``

        **Usage:**
            >>> from estnin import estnin
            >>> person = estnin(37001011233)
            >>> person.century
            3
            >>> person.century = 5
            >>> person
            57001011235
        """
        return self._estnin.century

    @century.setter
    def century(self, value):
        century = int(value)

        self._validate_century(century)
        year = self._calculate_year(century, self._estnin.date.year)
        date = self._estnin.date.replace(year=year)
        self._estnin = self._estnin._replace(century=century, date=date)
        self._update_checksum()

    @property
    def year(self):
        """
        Year property that returns the year in the EstNIN or sets it accordingly.

        :getter: return the year as :py:func:`int` in the format of ``YYYY``.
        :setter: update the year given as :py:func:`int` or :py:func:`str` in the format of ``YYYY``.
        :modifies: century, checksum
        :raises: :py:exc:`ValueError <ValueError>` if year value is not in range ``[1800..2199]``

        **Usage:**
            >>> from estnin import estnin
            >>> person = estnin(37001011233)
            >>> person.year
            1970
            >>> person.year = 2001
            >>> person
            50101011235
        """
        return self._estnin.date.year

    @year.setter
    def year(self, value):
        year = int(value)
        self._validate_year(year)
        date = self._estnin.date.replace(year=year)
        century = self._calculate_century(date.year)
        self._estnin = self._estnin._replace(century=century, date=date)
        self._update_checksum()

    @property
    def month(self):
        """
        Month property that returns the month in the EstNIN or sets it accordingly.

        :getter: return the month as :py:func:`int` in the format of ``MM``.
        :setter: update the month given as :py:func:`int` or :py:func:`str` in the format of ``MM``.
        :modifies: checksum
        :raises: :py:exc:`ValueError <ValueError>` if month value is not in range ``[1..12]``

        **Usage:**
            >>> from estnin import estnin
            >>> person = estnin(37001011233)
            >>> person.month
            1
            >>> person.month = 12
            >>> person
            30112011231
        """
        return self._estnin.date.month

    @month.setter
    def month(self, value):
        month = int(value)
        date = self._estnin.date.replace(month=month)
        self._estnin = self._estnin._replace(date=date)
        self._update_checksum()

    @property
    def day(self):
        """
        Day property that returns the day in the EstNIN or sets it accordingly.

        :getter: return the day as :py:func:`int` in the format of ``DD``.
        :setter: update the day given as :py:func:`int` or :py:func:`str` in the format of ``DD``.
        :modifies: checksum
        :raises: :py:exc:`ValueError <ValueError>` if day value is not valid for given month.

        **Usage:**
            >>> from estnin import estnin
            >>> person = estnin(37001011233)
            >>> person.day
            1
            >>> person.day = 31
            >>> person
            37001311233
        """
        return self._estnin.date.day

    @day.setter
    def day(self, value):
        day = int(value)
        date = self._estnin.date.replace(day=day)
        self._estnin = self._estnin._replace(date=date)
        self._update_checksum()

    @property
    def sequence(self):
        """
        Sequence property that returns the sequence in the EstNIN or sets it accordingly.

        :getter: return the sequence as :py:func:`int`.
        :setter: update the sequence given as :py:func:`int` or :py:func:`str`.
        :modifies: checksum
        :raises: :py:exc:`ValueError <ValueError>` if sequence value is not in range ``[0..999]``.

        **Usage:**
            >>> from estnin import estnin
            >>> person = estnin(37001011233)
            >>> person.sequence
            123
            >>> person.sequence = 42
            >>> person
            37001010421
        """
        return self._estnin.sequence

    @sequence.setter
    def sequence(self, value):
        sequence = int(value)

        self._validate_sequence(sequence)
        self._estnin = self._estnin._replace(sequence=sequence)
        self._update_checksum()

    @property
    def checksum(self):
        """
        Checksum property that returns the checksum digit in the EstNIN.

        :getter: return the checksum as :py:func:`int`.

        **Usage:**
            >>> from estnin import estnin
            >>> person = estnin(37001011233)
            >>> person.checksum
            3
        """
        return self._estnin.checksum

    @property
    def date(self):
        """
        Date property that returns the date representated in the EstNIN.

        :getter: return the date as :py:func:`datetime.date`.
        :setter: update the date given as :py:func:`datetime.date`.
        :modifies: century, checksum
        :raises: :py:exc:`ValueError <ValueError>` if invalid date is given.

        **Usage:**
            >>> from estnin import estnin
            >>> person = estnin(37001011233)
            >>> person.date
            datetime.date(1970, 1, 1)
            >>> person.date = person.date.replace(year=1972, day=22)
            >>> person.date
            datetime.date(1972, 1, 22)
            >>> person
            37201221236
        """
        return self._estnin.date

    @date.setter
    def date(self, value):
        if not isinstance(value, date):
            raise ValueError('invalid date object')

        self.year = value.year
        self.month = value.month
        self.day = value.day
