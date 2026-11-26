"""Inventory management application and interactive menu."""
import argparse
from inventory_system.models.product import Product
from inventory_system.models.inventory import Inventory
from inventory_system.patterns.pricing_strategy import (
    PricingContext, RegularPricingStrategy, DiscountPricingStrategy,
    BulkPricingStrategy, SeasonalPricingStrategy,
)
from inventory_system.patterns.notification_system import (
    NotificationLogger, EmailNotificationSystem, DashboardNotificationSystem,
)
from inventory_system.utils.reports import print_inventory, export_inventory


def build_inventory():
    inventory = Inventory()
    logger = NotificationLogger()
    email = EmailNotificationSystem()
    dashboard = DashboardNotificationSystem()
    for observer in (logger, email, dashboard):
        inventory.add_observer(observer)
    return inventory, logger, email, dashboard


def show_prices(product):
    context = PricingContext()
    strategies = [RegularPricingStrategy(), DiscountPricingStrategy(10),
                  BulkPricingStrategy({10: 5, 50: 10, 100: 15}),
                  SeasonalPricingStrategy(1.2)]
    print("\nPricing strategies (per unit, order quantity 50):")
    for strategy in strategies:
        context.set_strategy(strategy)
        result = context.get_price_breakdown(product, quantity=50)
        print(f"{result['strategy_name']}: ${result['calculated_price']:.2f}")


def run_demo(inventory, email, dashboard):
    print("=== Inventory Management System ===")
    for product in (Product("P001", "Laptop", 1000, 20, "Electronics"),
                    Product("P002", "Mouse", 25, 8, "Electronics"),
                    Product("P003", "Keyboard", 50, 0, "Electronics")):
        inventory.add_product(product)
    inventory.update_stock("P001", 5)
    inventory.update_stock("P002", 0)
    print_inventory(inventory)
    show_prices(inventory.get_product("P001"))
    print("\nDashboard counts:", dashboard.get_notification_count())
    print("Simulated email alerts:", len(email.get_sent_notifications()))
    print("Report saved:", export_inventory(inventory))
    print("Lab 94 completed successfully!")


def interactive_menu(inventory, dashboard):
    while True:
        print("\n1. Add product\n2. Update stock\n3. List products")
        print("4. Search\n5. Pricing\n6. Alerts\n7. Export CSV")
        print("8. Remove product\n9. Exit")
        choice = input("Choose: ").strip()
        try:
            if choice == "1":
                product = Product(input("ID: "), input("Name: "),
                                  float(input("Price: ")), int(input("Quantity: ")),
                                  input("Category: ") or "General")
                print("Added" if inventory.add_product(product) else "Duplicate ID")
            elif choice == "2":
                found = inventory.update_stock(input("ID: "), int(input("New quantity: ")))
                print("Updated" if found else "Product not found")
            elif choice == "3":
                print_inventory(inventory)
            elif choice == "4":
                for product in inventory.search_products(input("Search: ")):
                    print(product)
            elif choice == "5":
                product = inventory.get_product(input("ID: "))
                if product:
                    show_prices(product)
                else:
                    print("Product not found")
            elif choice == "6":
                for alert in dashboard.get_notifications():
                    print(alert['severity'], alert['message'])
            elif choice == "7":
                print("Report saved:", export_inventory(inventory))
            elif choice == "8":
                print("Removed" if inventory.remove_product(input("ID: ")) else "Not found")
            elif choice == "9":
                break
            else:
                print("Invalid choice")
        except ValueError as error:
            print("Invalid input:", error)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interactive", action="store_true")
    args = parser.parse_args()
    inventory, logger, email, dashboard = build_inventory()
    try:
        if args.interactive:
            interactive_menu(inventory, dashboard)
        else:
            run_demo(inventory, email, dashboard)
    except (EOFError, KeyboardInterrupt):
        print("\nExiting")
    finally:
        logger.close()


if __name__ == "__main__":
    main()
