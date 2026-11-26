"""
Product model module.

This module contains the Product class that represents items in the inventory.
"""

from datetime import datetime


class Product:
    """
    Represents a product in the inventory system.

    This class follows PEP 8 guidelines and includes proper documentation,
    type hints, and naming conventions.
    """

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        quantity: int = 0,
        category: str = "General"
    ) -> None:
        """
        Initialize a new Product instance.

        Args:
            product_id: Unique identifier for the product
            name: Product name
            price: Product price
            quantity: Initial quantity in stock
            category: Product category

        Raises:
            ValueError: If price is negative or product_id is empty
        """
        if not product_id.strip():
            raise ValueError("Product ID cannot be empty")
        if not name.strip():
            raise ValueError("Product name cannot be empty")
        if price < 0:
            raise ValueError("Price cannot be negative")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")

        self._product_id = product_id.strip()
        self._name = name.strip()
        self._price = price
        self._quantity = quantity
        self._category = category.strip()
        self._created_at = datetime.now()
        self._last_updated = datetime.now()

    @property
    def product_id(self) -> str:
        """Get the product ID."""
        return self._product_id

    @property
    def name(self) -> str:
        """Get the product name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set the product name."""
        if not value.strip():
            raise ValueError("Product name cannot be empty")
        self._name = value.strip()
        self._last_updated = datetime.now()

    @property
    def price(self) -> float:
        """Get the product price."""
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        """Set the product price."""
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value
        self._last_updated = datetime.now()

    @property
    def quantity(self) -> int:
        """Get the current quantity in stock."""
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        """Set the quantity in stock."""
        if value < 0:
            raise ValueError("Quantity cannot be negative")
        self._quantity = value
        self._last_updated = datetime.now()

    @property
    def category(self) -> str:
        """Get the product category."""
        return self._category

    @category.setter
    def category(self, value: str) -> None:
        """Set the product category."""
        self._category = value.strip()
        self._last_updated = datetime.now()

    @property
    def is_in_stock(self) -> bool:
        """Check if the product is currently in stock."""
        return self._quantity > 0

    @property
    def is_low_stock(self) -> bool:
        """Check if the product has low stock (less than 10 units)."""
        return self._quantity < 10

    def add_stock(self, amount: int) -> None:
        """
        Add stock to the product.

        Args:
            amount: Amount to add to current stock

        Raises:
            ValueError: If amount is negative
        """
        if amount < 0:
            raise ValueError("Cannot add negative stock")
        self._quantity += amount
        self._last_updated = datetime.now()

    def remove_stock(self, amount: int) -> bool:
        """
        Remove stock from the product.

        Args:
            amount: Amount to remove from current stock

        Returns:
            True if stock was successfully removed, False if insufficient stock

        Raises:
            ValueError: If amount is negative
        """
        if amount < 0:
            raise ValueError("Cannot remove negative stock")
        if amount > self._quantity:
            return False
        self._quantity -= amount
        self._last_updated = datetime.now()
        return True

    def get_total_value(self) -> float:
        """Calculate the total value of stock for this product."""
        return self._price * self._quantity

    def __str__(self) -> str:
        """Return string representation of the product."""
        return (
            f"Product(ID: {self._product_id}, Name: {self._name}, "
            f"Price: ${self._price:.2f}, Quantity: {self._quantity}, "
            f"Category: {self._category})"
        )

    def __repr__(self) -> str:
        """Return detailed string representation of the product."""
        return (
            f"Product(product_id='{self._product_id}', name='{self._name}', "
            f"price={self._price}, quantity={self._quantity}, "
            f"category='{self._category}')"
        )

    def __eq__(self, other) -> bool:
        """Check equality based on product ID."""
        if not isinstance(other, Product):
            return False
        return self._product_id == other._product_id

    def __hash__(self) -> int:
        """Return hash based on product ID."""
        return hash(self._product_id)
