"""
Inventory model module.

This module contains the Inventory class that manages products and implements
the Observer pattern for notifications.
"""

from typing import Dict, List, Optional, Set
from .product import Product


class InventoryObserver:
    """
    Abstract base class for inventory observers.

    Classes that want to be notified of inventory changes should inherit
    from this class and implement the update method.
    """

    def update(self, event_type: str, product: Product, **kwargs) -> None:
        """
        Called when inventory changes occur.

        Args:
            event_type: Type of event (e.g., 'low_stock', 'out_of_stock')
            product: The product that triggered the event
            **kwargs: Additional event data
        """
        raise NotImplementedError("Subclasses must implement update method")


class Inventory:
    """
    Manages the inventory of products and notifies observers of changes.

    This class implements the Observer pattern to notify interested parties
    when inventory levels change.
    """

    def __init__(self) -> None:
        """Initialize a new Inventory instance."""
        self._products: Dict[str, Product] = {}
        self._observers: Set[InventoryObserver] = set()

    def add_observer(self, observer: InventoryObserver) -> None:
        """
        Add an observer to be notified of inventory changes.

        Args:
            observer: Observer to add
        """
        self._observers.add(observer)

    def remove_observer(self, observer: InventoryObserver) -> None:
        """
        Remove an observer from notifications.

        Args:
            observer: Observer to remove
        """
        self._observers.discard(observer)

    def _notify_observers(
        self,
        event_type: str,
        product: Product,
        **kwargs
    ) -> None:
        """
        Notify all observers of an inventory event.

        Args:
            event_type: Type of event
            product: Product that triggered the event
            **kwargs: Additional event data
        """
        for observer in self._observers:
            observer.update(event_type, product, **kwargs)

    def add_product(self, product: Product) -> bool:
        """
        Add a product to the inventory.

        Args:
            product: Product to add

        Returns:
            True if product was added, False if product already exists
        """
        if product.product_id in self._products:
            return False

        self._products[product.product_id] = product
        self._notify_observers("product_added", product)

        # Check for low stock notification
        if product.is_low_stock and product.is_in_stock:
            self._notify_observers("low_stock", product)
        elif not product.is_in_stock:
            self._notify_observers("out_of_stock", product)

        return True

    def remove_product(self, product_id: str) -> bool:
        """
        Remove a product from the inventory.

        Args:
            product_id: ID of product to remove

        Returns:
            True if product was removed, False if product not found
        """
        if product_id not in self._products:
            return False

        product = self._products.pop(product_id)
        self._notify_observers("product_removed", product)
        return True

    def get_product(self, product_id: str) -> Optional[Product]:
        """
        Get a product by ID.

        Args:
            product_id: ID of product to retrieve

        Returns:
            Product if found, None otherwise
        """
        return self._products.get(product_id)

    def update_stock(self, product_id: str, new_quantity: int) -> bool:
        """
        Update the stock quantity for a product.

        Args:
            product_id: ID of product to update
            new_quantity: New quantity value

        Returns:
            True if stock was updated, False if product not found
        """
        product = self.get_product(product_id)
        if not product:
            return False

        old_quantity = product.quantity
        product.quantity = new_quantity

        # Notify observers of stock change
        self._notify_observers(
            "stock_updated",
            product,
            old_quantity=old_quantity,
            new_quantity=new_quantity
        )

        # Check for stock level notifications
        if product.is_low_stock and product.is_in_stock:
            self._notify_observers("low_stock", product)
        elif not product.is_in_stock:
            self._notify_observers("out_of_stock", product)

        return True

    def get_all_products(self) -> List[Product]:
        """Get a list of all products in the inventory."""
        return list(self._products.values())

    def get_products_by_category(self, category: str) -> List[Product]:
        """
        Get all products in a specific category.

        Args:
            category: Category to filter by

        Returns:
            List of products in the specified category
        """
        return [
            product for product in self._products.values()
            if product.category.lower() == category.lower()
        ]

    def get_low_stock_products(self) -> List[Product]:
        """Get all products with low stock levels."""
        return [
            product for product in self._products.values()
            if product.is_low_stock and product.is_in_stock
        ]

    def get_out_of_stock_products(self) -> List[Product]:
        """Get all products that are out of stock."""
        return [
            product for product in self._products.values()
            if not product.is_in_stock
        ]

    def get_total_inventory_value(self) -> float:
        """Calculate the total value of all inventory."""
        return sum(product.get_total_value() for product in self._products.values())

    def get_product_count(self) -> int:
        """Get the total number of different products in inventory."""
        return len(self._products)

    def search_products(self, search_term: str) -> List[Product]:
        """
        Search for products by name or ID.

        Args:
            search_term: Term to search for

        Returns:
            List of products matching the search term
        """
        search_term = search_term.lower()
        return [
            product for product in self._products.values()
            if (search_term in product.name.lower() or
                search_term in product.product_id.lower())
        ]

