#!/usr/bin/env python3
# coding: utf-8


import os
import sys
import pytest

sys.path.insert(0, os.path.abspath('..'))
from estnin import estnin
from datetime import date

def test_create_validates_year():
    with pytest.raises(ValueError):
        estnin.create(estnin.MALE, date(1799, 1, 1), 0)

    with pytest.raises(ValueError):
        estnin.create(estnin.MALE, date(2200, 1, 1), 0)

def test_create_validates_sequence():
    with pytest.raises(ValueError):
        estnin.create(estnin.MALE, date(1800, 1, 1), -1)

    with pytest.raises(ValueError):
        estnin.create(estnin.MALE, date(2199, 1, 1), 1000)

def test_create_sets_century():
    person = estnin.create(estnin.MALE, date(1800, 1, 1), 0)
    assert person.century == 1

    person = estnin.create(estnin.FEMALE, date(1800, 1, 1), 0)
    assert person.century == 2

    person = estnin.create(estnin.MALE, date(2100, 1, 1), 0)
    assert person.century == 7

    person = estnin.create(estnin.FEMALE, date(2100, 1, 1), 0)
    assert person.century == 8

def test_create_sets_checksum():
    person = estnin.create(estnin.MALE, date(1800, 1, 1), 0)
    assert person.checksum == 2

def test_argument_length_is_checked():
    with pytest.raises(ValueError):
        estnin("00000000000")

def test_argument_length_is_checked():
    with pytest.raises(ValueError):
        estnin("00000000000")

def test_argument_must_be_an_integer():
    with pytest.raises(ValueError):
        estnin("gyymmddsssc")

def test_century_value_is_checked():
    with pytest.raises(ValueError):
        estnin(90001010000)

def test_date_month_value_is_checked():
    with pytest.raises(ValueError):
        estnin(10013010000)

def test_date_day_value_is_checked():
    with pytest.raises(ValueError):
        estnin(10001990000)

    with pytest.raises(ValueError):
        estnin(10002290000)

def test_checksum_value_is_checked():
    with pytest.raises(ValueError):
        estnin(10001010009)

def test_is_male_returns_true_if_male():
    assert estnin(10001010002).is_male

def test_is_female_returns_true_if_female():
    assert estnin(20001010003).is_female

def test_is_male_and_is_female_are_exclusive():
    assert estnin(10001010002).is_male
    assert not estnin(10001010002).is_female

    assert estnin(20001010003).is_female
    assert not estnin(20001010003).is_male

def test_checksum_returns_valid_value():
    assert estnin._calculate_checksum(10001010002) == 2

def test_checksum_recalculates_if_value_is_10():
    assert estnin._calculate_checksum(10001010214) == 4

def test_checksum_is_zero_if_recalculated_value_is_10():
    assert estnin._calculate_checksum(10001010080) == 0

def test_century_property_returns_value():
    assert estnin(10001010002).century == 1

def test_updating_century_property_is_validated():
    p = estnin(10001010002)

    with pytest.raises(ValueError):
        p.century = 0

    with pytest.raises(ValueError):
        p.century = 9

    assert p.century == 1

def test_updating_century_property_type_is_validated():
    p = estnin(10001010002)

    with pytest.raises(ValueError):
        p.century = 'x'

    assert p.century == 1

def test_updating_century_property_updates_checksum():
    p = estnin(10001010002)
    p.century = 2
    assert p.century == 2
    assert p.checksum == 3

def test_year_returns_valid_value():
    assert estnin(14201010005).year == 1842

def test_setting_year_checks_type():
    with pytest.raises(ValueError):
        estnin(14201010005).year = 'invalid'

def test_setting_year_checks_range():
    with pytest.raises(ValueError):
        estnin(14201010005).year = 1799

    with pytest.raises(ValueError):
        estnin(14201010005).year = 2200

def test_setting_year_updates_value():
    p = estnin(10001010002)
    p.year = 2000
    assert p.year == 2000

def test_setting_year_updates_century():
    p = estnin(10001010002)
    p.year = 2000
    assert p.century == 5

def test_setting_year_updates_checksum():
    p = estnin(10001010002)
    p.year = 2000
    assert p.checksum == 6

def test_sequence_returns_valid_value():
    assert estnin(10001010002).sequence == 0

def test_settings_sequence_updates_value():
    p = estnin(10001010002)
    p.sequence = 10
    assert p.sequence == 10

def test_setting_sequence_checks_type():
    with pytest.raises(ValueError):
        estnin(10001010002).sequence = 'invalid'

def test_setting_sequence_checks_range():
    with pytest.raises(ValueError):
        estnin(10001010002).sequence = -1

    with pytest.raises(ValueError):
        estnin(10001010002).sequence = 1000

def test_setting_sequence_updates_checksum():
    p = estnin(10001010002)
    p.sequence = 1
    assert p.checksum == 3

def test_date_property_returns_date_obj():
    assert estnin(37611050002).date == date(1976, 11, 5)

def test_estnin_has_int_representation():
    assert int(estnin(10001010002)) == 10001010002

def test_estnin_has_lt_comparison():
    assert estnin(10001010002) < estnin(10001010013)

def test_estnin_has_le_comparison():
    assert estnin(10001010002) <= estnin(10001010013)
    assert estnin(10001010002) <= estnin(10001010002)

def test_estnin_has_eq_comparison():
    assert estnin(10001010002) == estnin(10001010002)

def test_estnin_has_ne_comparison():
    assert estnin(10001010002) != estnin(10001010013)

def test_estnin_has_gt_comparison():
    assert estnin(10001010013) > estnin(10001010002)

def test_estnin_has_ge_comparison():
    assert estnin(10001010013) >= estnin(10001010002)
    assert estnin(10001010002) >= estnin(10001010002)

def test_inverting_estnin_changes_sex():
    person = estnin.create(estnin.MALE, date(2000, 1, 1), 0)
    assert person.is_male

    ~person
    assert person.is_female

    person = estnin.create(estnin.FEMALE, date(2000, 1, 1), 0)
    assert person.is_female

    ~person
    assert person.is_male

def test_adding_integers_increments_sequence():
    p = estnin(10001010002)
    p += 1
    assert p.sequence == 1
    assert p.checksum == 3

def test_adding_integers_increments_date():
    p = estnin.create(estnin.MALE, date(1999, 12, 31), 999)
    p += 1
    assert p.sequence == 0
    assert p.date.day == 1
    assert p.date.month == 1
    assert p.date.year == 2000
    assert p.is_male
    assert p.century == 5
