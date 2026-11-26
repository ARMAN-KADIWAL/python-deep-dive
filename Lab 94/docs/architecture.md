# Architecture

- Product stores identity, price, stock and category.
- Inventory manages products and publishes events.
- PricingContext switches between regular, discount, bulk and seasonal strategies.
- NotificationLogger, EmailNotificationSystem and DashboardNotificationSystem observe inventory events.
- reports.py provides terminal summaries and CSV export.
- main.py orchestrates the demo and interactive operations.

Stock quantity 1–9 triggers a warning; zero triggers a critical out-of-stock alert. The unit tests cover product validation, inventory operations, observers, price strategies and file output. This is not a production database or email service.
