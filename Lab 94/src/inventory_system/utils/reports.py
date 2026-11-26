"""Inventory reporting utilities."""
import csv


def print_inventory(inventory):
    print("\nID | Name | Price | Quantity | Category")
    for product in inventory.get_all_products():
        print(f"{product.product_id} | {product.name} | "
              f"${product.price:.2f} | {product.quantity} | {product.category}")
    print(f"Products: {inventory.get_product_count()}")
    print(f"Total inventory value: ${inventory.get_total_inventory_value():.2f}")


def export_inventory(inventory, filename="inventory_report.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Price", "Quantity", "Category"])
        for product in inventory.get_all_products():
            writer.writerow([product.product_id, product.name, product.price,
                             product.quantity, product.category])
    return filename
