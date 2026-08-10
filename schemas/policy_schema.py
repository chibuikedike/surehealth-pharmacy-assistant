SEARCH_POLICY_SCHEMA = {
    "type": "function",
    "function": {
        "name": "search_policy",
        "description": (
            "Search the pharmacy policy document for information about "
            "store procedures, store ownership, contact information, dispensing rules, returns, refunds, "
            "inventory management, customer service, suppliers, or "
            "other operational policies."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "Keyword or phrase to search for in the policy document."
                    )
                },
                "limit": {
                    "type": "integer",
                    "description": (
                        "Maximum number of matching policy sections to return."
                    ),
                    "default": 5,
                    "minimum": 1
                }
            },
            "required": []
        }
    }
}
