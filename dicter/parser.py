from typing import Dict
from dicter.expression import Expression, Term, Match_Type, conj, disj, neg

# Map condition symbols to match types.
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

# Map logic symbols to logical operators
LOGIC_SYMBOLS = {
    '$and': conj,
    '$or': disj,
    '$not': neg
}


class Parse_error(Exception):
    """
    Exception raised when an error occurs parsing an input dictionary.
    """

    def __init__(self, msg: str = "") -> None:
        """
        Create a ParseError with the given error string.
        Arguments:
            msg : message string. Defaults to empty string.
        """
        super().__init__()
        self.message = msg


def parse(dict: Dict) -> Expression:
    """
    Create an expression from a dict.
    Arguments:
        dict : dictionary representing a filter expression
    Raises:
        Parse_error if dict is not valid
    """
    # Make sure input dictionary is valid
    if len(dict) == 0:
        raise Parse_error("Cannot parse empty dictionary")
    if len(dict) > 1:
        raise Parse_error(
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
                msg = "Parse failed. Expecting a list of arguments to " + \
                    key + ". Got " + str(type(args))
                raise Parse_error(msg)
            if len(args) < 2:
                msg = "Expecting a list of length at least 2 arguments for " + \
                    key + " Got " + str(len(args))
                raise Parse_error(msg)
            # Apply logical operator to result of parsing subexpressions
            if key == '$or':
                return disj(list(map(lambda arg: parse(arg), args)))
                # return disj([parse(args[0]), parse(args[1])])
            else:  # must be $and
                return conj(list(map(lambda arg: parse(arg), args)))
    else:
        # Could be atomic but with '$eq' (default) ommitted.  Try that.
        return parse({'$eq': dict})
