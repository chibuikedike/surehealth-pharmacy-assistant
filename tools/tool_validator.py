class ToolValidator:
    """
    Validates LLM-generated tool calls before execution.
    """

    def validate(
        self,
        tool_name: str,
        arguments: dict,
    ) -> tuple[bool, str]:
        """
        Return:
            (True, "") if valid
            (False, reason) if invalid
        """

        if tool_name == "search_inventory":
            return self._validate_inventory_search(arguments)

        if tool_name == "search_policy":
            return self._validate_policy_search(arguments)

        if tool_name == "get_medication_by_sku":
            return self._validate_sku_lookup(arguments)

        if tool_name == "get_expiring_medications":
            return self._validate_expiring(arguments)

        if tool_name == "get_low_stock":
            return True, ""

        return False, f"Unknown tool: {tool_name}"

    def _validate_inventory_search(
        self,
        arguments: dict,
    ) -> tuple[bool, str]:

        query = arguments.get("query")

        if not isinstance(query, str):
            return False, "Inventory search requires a query."

        if not query.strip():
            return False, "Inventory search query cannot be empty."

        return True, ""

    def _validate_policy_search(
        self,
        arguments: dict,
    ) -> tuple[bool, str]:

        query = arguments.get("query")

        if query is not None and not isinstance(query, str):
            return False, "Policy query must be text."

        if query is not None and not query.strip():
            return False, "Policy query cannot be empty."

        limit = arguments.get("limit", 5)

        if not isinstance(limit, int):
            return False, "Policy limit must be an integer."

        if limit < 5:
            return False, "Policy limit must be at least 5."

        return True, ""

    def _validate_sku_lookup(
        self,
        arguments: dict,
    ) -> tuple[bool, str]:

        sku = arguments.get("sku")

        if not isinstance(sku, str):
            return False, "SKU must be text."

        if not sku.strip():
            return False, "SKU cannot be empty."

        return True, ""

    def _validate_expiring(
        self,
        arguments: dict,
    ) -> tuple[bool, str]:

        days = arguments.get("days", 30)

        if not isinstance(days, int):
            return False, "Days must be an integer."

        if days < 1:
            return False, "Days must be greater than zero."

        return True, ""
