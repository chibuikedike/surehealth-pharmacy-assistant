from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


class InventoryService:
    """
    Handles all inventory-related operations.

    Responsibilities:
        - Load inventory
        - Search inventory
        - Retrieve medication by SKU
        - Find low-stock items
        - Find expiring medications
        - Reload inventory
    """

    SEARCH_COLUMNS = [
        "SKU",
        "Medication Name",
        "Category",
        "Strength",
        "Dosage Form",
        "Brand Name",
        "Supplier",
        "Warehouse Location",
        "Batch Number",
    ]

    DATE_COLUMN = "Expiry Date"

    STOCK_COLUMN = "Current Stock"

    REORDER_COLUMN = "Reorder Level"

    def __init__(self, inventory_file: str):
        self.inventory_file = Path(inventory_file)
        self.df = self._load_inventory()

    # ==========================================================
    # Internal Methods
    # ==========================================================

    def _load_inventory(self) -> pd.DataFrame:
        """
        Load inventory from CSV.
        """

        if not self.inventory_file.exists():
            raise FileNotFoundError(
                f"Inventory file not found: {self.inventory_file}"
            )

        df = pd.read_csv(self.inventory_file)

        df.columns = df.columns.str.strip()

        if self.DATE_COLUMN in df.columns:
            df[self.DATE_COLUMN] = pd.to_datetime(
                df[self.DATE_COLUMN],
                errors="coerce",
            )

        return df

    # ==========================================================
    # Public Methods
    # ==========================================================

    def reload_inventory(self) -> None:
        """
        Reload inventory from disk.
        """
        self.df = self._load_inventory()

    def get_all(self) -> list[dict[str, Any]]:
        """
        Return every inventory item.
        """
        return self.df.to_dict(orient="records")

    def get_by_sku(self, sku: str) -> dict[str, Any] | None:
        """
        Retrieve a medication using its SKU.
        """

        result = self.df[
            self.df["SKU"]
            .astype(str)
            .str.lower()
            == sku.lower()
        ]

        if result.empty:
            return None

        return result.iloc[0].to_dict()

    def search_inventory(
    self,
    query: str | None = None,
    category: str | None = None,
    brand_name: str | None = None,
    strength: str | None = None,
    dosage_form: str | None = None,
    supplier: str | None = None,
    warehouse_location: str | None = None,
    batch_number: str | None = None,
    limit: int = 10,
    ) -> list[dict[str, Any]]:
        """
        Search across searchable columns.
        """

        query = query.strip().lower()

        if not query:
            return []

        mask = pd.Series(False, index=self.df.index)

        for column in self.SEARCH_COLUMNS:

            if column not in self.df.columns:
                continue

            mask |= (
                self.df[column]
                .fillna("")
                .astype(str)
                .str.lower()
                .str.contains(query, na=False)
            )

        results = self.df[mask]

        if limit:
            results = results.head(limit)

        return results.to_dict(orient="records")

    def get_low_stock(self) -> list[dict[str, Any]]:
        """
        Return medications whose stock is at or below
        their reorder level.
        """

        if (
            self.STOCK_COLUMN not in self.df.columns
            or self.REORDER_COLUMN not in self.df.columns
        ):
            return []

        results = self.df[
            self.df[self.STOCK_COLUMN]
            <= self.df[self.REORDER_COLUMN]
        ]

        return results.to_dict(orient="records")

    def get_expiring(
        self,
        days: int = 30,
    ) -> list[dict[str, Any]]:
        """
        Return medications expiring within the
        specified number of days.
        """

        if self.DATE_COLUMN not in self.df.columns:
            return []

        today = pd.Timestamp.today().normalize()

        end_date = today + pd.Timedelta(days=days)

        results = self.df[
            (self.df[self.DATE_COLUMN] >= today)
            & (self.df[self.DATE_COLUMN] <= end_date)
        ]

        return results.to_dict(orient="records")