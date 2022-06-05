#!/usr/bin/env python

"""Computes statistics over lists of dictionaries"""

from typing import Dict, List
import numpy as np

PERCENTILES = [5, 10, 25, 50, 75, 90, 95]


class Stats:
    def __init__(self, records: List[Dict], key: str) -> None:
        self.records = records
        self.key = key

    def data(self) -> np.array:
        values = []
        for record in self.records:
            values.append(float(record[self.key]))
        return np.array(values)

    def mean(self) -> float:
        return np.mean(self.data())

    def min(self) -> float:
        return np.min(self.data())

    def max(self) -> float:
        return np.max(self.data())

    def std(self) -> float:
        return np.std(self.data())

    def median(self) -> float:
        return np.median(self.data())

    def sum(self) -> float:
        return np.sum(self.data())

    def percentiles(self) -> Dict:
        ret = {}
        for p in PERCENTILES:
            ret[str(p)] = np.percentile(self.data(), p)
        return ret

    def percentile(self, q: str) -> float:
        arg = str(q)
        if arg not in PERCENTILES:
            ValueError
        return self.percentiles()[arg]

    def n(self) -> int:
        return len(self.data())
