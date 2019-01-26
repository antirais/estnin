import os
import sys
import copy

from estnin import estnin
from estnin import _estnin
from datetime import date
from timeit import default_timer as timer


def target(count):
    # return [p for p in estnin.create(estnin.FEMALE, date(2199, 12, 1), 0)]
    for _ in range(count):
        #estnin(89912319991, set_checksum=False)
        estnin(estnin.MIN, set_checksum=False)
    return count

def print_person(person):
    print('='*30)
    print('to str:     %s' % person)
    print('is male:    %s' % person.is_male)
    print('is female:  %s' % person.is_female)
    print('date:       %s' % person.date)
    print('year:       %s' % person.year)
    print('month:      %s' % person.month)
    print('day:        %s' % person.day)
    print('sequence:   %s' % person.sequence)
    print('checksum:   %s' % person.checksum)

def performance():
    """
    [*] creating list of 91999 elements took: 3.30743s, 27815.870 elems/s
        baseline

    [*] creating list of 91999 elements took: 3.01910s, 30472.310 elems/s
        __int__ optimization

    [*] creating list of 91999 elements took: 2.83526s, 32448.128 elems/s
        __str__ optimization

    [*] creating list of 91999 elements took: 2.77732s, 33125.086 elems/s
        create does not cast to str
    """
    times = []
    rounds = 20
    for c in range(rounds):
        print("\r[*] round: {}/{}".format(c+1, rounds), end='')
        start = timer()
        persons = target(10000)
        end = timer()
        times.append(end - start)
    print()
    total = sum(times)/len(times)
    print("[*] times (ms):", ' '.join(map(lambda time: '{:.2f}'.format(time*100), times)))
    print("[*] creating list of {} elements took: average {:.3f}ms, {:.3f} elems/s ".format(persons, total*100, persons/total))

def test():
    e = estnin(estnin.MIN)
    print_person(e)
    o = copy.copy(e)
    o.month += 1
    print_person(o)
    print((-e))
    print_person(e)

if __name__ == '__main__':
    try:
        person = estnin.create(estnin.MALE, date(1800, 1, 1), 0)
        print_person(person)

        performance()

        test()

        person = estnin.create(estnin.MALE, date(1800, 1, 1), 0)

        print(_estnin(3, date(1989, 8 ,28), 27, 1))

    except KeyboardInterrupt:
        sys.exit()
