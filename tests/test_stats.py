from dicter.stats import Stats

RECORDS = [
    {"a": '10', "b": '100', "c": '1000'},
    {"a": '20', "b": '200', "c": '2000'},
    {"a": '30', "b": '300', "c": '3000'},
    {"a": '40', "b": '400', "c": '4000'},
    {"a": '50', "b": '500', "c": '5000'}
]


def test_mean():
    stats = Stats(RECORDS, "a")
    assert(stats.min() == 10)
    assert(stats.mean() == 30)


def test_percentiles():
    stats = Stats(RECORDS, "b")
    assert(stats.percentiles()['50'] == 300)
    assert(stats.percentiles()['5'] == 120)
    assert(stats.percentiles()['10'] == 140)
    assert(stats.percentiles()['25'] == 200)
    assert(stats.percentiles()['75'] == 400)
    assert(stats.percentiles()['90'] == 460)
    assert(stats.percentiles()['95'] == 480)


def test_min():
    stats = Stats(RECORDS, "c")
    assert(stats.min() == 1000)


def test_max():
    stats = Stats(RECORDS, 'b')
    assert(stats.max() == 500)


def test_n():
    stats = Stats(RECORDS, 'b')
    assert(stats.n() == 5)
