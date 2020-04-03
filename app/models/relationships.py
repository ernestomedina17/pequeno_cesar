from neomodel import StructuredRel, IntegerProperty


class HasPizzaRel(StructuredRel):
    units = IntegerProperty(required=True)


class HasComplementRel(StructuredRel):
    units = IntegerProperty(required=True)


class HasDrinkRel(StructuredRel):
    units = IntegerProperty(required=True)


class HasSauceRel(StructuredRel):
    units = IntegerProperty(required=True)
