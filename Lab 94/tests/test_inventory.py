import pytest
from inventory_system.models.product import Product
from inventory_system.models.inventory import Inventory
from inventory_system.patterns.pricing_strategy import (
    PricingContext, DiscountPricingStrategy, BulkPricingStrategy,
    SeasonalPricingStrategy,
)
from inventory_system.patterns.notification_system import (
    DashboardNotificationSystem, EmailNotificationSystem, NotificationLogger,
)
from inventory_system.utils.reports import export_inventory


def test_product():
    p = Product("P1", "Mouse", 25, 12)
    p.add_stock(3)
    assert p.remove_stock(5) and p.quantity == 10
    assert not p.remove_stock(11)
    assert p.get_total_value() == 250


@pytest.mark.parametrize("args", [("", "Item", 1, 1), ("P", "", 1, 1),
                                  ("P", "Item", -1, 1), ("P", "Item", 1, -1)])
def test_invalid_product(args):
    with pytest.raises(ValueError):
        Product(*args)


def test_inventory():
    inv = Inventory()
    p = Product("P1", "Mouse", 25, 12, "Electronics")
    assert inv.add_product(p)
    assert not inv.add_product(p)
    assert inv.get_product_count() == 1
    assert inv.search_products("mouse") == [p]
    assert inv.get_products_by_category("electronics") == [p]
    assert inv.get_total_inventory_value() == 300
    assert inv.remove_product("P1") and not inv.remove_product("P1")


def test_observers():
    inv = Inventory()
    dash, email = DashboardNotificationSystem(), EmailNotificationSystem()
    inv.add_observer(dash)
    inv.add_observer(email)
    inv.add_product(Product("P1", "Mouse", 25, 12))
    assert inv.update_stock("P1", 5)
    assert len(inv.get_low_stock_products()) == 1
    assert inv.update_stock("P1", 0)
    assert len(inv.get_out_of_stock_products()) == 1
    assert dash.get_notification_count() == {"critical": 1, "warning": 1, "info": 3}
    assert len(email.get_sent_notifications()) == 2
    inv.remove_observer(email)
    inv.update_stock("P1", 3)
    assert len(email.get_sent_notifications()) == 2


def test_pricing():
    p = Product("P1", "Laptop", 1000)
    ctx = PricingContext()
    assert ctx.calculate_price(p) == 1000
    ctx.set_strategy(DiscountPricingStrategy(10))
    assert ctx.calculate_price(p) == 900
    ctx.set_strategy(BulkPricingStrategy({10: 5, 50: 10, 100: 15}))
    assert ctx.calculate_price(p, quantity=50) == 900
    ctx.set_strategy(SeasonalPricingStrategy(1.2))
    assert ctx.calculate_price(p) == 1200
    assert ctx.get_price_breakdown(Product("P2", "Free", 0))["discount_percentage"] == 0


def test_invalid_bulk():
    with pytest.raises(ValueError):
        BulkPricingStrategy({10: 150})


def test_reports_and_logs(tmp_path):
    inv = Inventory()
    logger = NotificationLogger(str(tmp_path / "inventory.log"))
    inv.add_observer(logger)
    inv.add_product(Product("P1", "Mouse", 25, 5))
    logger.close()
    assert "LOW_STOCK" in (tmp_path / "inventory.log").read_text()
    report = tmp_path / "inventory.csv"
    export_inventory(inv, report)
    assert "P1,Mouse,25,5,General" in report.read_text()
