#!/usr/bin/env python3
# coding: utf-8

import sys
import datetime

from datetime import date
from collections import namedtuple

__author__ = "Anti Räis"

class _estnin(namedtuple('ESTNIN', 'century date sequence checksum')):
    def __str__(self):
        return str(int(self))

    def __int__(self):
        date = self.date
        return self.century*10**10+date.year%100*10**8+date.month*10**6+date.day*10**4+self.sequence*10+self.checksum

class estnin(object):
    """Estonian national identity number"""

    MIN = 10001010002
    MAX = 89912319991

    MALE = 0
    FEMALE = 1

    def __init__(self, estnin, set_checksum=False):
        self._estnin = self._validate_format(estnin, set_checksum=set_checksum)

    @classmethod
    def create(cls, sex, birth_date, sequence):
        cls._validate_year(birth_date.year)
        cls._validate_sequence(sequence)

        century = ((birth_date.year-1800)//100)*2+1+bool(sex)
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
        days, sequence = divmod(self.sequence+other, 1000)
        date = self.date + datetime.timedelta(days=days)
        self._validate_year(date.year)
        century = self._calculate_century(date.year)
        self._estnin = self._estnin._replace(century=century, date=date, sequence=sequence)
        self._update_checksum()
        return self

    def __sub__(self, other):
        return self+(-other)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            value = estnin(self)
            self += 1
            return value
        except ValueError as e:
            raise StopIteration

    def __reversed__(self):
        try:
            while True:
                value = estnin(self)
                self -= 1
                yield value
        except ValueError as e:
            raise StopIteration

    @classmethod
    def _validate_year(self, year):
        if not 1800 <= year <= 2199:
            raise ValueError('invalid date')

    @classmethod
    def _validate_sequence(self, sequence):
        if not 0 <= sequence <= 999:
            raise ValueError('invalid sequence')

    @classmethod
    def _validate_century(self, century):
        if not 1 <= century <= 8:
            raise ValueError('invalid century')

    def _calculate_century(self, year):
        century = (year-1800)//100*2+1
        return century if self.is_male else century+1

    @classmethod
    def _calculate_year(self, century, year):
        return 1800+100*((century-1)//2)+year%100

    def _validate_format(self, estnin, set_checksum=False):
        estnin = int(estnin)

        if set_checksum:
            if not self.MIN//10*10 <= estnin <= self.MAX//10*10+9:
                raise ValueError('invalid value')
        else:
            if not self.MIN <= estnin <= self.MAX:
                raise ValueError('invalid value')


        if set_checksum:
            checksum = self._calculate_checksum(estnin)
        else:
            checksum = self._validate_checksum(estnin)

        estnin = str(estnin)
        return _estnin(
            int(estnin[0]),
            self._validate_date(estnin),
            int(estnin[7:10]),
            checksum,
        )

    def _validate_date(self, estnin):
        century = int(estnin[0])
        birth_year = self._calculate_year(century, int(estnin[1:3]))
        birth_month = int(estnin[3:5])
        birth_day = int(estnin[5:7])

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
        checksum = sum(int(k)*v for k, v in zip(_estnin, [1,2,3,4,5,6,7,8,9,1])) % 11

        if checksum == 10:
            checksum = sum(int(k)*v for k, v in zip(_estnin, [3,4,5,6,7,8,9,1,2,3])) % 11
            checksum = 0 if checksum == 10 else checksum

        return checksum

    @property
    def is_male(self):
        return self._estnin.century % 2 == 1

    @property
    def is_female(self):
        return self._estnin.century % 2 == 0

    @property
    def century(self):
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
        return self._estnin.date.month

    @month.setter
    def month(self, value):
        month = int(value)
        date = self._estnin.date.replace(month=month)
        self._estnin = self._estnin._replace(date=date)
        self._update_checksum()

    @property
    def day(self):
        return self._estnin.date.day

    @day.setter
    def day(self, value):
        day = int(value)
        date = self._estnin.date.replace(day=day)
        self._estnin = self._estnin._replace(date=date)
        self._update_checksum()

    @property
    def sequence(self):
        return self._estnin.sequence

    @sequence.setter
    def sequence(self, value):
        sequence = int(value)

        self._validate_sequence(sequence)
        self._estnin = self._estnin._replace(sequence=sequence)
        self._update_checksum()

    @property
    def checksum(self):
        return self._estnin.checksum

    @property
    def date(self):
        return self._estnin.date
