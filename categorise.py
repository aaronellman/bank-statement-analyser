
DEFAULTS = {

    # Groceries     
    "woolworths":       "Groceries",
    "checkers":         "Groceries", 
    "pick n pay":       "Groceries",
    "pnp":              "Groceries",
    "spar":             "Groceries",
    "shoprite":         "Groceries",
    "food lovers":      "Groceries",

    # Fuel
    "engen":            "Fuel",
    "shell":            "Fuel",
    "bp ":              "Fuel",
    "caltex":           "Fuel",
    "sasol":            "Fuel",
    "total ":           "Fuel",
    "Fuel":             "Fuel",  

    # Transport
    "uber":             "Transport",
    "bolt":             "Transport",
    "gautrain":         "Transport",
    "myciti":           "Transport",

    # Restaurant
    "nandos":           "Restaurant",
    "kfc":              "Restaurant",
    "steers":           "Restaurant",

    # Pharmacy
    "dischem":          "Pharmacy",
    "clicks":           "Healthcare",

    # Healthcare
    "netcare":          "Health",
    "mediclinic":       "Health",

    # Entertainment
    "netflix":          "Entertainment",
    "showmax":          "Entertainment",
    "spotify":          "Entertainment",
    "dstv":             "Entertainment",
    "steam":            "Entertainment",
    "apple.com":        "Entertainment",
    "google play":      "Entertainment",
    "youtube":          "Entertainment",

    # Shopping
    "takealot":         "Shopping",
    "mr price":         "Shopping",
    "foschini":         "Shopping",
    "truworths":        "Shopping",
    "edgars":           "Shopping",
    "ackermans":        "Shopping",
    "h&m":              "Shopping",

    # Utilities & Telecoms
    "eskom":            "Utilities",
    "city of cape":     "Utilities",
    "city power":       "Utilities",
    "telkom":           "Utilities",
    "vodacom":          "Utilities",
    "mtn":              "Utilities",
    "cell c":           "Utilities",
    "rain":             "Utilities",

    # Insurance
    "discovery":        "Insurance",
    "outsurance":       "Insurance",
    "momentum":         "Insurance",
    "old mutual":       "Insurance",
    "sanlam":           "Insurance",

    # Bank Charges
    "service fee":      "Bank Charges",
    "monthly fee":      "Bank Charges",
    "monthly account":  "Bank Charges",
    "bank charge":      "Bank Charges",
    "admin fee":        "Bank Charges",

    # Cash
    "atm":              "Cash",
    "cash withdrawal":  "Cash",
} 

def categorise(description: str, user_rules: list[dict]) -> str:
    """categorises the transactions based on the users' categories given and the default categories"""