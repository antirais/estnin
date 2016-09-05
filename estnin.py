#!/usr/bin/env python3
# coding: utf-8

import sys
import datetime

from datetime import date
from collections import namedtuple

__author__ = "Anti Räis"

class _estnin(namedtuple('ESTNIN', 'century date sequence checksum')):
    def __str__(self):
        date = '{:02d}{:02d}{:02d}'.format(self.date.year%100, self.date.month, self.date.day)
        return '{c:d}{d}{s:03d}{cs:d}'.format(c=self.century, d=date, s=self.sequence, cs=self.checksum)

class estnin(object):
    """Estonian national identity number"""

    MIN = 10001010002
    MAX = 89912319991

    MALE = 0
    FEMALE = 1

    def __init__(self, estnin):
        self._estnin = self._validate_format(estnin)

    @classmethod
    def create(cls, sex, birth_date, sequence):
        if not 1800 <= birth_date.year <= 2199:
            raise ValueError('invalid date')

        if not 0 <= sequence <= 999:
            raise ValueError('invalid sequence')

        century = ((birth_date.year-1800)//100)*2+1+bool(sex)
        date = '{:02d}{:02d}{:02d}'.format(birth_date.year%100, birth_date.month, birth_date.day)
        checksum = cls._calculate_checksum("{}{}{:03d}".format(century, date, sequence))
        return cls(str(_estnin(century, birth_date, sequence, checksum)))

    def __repr__(self):
        return str(self._estnin)

    def _validate_format(self, estnin):
        estnin = int(estnin)

        if not self.MIN <= estnin <= self.MAX:
            raise ValueError('invalid value')

        estnin = str(estnin)
        return _estnin(
            int(estnin[0]),
            self._validate_date(estnin),
            int(estnin[7:10]),
            self._validate_checksum(estnin),
        )

    def _validate_date(self, estnin):
        century = int(estnin[0])
        birth_year = int(estnin[1:3])+1800+100*((century-1)//2)
        birth_month = int(estnin[3:5])
        birth_day = int(estnin[5:7])

        return datetime.date(birth_year, birth_month, birth_day)

    def _validate_checksum(self, checksum):
        orig_checksum = int(checksum[-1])
        checksum = self._calculate_checksum(checksum)

        if orig_checksum != checksum:
            raise ValueError('invalid checksum')

        return orig_checksum

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

        if not 1 <= century <= 8:
            raise ValueError('invalid century')

        year = 1800+100*((century-1)//2)+self._estnin.date.year%100
        date = self._estnin.date.replace(year=year)
        self._estnin = self._estnin._replace(century=century, date=date)
        self._update_checksum()

    @property
    def year(self):
        return self._estnin.date.year

    @year.setter
    def year(self, value):
        year = int(value)

        if not 1800 <= year <= 2199:
            raise ValueError('invalid year')

        date = self._estnin.date.replace(year=year)
        century = (year-1800)//100*2+1
        century = century if self.is_male else century+1
        self._estnin = self._estnin._replace(century=century, date=date)
        self._update_checksum()

    @property
    def sequence(self):
        return self._estnin.sequence

    @sequence.setter
    def sequence(self, value):
        sequence = int(value)

        if not 0 <= sequence <= 999:
            raise ValueError('invalid sequence')

        self._estnin = self._estnin._replace(sequence=sequence)
        self._update_checksum()

    @property
    def checksum(self):
        return self._estnin.checksum

    @property
    def date(self):
        return self._estnin.date

if __name__ == '__main__':

    def print_person(person):
        print('='*30)
        print('to str:     %s' % person)
        print('is male:    %s' % person.is_male)
        print('is female:  %s' % person.is_female)
        print('date:       %s' % person.date)
        print('year:       %s' % person.year)
        print('sequence:   %s' % person.sequence)
        print('checksum:   %s' % person.checksum)

    #person = estnin('37611050002')
    person = estnin.create(estnin.MALE, datetime.date(1989, 8, 28), 27)
    print_person(person)

    person = estnin.create(estnin.MALE, date(1800, 1, 1), 0)
    print(person)
    #print(estnin.create(estnin.MALE, datetime.datetime.now(), 1))
    #for i in range(1, 9):
    #    person.century = i
    #    print_person(person)

    #person.century = 1
    #person.sequence = 27
    #print_person(person)

    #person.year = 2200-1
    #print_person(person)

    #print(estnin._calculate_checksum(MAX))
    #for i in range(10001010000, 10001020000, 10):
    #    r = estnin._calculate_checksum(i)
    #    if r != 0:
    #        print("%s%s" % (str(i)[:-1], r))