SEARCH_POLICY_SCHEMA = {
    "type": "function",
    "function": {
        "name": "search_policy",
        "description": (
            "Search the internal pharmacy policy document to retrieve "
            "relevant policy sections. Use this tool when the user asks "
            "about internal procedures, rules, returns, refunds, "
            "dispensing, inventory procedures, suppliers, customer "
            "service, store ownership, contact information, or other "
            "operational policies. Search using the key concepts from "
            "the user's question. Do not require the user's exact "
            "wording to appear in the document."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "The main topic, keywords, or concepts from the "
                        "user's question to search for in the policy document."
                    )
                },
                "limit": {
                    "type": "integer",
                    "description": (
                        "Maximum number of relevant policy sections to return."
                    ),
                    "default": 5,
                    "minimum": 1,
                    "maximum": 10
                }
            },
            "required": ["query"]
        }
    }
}
