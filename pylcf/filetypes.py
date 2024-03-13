# The type mentioned is used by the reader to interpret specific bytes.
# When converting the dictionary back to an LCF file, if the found value matches the default, it is left out.

class LcfMapUnit:
    storeType = "single"
    typesDict = {
                1: {"type": "int", "default": 1},
                2: {"type": "int", "default": 20},
                3: {"type": "int", "default": 15},
                11: {"type": "int", "minimum": 0, "maximum": 3},
                31: {"type": "bool", "default": False},
                32: {"type": "string", "default": ""},
                33: {"type": "bool", "default": False},
                34: {"type": "bool", "default": False},
                35: {"type": "bool", "default": False},
                36: {"type": "int", "default": 0},
                37: {"type": "bool", "default": False},
                38: {"type": "int", "default": 0},
                42: {"type": "bool", "optional": True}, # start of useless data.  the bool is missing sometimes
                50: {"type": "string"},
                60: {"type": "string"},
                61: {"type": "string"},
                62: {"type": "string"}, # end of useless data
                71: {"type": "binary"},
                72: {"type": "binary"},
                81: {"type": "event_array"},
                90: {"type": "int"},
                91: {"type": "int", "optional": True}
                }

class LcfMapTree:
    storeType = "list"
    typesDict = {}

class LcfDatabase:
    storeType = "list_rooted"
    typesDict = {}