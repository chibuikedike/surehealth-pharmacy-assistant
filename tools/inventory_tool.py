# tools/inventory_tool.py

from tools.tool import Tool

from schemas.inventory_schema import (
    SEARCH_INVENTORY_SCHEMA,
    GET_BY_SKU_SCHEMA,
    LOW_STOCK_SCHEMA,
    EXPIRING_SCHEMA,
)


class InventoryTool:
    """
    Exposes inventory functionality to the LLM.
    """

    def __init__(self, inventory_service):
        self.inventory_service = inventory_service

    # =====================================================
    # Tool Functions
    # =====================================================

    def search_inventory(self, query: str):
        return self.inventory_service.search_inventory(query=query)

    def get_medication_by_sku(self, sku: str):
        return self.inventory_service.get_by_sku(sku)

    def get_low_stock(self):
        return self.inventory_service.get_low_stock()

    def get_expiring_medications(self, days: int = 30):
        return self.inventory_service.get_expiring(days)

    # =====================================================
    # Tool Factory
    # =====================================================

    def create_tools(self) -> list[Tool]:
        """
        Create all inventory tools.
        """

        return [

            Tool(
                function=self.search_inventory,
                schema=SEARCH_INVENTORY_SCHEMA,
            ),

            Tool(
                function=self.get_medication_by_sku,
                schema=GET_BY_SKU_SCHEMA,
            ),

            Tool(
                function=self.get_low_stock,
                schema=LOW_STOCK_SCHEMA,
            ),

            Tool(
                function=self.get_expiring_medications,
                schema=EXPIRING_SCHEMA,
            ),

        ]