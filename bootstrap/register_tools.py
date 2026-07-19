from tools.tool_registry import ToolRegistry

from tools.inventory_tool import InventoryTool
from tools.policy_tool import PolicyTool


def register_tools(
    inventory_service,
    policy_service,
):
    """
    Register every tool available to the AI agent.
    """

    registry = ToolRegistry()

    inventory_tool = InventoryTool(
        inventory_service
    )

    policy_tool = PolicyTool(
        policy_service
    )

    for tool in inventory_tool.create_tools():
        registry.register(tool)

    for tool in policy_tool.create_tools():
        registry.register(tool)

    return registry