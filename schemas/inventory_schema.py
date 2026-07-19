SEARCH_INVENTORY_SCHEMA = {
    "type": "function",
    "function": {
        "name": "search_inventory",
        "description": "Search the pharmacy inventory.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Medication name or search text."
                }
            },
            "required": ["query"]
        }
    }
}
GET_BY_SKU_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_medication_by_sku",
        "description": (
            "Retrieve a medication using its SKU."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "sku": {
                    "type": "string",
                    "description": (
                        "The SKU of the medication."
                    )
                }
            },
            "required": [
                "sku"
            ]
        }
    }
}


LOW_STOCK_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_low_stock",
        "description": (
            "Retrieve all medications whose current stock is less than "
            "or equal to their reorder level."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}


EXPIRING_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_expiring_medications",
        "description": (
            "Retrieve medications that will expire within a specified "
            "number of days."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "days": {
                    "type": "integer",
                    "description": (
                        "Number of days from today to check for upcoming expirations."
                    ),
                    "default": 30
                }
            },
            "required": []
        }
    }
}