import csv
from pathlib import Path
from dicter.stats import Stats
from dicter.expression import Expression, Match_Type, Term, conj, disj, neg
from dicter.filter import apply

FOOBAR = Term("foo", "bar")
BARBAZ = Term("bar", "baz")
FOO_LT = Term("foo", 10, Match_Type.LESS_THAN)
FOO_GT = Term("foo", 10, Match_Type.GREATER_THAN)
FOO_LE = Term("foo", 10, Match_Type.LESS_THAN_OR_EQUAL)
FOO_GE = Term("foo", 10, Match_Type.GREATER_THAN_OR_EQUAL)
FOO_SUBSTR = Term("foo", "everyone", Match_Type.SUBSTRING)
FOO_STARTS_WITH = Term("foo", "every", Match_Type.STARTS_WITH)
FOO_ENDS_WITH = Term("foo", "one", Match_Type.ENDS_WITH)
FOO_IN = Term("foo", ["bar", "baz"], Match_Type.IN)
SAMPLE_DATA_DIR = Path(__file__).resolve().parent.parent / 'examples'
IN_FILE = SAMPLE_DATA_DIR / 'weather.csv'


def test_atomic():
    exp = Expression(FOOBAR)
    assert(not exp.matches({"foo": "bas"}))
    assert(exp.matches({"foo": "bar"}))
    assert(not exp.matches({"fo": "bas"}))

    exp = Expression(FOO_LT)
    assert(not exp.matches({"foo": 10}))
    assert(not exp.matches({"foo": "10"}))
    assert(exp.matches({"foo": 9}))

    exp = Expression(FOO_GT)
    assert(not exp.matches({"foo": 10}))
    assert(not exp.matches({"foo": "10"}))
    assert(exp.matches({"foo": 11}))

    exp = Expression(FOO_LE)
    assert(exp.matches({"foo": 10}))
    assert(exp.matches({"foo": "10.0"}))
    assert(exp.matches({"foo": 9}))

    exp = Expression(FOO_GE)
    assert(exp.matches({"foo": 10}))
    assert(exp.matches({"foo": "10"}))
    assert(exp.matches({"foo": 11}))

    exp = Expression(FOO_SUBSTR)
    assert(exp.matches({"foo": "ve"}))
    assert(not exp.matches({"foo": "10"}))
    assert(exp.matches({"foo": "everyone"}))

    exp = Expression(FOO_STARTS_WITH)
    assert(exp.matches({"foo": "everyone"}))
    assert(not exp.matches({"foo": "er"}))
    assert(exp.matches({"foo": "everyone"}))

    exp = Expression(FOO_ENDS_WITH)
    assert(exp.matches({"foo": "everyone"}))
    assert(not exp.matches({"foo": ""}))
    assert(exp.matches({"foo": "everyone"}))

    exp = Expression(FOO_IN)
    assert(exp.matches({"foo": "bar"}))
    assert(not exp.matches({"foo": "bee"}))
    assert(exp.matches({"foo": "baz"}))


def test_conj():
    con = conj([FOOBAR, BARBAZ])
    assert(con.matches({"foo": "bar", "bar": "baz"}))
    assert(not con.matches({"foo": "bar", "bar": "bat"}))
    assert(not con.matches({"foo": "bas", "bas": "baz"}))


def test_disj():
    dis = disj([FOOBAR, BARBAZ])
    assert(dis.matches({"foo": "bar", "bar": "baz"}))
    assert(dis.matches({"foo": "bar", "bar": "bat"}))
    assert(not dis.matches({"foo": "bas", "bas": "baz"}))


def test_negate():
    con = conj([FOOBAR, BARBAZ])
    dis = disj([FOOBAR, BARBAZ])
    neg_conj = neg(con)
    neg_disj = neg(dis)
    assert(not neg_disj.matches({"foo": "bar", "bar": "baz"}))
    assert(not neg_disj.matches({"foo": "bar", "bar": "bat"}))
    assert(neg_disj.matches({"foo": "bas", "bas": "baz"}))
    assert(not neg_conj.matches({"foo": "bar", "bar": "baz"}))
    assert(neg_conj.matches({"foo": "bar", "bar": "bat"}))
    assert(neg_conj.matches({"foo": "bas", "bas": "baz"}))


def test_apply():
    records = [
        {"a": '10', "b": '12', "c": '13'},
        {"a": '20', "b": '21', "c": '23'},
        {"a": '30', "b": '31', "c": '33'},
        {"a": '40', "b": '41', "c": '43'},
        {"a": '50', "b": '51', "c": '53'}
    ]
    # a = 10 or b = 21 or c = 33 - should get first three records
    aterm = Term('a', '10')
    bterm = Term('b', '21')
    cterm = Term('c', '33')
    first_three = disj(
        [Expression(aterm), Expression(bterm), Expression(cterm)])
    filtered_records = apply(first_three, records)
    assert(len(filtered_records) == 3)
    assert(records[0] in filtered_records)
    assert(records[1] in filtered_records)
    assert(records[2] in filtered_records)

    # a is 10 or 20 and b is 21 or 31 - second row
    aterm2 = Term('a', '20')
    bterm2 = Term('b', '31')
    second_only = conj(
        [disj([aterm, aterm2]),
         disj([bterm, bterm2])])
    filtered_records = apply(second_only, records)
    assert(len(filtered_records) == 1)
    assert(records[1] in filtered_records)

    # a is greater than 10 and b is less than 50 - three middle rows
    aterm3 = Term('a', 10, Match_Type.GREATER_THAN)
    bterm3 = Term('b', 50, Match_Type.LESS_THAN)
    middle_three = conj([aterm3, bterm3])
    filtered_records = apply(middle_three, records)
    assert(len(filtered_records) == 3)
    assert(records[1] in filtered_records)
    assert(records[2] in filtered_records)
    assert(records[3] in filtered_records)


def test_apply_with_stats():
    input_records = csv.DictReader(open(IN_FILE))
    filtered_records = apply(
        {'$and':
            [
                {'$or': [
                    {'$gt': {'Data.Temperature.Max Temp': 100}},
                    {'$gt': {'Data.Temperature.Min Temp': 80}}
                ]},
                {'$not': {'Station.State': 'Arizona'}}
            ]
         }, input_records)
    assert(Stats(filtered_records, 'Data.Temperature.Max Temp').n() == 94)
    assert(Stats(filtered_records, 'Data.Temperature.Min Temp').percentile(90) == 82.0)
