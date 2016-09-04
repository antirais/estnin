#!/usr/bin/env python3
# coding: utf-8

import sys
import datetime

from datetime import date
from collections import namedtuple

__author__ = "Anti Räis"

_estnin = namedtuple('ESTNIN', 'century year month day sequence checksum')

# estnin e.g Estonian national identity number
class estnin(object):

    def __init__(self, estnin):
        self._estnin        = str(self._validate_format(estnin))
        #self._testnin       = _estnin(
        #                          int(estnin[0]),
        #                          int(estnin[1:3]),
        #                          int(estnin[3:5]),
        #                          int(estnin[5:7]),
        #                          int(estnin[7:10]),
        #                          int(estnin[10]),
        #                    )
        self._century       = self._validate_century(self._estnin[0])
        self._date          = self._validate_date(self._estnin[1:7])
        self._sequence      = int(self._estnin[7:10])
        self._checksum      = self._validate_checksum(self._estnin[10])

    def __repr__(self):
        return self._estnin
        #return '{century:d}{year:0d}{month:0d}{day:0d}{sequence:03d}{checksum:d}'.format(**self._testnin._asdict())

    def _validate_format(self, esnin):
        try:
            esnin = int(esnin)
        except ValueError as e:
            raise ValueError("not an integer")

        if len(str(esnin)) != 11:
            raise ValueError("invalid length")

        return esnin

    def _validate_century(self, century):
        century = int(century)

        if century < 1 or century > 8:
            raise ValueError("invalid century")

        return century

    def _validate_date(self, date):
        birth_year = int(date[0:2])+1800+100*((self._century-1)//2)
        birth_month = int(date[2:4])
        birth_day = int(date[4:6])

        return datetime.date(birth_year, birth_month, birth_day)

    @classmethod
    def _calculate_checksum(self, estnin):
        estnin = str(estnin)

        checksum = 0
        for i, k in zip(estnin, [1,2,3,4,5,6,7,8,9,1]):
            checksum += int(i)*k
        checksum %= 11

        if checksum == 10:
            checksum = 0
            for i, k in zip(estnin, [3,4,5,6,7,8,9,1,2,3]):
                checksum += int(i)*k
            checksum %= 11

            if checksum == 10:
                checksum = 0

        return checksum

    def _validate_checksum(self, checksum):
        orig_checksum = int(checksum)
        checksum = self._calculate_checksum(self._estnin)

        if orig_checksum != checksum:
            raise ValueError("invalid checksum")

        return orig_checksum

    def _update_checksum(self):
        self._checksum = self._calculate_checksum(self._estnin)
        self._estnin = self._estnin[:10]+str(self._checksum)

    @property
    def is_male(self):
        return self._century % 2 == 1

    @property
    def is_female(self):
        return self._century % 2 == 0

    @property
    def century(self):
        return self._century

    @century.setter
    def century(self, value):
        self._century = self._validate_century(value)
        self._estnin = str(self._century)+self._estnin[1:]
        self._update_checksum()

    @property
    def year(self):
        return self._date.year

    @year.setter
    def year(self, value):
        year = int(value)

        if year < 1800 or year >= 2200:
            raise ValueError("invalid year")

        self._date = self._date.replace(year=year)
        self._estnin = self._estnin[0]+self._date.strftime("%y%m%d")+self._estnin[7:]

        century = (year-1800)//100*2+1
        self._century = century if self.is_male else century+1
        self._estnin = str(self._century)+self._estnin[1:]

        self._update_checksum()

    @property
    def sequence(self):
        return self._sequence

    @sequence.setter
    def sequence(self, value):
        try:
            sequence = int(value)

            if sequence < 0 or sequence > 999:
                raise ValueError

            self._sequence = sequence
            self._estnin = self._estnin[:7]+"{:03d}".format(sequence)
            self._update_checksum()
        except ValueError:
            raise ValueError("invalid sequence")

    @property
    def checksum(self):
        return self._checksum

    def sex(self, male='M', female='F'):
        return male if self.is_male else female

    @property
    def date(self):
        return self._date

if __name__ == '__main__':

    def print_person(person):
        print("="*30)
        print("to str:     %s" % person)
        print("is male:    %s" % person.is_male)
        print("is female:  %s" % person.is_female)
        print("sex:        %s" % person.sex())
        print("date:       %s" % person.date)
        print("year:       %s" % person.year)
        print("sequence:   %s" % person.sequence)
        print("checksum:   %s" % person.checksum)
        #print(person._testnin)

    person = estnin("37611050002")
    person.sequence = 1
    print_person(person)

    #person.century = 0
    #person.sequence = 27
    #person.year = 2200-1
    #print_person(person)

    print(estnin._calculate_checksum(person))
    #for i in range(10001010000, 10001020000, 10):
    #    r = estnin._calculate_checksum(i)
    #    if r != 0:
    #        print("%s%s" % (str(i)[:-1], r))