from typing import Dict
from dicter.expression import Expression, Term, Match_Type, conj, disj, neg

MATCH_SYMBOLS = {
    '$eq': Match_Type.EQUALS,
    '$lt': Match_Type.LESS_THAN,
    '$gt': Match_Type.GREATER_THAN,
    '$le': Match_Type.LESS_THAN_OR_EQUAL,
    '$ge': Match_Type.GREATER_THAN_OR_EQUAL,
    '$substr': Match_Type.SUBSTRING,
    '$startswith': Match_Type.STARTS_WITH,
    '$endswith': Match_Type.ENDS_WITH,
    '$feq': Match_Type.FLOAT_EQUALS,
    '$re': Match_Type.REGEX,
    '$in': Match_Type.IN
}

LOGIC_SYMBOLS = {
    '$and': conj,
    '$or': disj,
    '$not': neg
}


class ParseError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__()
        self.message = msg


def parse(dict: Dict) -> Expression:
    # Make sure input dictionary is valid
    if len(dict) == 0:
        raise ParseError("Cannot parse empty dictionary")
    if len(dict) > 1:
        raise ParseError(
            "Input dictionary should have just one top-level entry.")
    key = next(iter(dict))
    if key in MATCH_SYMBOLS:
        # atomic case - create a term.
        # Example: {'$eq', {'name': 'joe'}}
        entry = dict[key]  # {'name' : 'joe'}
        attr = next(iter(entry))  # 'name'
        value = entry[attr]  # 'joe'
        comp = MATCH_SYMBOLS[key]  # Match_Type.EQUALS
        return Expression(Term(attr, value, comp))
    if key in LOGIC_SYMBOLS:
        # Composite case - recurse.
        # Example: {$or : [{'$eq : {'name': 'Bob'}}, {'$eq' : {'name': 'Sally'}]}
        if key == '$not':  # unary
            return neg(parse(dict[key]))
        else:   # binary - make sure value is a list of two subexpressions
            args = dict[key]
            if not isinstance(args, list):
                raise ParseError(
                    "Parse failed. Expecting a list of arguments to", key, ". Got ", args)
            if len(args) != 2:
                raise ParseError("Expecting 2 arguments to ",
                                 key, ". Got ", args)
            # Apply logical operator to result of parsing subexpressions
            if key == '$or':
                return disj([parse(args[0]), parse(args[1])])
            else:  # must be $and
                return conj([parse(args[0]), parse(args[1])])
    else:
        # Could be atomic but with '$eq' (default) ommitted.  Try that.
        return parse({'$eq': dict})
