from dicter.expression import Expression, Term
from dicter.parser import parse
from typing import Union, Dict, List


def apply(expression: Union[Expression, Term, Dict], records: List[Dict]) -> List[Dict]:
    """
    Filter records for those that match the expression.
    Arguments:
        expression  : expression to satisfy, or dict representing an expression
        records     : records to examine
    Returns:
        sublist of records that satisfy the expression

    If expression is a dict, the dict is parsed to create an expression to apply.  
    """
    if isinstance(expression, dict):  # Parse the expression
        return apply(parse(expression), records)
    else:
        return [record for record in records if expression.matches(record)]
