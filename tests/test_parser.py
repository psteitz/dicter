from dicter.filter import apply
from dicter.parser import parse

TEST_RECORDS = [
    {"name": 'Bob', "age": '12', "weight": '100', "team": 'ducks'},
    {"name": 'Sally', "age": '20', "weight": '110', "team": 'bears'},
    {"name": 'Clarence', "age": '30', "weight": '175', "team": 'ducks'},
    {"name": 'Maddie', "age": '40', "weight": '135', "team": 'aminals'},
    {"name": 'Poo', "age": '50', "weight": '180', "team": 'bears'}
]


def test_equals():
    exp_str = {'team': 'bears'}  # '$eq' omitted
    exp = parse(exp_str)
    bears_records = apply(exp, TEST_RECORDS)
    assert(len(bears_records) == 2)
    assert({"name": 'Sally', "age": '20', "weight": '110',
           "team": 'bears'} in bears_records)
    assert({"name": 'Poo', "age": '50', "weight": '180',
           "team": 'bears'} in bears_records)
    test_exp = {'$eq': {'name': 'Bob'}}  # '$eq' explicit
    bob_records = apply(parse(test_exp), TEST_RECORDS)
    assert(len(bob_records) == 1)
    assert({"name": 'Bob', "age": '12', "weight": '100',
           "team": 'ducks'} in bob_records)


def test_lt():
    exp_str = {'$lt': {'age': 25}}
    exp = parse(exp_str)
    young_records = apply(exp, TEST_RECORDS)
    assert(len(young_records) == 2)
    assert({"name": 'Bob', "age": '12', "weight": '100',
           "team": 'ducks'} in young_records)
    assert({"name": 'Sally', "age": '20', "weight": '110',
           "team": 'bears'} in young_records)


def test_gt():
    exp_str = {'$gt': {'age': 25}}
    exp = parse(exp_str)
    old_records = apply(exp, TEST_RECORDS)
    assert(len(old_records) == 3)
    assert({"name": 'Clarence', "age": '30',
           "weight": '175', "team": 'ducks'} in old_records)
    assert({"name": 'Maddie', "age": '40', "weight": '135',
           "team": 'aminals'} in old_records)
    assert({"name": 'Poo', "age": '50', "weight": '180',
           "team": 'bears'} in old_records)


def test_le():
    exp_str = {'$le': {'age': 20}}
    exp = parse(exp_str)
    young_records = apply(exp, TEST_RECORDS)
    assert(len(young_records) == 2)
    assert({"name": 'Bob', "age": '12', "weight": '100',
           "team": 'ducks'} in young_records)
    assert({"name": 'Sally', "age": '20', "weight": '110',
           "team": 'bears'} in young_records)


def test_ge():
    exp_str = {'$ge': {'age': 30}}
    exp = parse(exp_str)
    old_records = apply(exp, TEST_RECORDS)
    assert(len(old_records) == 3)
    assert({"name": 'Clarence', "age": '30',
           "weight": '175', "team": 'ducks'} in old_records)
    assert({"name": 'Maddie', "age": '40', "weight": '135',
           "team": 'aminals'} in old_records)
    assert({"name": 'Poo', "age": '50', "weight": '180',
           "team": 'bears'} in old_records)


def test_and_or():
    recs = apply(
        {'$and':
            [
                {'$or': [
                    {'$gt': {'age': 20}},
                    {'$gt': {'weight': 105}}
                ]},
                {'$not': {'team': 'aminals'}}
            ]
         }, TEST_RECORDS)
    assert(len(recs) == 3)
    for rec in recs:
        assert(rec['name'] in ['Sally', 'Clarence', 'Poo'])


def test_more_than_2_disjuncts():
    recs = apply(
        {'$or':
         [
             {'$gt': {'age': 20}},
             {'$gt': {'weight': 105}},
             {'team': 'ducks'}
         ]
         }, TEST_RECORDS)
    assert(len(recs) == 5)
