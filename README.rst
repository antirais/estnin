======
estnin
======

Python library for working with Estonian national identity numbers.

Install
=======

Use ``pip`` to install::

	pip install estnin

Runnig tests
============
::

	python setup.py test

Usage
=====

Create a new ``estnin`` instance::

	>>> from estnin import estnin
	>>> person = estnin(37001011233)
	>>> print(person.sequence)
	>>> 123
	>>> print(estnin(estnin.MIN))
	>>> 10001010002
	>>> person = estnin.create(estnin.MALE, date(1970, 1, 1), 1)
	>>> print(person)
	>>> 37001010018

str()
"""""
::

	>>> assert estnin(37001010018) == "37001010018"

int()
"""""
::

	>>> assert estnin(37001010018) == 37001010018

<, ==, >
""""""""
::

	>>> assert estnin(37001011233) < estnin(estnin.MAX)
	>>> assert estnin(37001011233) > estnin(estnin.MIN)
	>>> assert estnin(37001011233) == estnin(37001011233)

negation
""""""""
Negation is defined as changing the sex from male to female or vice verca.
::

	>>> assert -estnin(37001011233) == estnin(47001011234)

addition and substraction
"""""""""""""""""""""""""
Adding an integer increments the sequence value by given amount. If the sum of the sequence and the number given is greater than 999, then the day is incremented and the remainder is set as the new sequence value. The day, month and year values are incremented in chronological order until the defined maximum value is reached. If the year crosses the century boundary, then the century digit is also properly set.
::

	>>> assert estnin(37001011244) == estnin(37001011233)+1
	>>> assert estnin(37001011244) == estnin(37001011255)-1
	>>> # Create new person
	>>> person = estnin.create(estnin.MALE, date(1999, 12, 31), 999)
	>>> print(person)
	>>> 39912319997
	>>> assert estnin(50001010006) == person+1

iteration
"""""""""
Iterating over a given ``estnin`` instance creates new objects.
::

	>>> people = [p for _, p in zip(range(3), estnin(37001011233))]
	>>> print(' '.join(map(str, people)))
	>>> 37001011233 37001011244 37001011255

Iterating in a reverse order can be done by using the method ``reversed()``::

	>>> people = [p for _, p in zip(range(3), reversed(estnin(37001011233)))]
	>>> print(' '.join(map(str, people)))
	>>> 37001011233 37001011222 37001011211

properties
""""""""""
::

	>>> person = estnin.create(estnin.MALE, date(1970, 1, 2), 3)
	>>> person
	37001020036
	>>> person.century
	3
	>>> person.year
	1970
	>>> person.month
	1
	>>> person.day
	2
	>>> person.sequence
	3
	>>> person.checksum
	6
	>>> person.date
	datetime.date(1970, 1, 2)
