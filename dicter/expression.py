#!/usr/bin/env python

"""Implements filters expressed using boolean combinations of attributes."""

from typing import Dict, List, Union
from enum import Enum
import re


class Match_Type(Enum):
    """
    Symbolic names for conditions used in Terms.
    """
    EQUALS = 1                  # Exact string match
    LESS_THAN = 2               # Float value less than
    GREATER_THAN = 3            # Float value greater than
    LESS_THAN_OR_EQUAL = 4      # Float value less than or equal
    GREATER_THAN_OR_EQUAL = 5   # Float value greater than or equal
    SUBSTRING = 6               # Substring
    STARTS_WITH = 7             # Starts with
    ENDS_WITH = 8               # Ends with
    FLOAT_EQUALS = 9            # Float values equal
    REGEX = 10                  # Satisfies regex
    IN = 11                     # In


# Dictionary with keys = condition names and values = condition implementations.
CONDITIONS = {
    Match_Type.EQUALS: lambda x, y: x == y,
    Match_Type.LESS_THAN: lambda x, y: float(x) < float(y),
    Match_Type.GREATER_THAN: lambda x, y: float(x) > float(y),
    Match_Type.LESS_THAN_OR_EQUAL: lambda x, y: float(x) <= float(y),
    Match_Type.GREATER_THAN_OR_EQUAL: lambda x, y: float(x) >= float(y),
    Match_Type.SUBSTRING: lambda x, y: x in y,
    Match_Type.STARTS_WITH: lambda x, y: x.startswith(y),
    Match_Type.ENDS_WITH: lambda x, y: x.endswith(y),
    Match_Type.FLOAT_EQUALS: lambda x, y: float(x) == float(y),
    Match_Type.REGEX: lambda x, y: re.compile(y).match(x),
    Match_Type.IN: lambda x, y: x in y
}


class Term:
    """
    Terms represent atomic assertions of the form
    record[key] <condition> value
    where <condition> is one of the values in CONDITIONS.

    For example, a Term with
        key = 'age'
        value = '20'
        type = Match_Type.LESS_THAN
    will match records satisfying
        record['age'] < 20

    Terms are the building blocks for Expressions which are
    boolean combinations of terms.
    """

    def __init__(self, key: str, value: Union[str, List],
                 tp: Match_Type = Match_Type.EQUALS) -> None:
        """
        Create a term making an assertion about the given key.
        Arguments:
            key:    the key whose value will be examined
            value:  comparison value or containing list
            tp:   (optional) the type of comparison. Default is equals.
        """
        self.key = key
        self.value = value
        self.type = tp

    def matches(self, record: Dict) -> bool:
        """
        Return true if the record matches the assertion made by this Term.
        """
        if self.key in record:
            return CONDITIONS[self.type](record[self.key], self.value)
        else:
            return False


class Expression:
    """
    An Expression is a logical combination of terms.
    """

    def __init__(self, term: Term) -> None:
        """
        Create an atomic expression from a Term.
        """
        if term is not None:
            self.matches = term.matches


def __satisfies_any(record: Dict, expressions: List[Expression]):
    """
    Return true if record satisfies any of the Expressions in expressions.
    Arguments:
        record      : record to examine
        expressions : expressions to evaluate to find a match
    Returns:
        true if matches returns true for any expression in expressions when applied to record 
    """
    for exp in expressions:
        if exp.matches(record):
            return True
    return False


def __satisfies_all(record: Dict, expressions: List[Expression]):
    """
    Return true if record satisfies all of the Expressions in expressions.
    Arguments:
        record      : record to examine
        expressions : expressions to evaluate
    Returns:
        true if matches returns true for each expression in expressions when applied to record
    """
    for exp in expressions:
        if not exp.matches(record):
            return False
    return True


def disj(disjuncts: List[Expression]) -> Expression:
    """
    Create an expression that is the logical disjuction of the expressions in disjuncts.
    Arguments:
        disjuncts : expressions to combine using OR
    Returns:
        expression equivalent to disjunction of disjuncts
    """
    ret = Expression(None)
    ret.matches = lambda record: __satisfies_any(record, disjuncts)
    return ret


def conj(conjuncts: List[Expression]) -> Expression:
    """
    Create an expression that is the logical conjunction of the expressions in conjuncts.
    Arguments:
        conjuncts : expressions to combine using AND
    Returns:
        expression equivalent to conjunction of conjuncts
    """
    ret = Expression(None)
    ret.matches = lambda record: __satisfies_all(record, conjuncts)
    return ret


def neg(expression: Expression) -> Expression:
    """
    Create an expression that is the logical negation of expression.
    Arguments:
        expression : expression to negate
    Returns:
        negated expression
    """
    ret = Expression(None)
    ret.matches = lambda record: not expression.matches(record)
    return ret
