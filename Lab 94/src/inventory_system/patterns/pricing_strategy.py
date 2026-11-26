"""
Pricing strategy module implementing the Strategy pattern.

This module provides different pricing strategies that can be applied
to products dynamically.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from ..models.product import Product


class PricingStrategy(ABC):
    """
    Abstract base class for pricing strategies.

    This class defines the interface that all pricing strategies must implement.
    """

    @abstractmethod
    def calculate_price(self, product: Product, **kwargs) -> float:
        """
        Calculate the price for a product.

        Args:
            product: Product to calculate price for
            **kwargs: Additional parameters for price calculation

        Returns:
            Calculated price
        """
        pass

    @abstractmethod
    def get_strategy_name(self) -> str:
        """Get the name of this pricing strategy."""
        pass


class RegularPricingStrategy(PricingStrategy):
    """Standard pricing strategy that returns the base price."""

    def calculate_price(self, product: Product, **kwargs) -> float:
        """Return the regular price of the product."""
        return product.price

    def get_strategy_name(self) -> str:
        """Get the strategy name."""
        return "Regular Pricing"


class DiscountPricingStrategy(PricingStrategy):
    """Pricing strategy that applies a percentage discount."""

    def __init__(self, discount_percentage: float) -> None:
        """
        Initialize the discount pricing strategy.

        Args:
            discount_percentage: Discount percentage (0-100)

        Raises:
            ValueError: If discount percentage is invalid
        """
        if not 0 <= discount_percentage <= 100:
            raise ValueError("Discount percentage must be between 0 and 100")
        self._discount_percentage = discount_percentage

    def calculate_price(self, product: Product, **kwargs) -> float:
        """Calculate discounted price."""
        discount_amount = product.price * (self._discount_percentage / 100)
        return product.price - discount_amount

    def get_strategy_name(self) -> str:
        """Get the strategy name."""
        return f"Discount Pricing ({self._discount_percentage}% off)"


class BulkPricingStrategy(PricingStrategy):
    """Pricing strategy that applies bulk discounts based on quantity."""

    def __init__(self, bulk_thresholds: Dict[int, float]) -> None:
        """
        Initialize the bulk pricing strategy.

        Args:
            bulk_thresholds: Dictionary mapping quantity thresholds to discount percentages
                           Example: {10: 5.0, 50: 10.0, 100: 15.0}
        """
        if any(t <= 0 or not 0 <= d <= 100 for t, d in bulk_thresholds.items()):
            raise ValueError("Invalid bulk thresholds or discounts")
        self._bulk_thresholds = dict(sorted(bulk_thresholds.items(), reverse=True))

    def calculate_price(self, product: Product, **kwargs) -> float:
        """
        Calculate bulk price based on quantity.

        Args:
            product: Product to price
            **kwargs: Must include 'quantity' parameter

        Returns:
            Price per unit with bulk discount applied
        """
        quantity = kwargs.get('quantity', 1)

        # Find the applicable bulk discount
        discount_percentage = 0.0
        for threshold, discount in self._bulk_thresholds.items():
            if quantity >= threshold:
                discount_percentage = discount
                break

        discount_amount = product.price * (discount_percentage / 100)
        return product.price - discount_amount

    def get_strategy_name(self) -> str:
        """Get the strategy name."""
        return "Bulk Pricing"


class SeasonalPricingStrategy(PricingStrategy):
    """Pricing strategy that applies seasonal adjustments."""

    def __init__(self, seasonal_multiplier: float) -> None:
        """
        Initialize the seasonal pricing strategy.

        Args:
            seasonal_multiplier: Multiplier for seasonal pricing (e.g., 1.2 for 20% increase)
        """
        if seasonal_multiplier <= 0:
            raise ValueError("Seasonal multiplier must be positive")
        self._seasonal_multiplier = seasonal_multiplier

    def calculate_price(self, product: Product, **kwargs) -> float:
        """Calculate seasonal price."""
        return product.price * self._seasonal_multiplier

    def get_strategy_name(self) -> str:
        """Get the strategy name."""
        multiplier_percent = (self._seasonal_multiplier - 1) * 100
        if multiplier_percent > 0:
            return f"Seasonal Pricing (+{multiplier_percent:.1f}%)"
        else:
            return f"Seasonal Pricing ({multiplier_percent:.1f}%)"


class PricingContext:
    """
    Context class for pricing strategies.

    This class allows switching between different pricing strategies
    at runtime, demonstrating the Strategy pattern.
    """

    def __init__(self, strategy: PricingStrategy = None) -> None:
        """
        Initialize the pricing context.

        Args:
            strategy: Initial pricing strategy to use
        """
        self._strategy = strategy or RegularPricingStrategy()

    def set_strategy(self, strategy: PricingStrategy) -> None:
        """
        Set the pricing strategy.

        Args:
            strategy: New pricing strategy to use
        """
        self._strategy = strategy

    def get_strategy(self) -> PricingStrategy:
        """Get the current pricing strategy."""
        return self._strategy

    def calculate_price(self, product: Product, **kwargs) -> float:
        """
        Calculate price using the current strategy.

        Args:
            product: Product to calculate price for
            **kwargs: Additional parameters for price calculation

        Returns:
            Calculated price
        """
        return self._strategy.calculate_price(product, **kwargs)

    def get_price_breakdown(self, product: Product, **kwargs) -> Dict[str, Any]:
        """
        Get detailed price breakdown.

        Args:
            product: Product to analyze
            **kwargs: Additional parameters

        Returns:
            Dictionary with price breakdown information
        """
        original_price = product.price
        calculated_price = self.calculate_price(product, **kwargs)

        return {
            'original_price': original_price,
            'calculated_price': calculated_price,
            'discount_amount': original_price - calculated_price,
            'discount_percentage': ((original_price - calculated_price) / original_price) * 100 if original_price else 0.0,
            'strategy_name': self._strategy.get_strategy_name(),
            'quantity': kwargs.get('quantity', 1)
        }

