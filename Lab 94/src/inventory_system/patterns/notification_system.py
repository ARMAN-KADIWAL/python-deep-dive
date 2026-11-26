"""
Notification system implementing the Observer pattern.

This module provides concrete observers for handling different types
of inventory notifications.
"""

import logging
from datetime import datetime
from typing import List, Dict, Any
from ..models.inventory import InventoryObserver
from ..models.product import Product


class NotificationLogger(InventoryObserver):
    """
    Observer that logs inventory events to a file.

    This class demonstrates the Observer pattern by logging
    all inventory changes to a log file.
    """

    def __init__(self, log_file: str = "inventory.log") -> None:
        """
        Initialize the notification logger.

        Args:
            log_file: Path to the log file
        """
        self._log_file = log_file

        self._logger = logging.Logger(__name__, logging.INFO)
        handler = logging.FileHandler(log_file, encoding="utf-8")
        handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        ))
        self._logger.addHandler(handler)

    def close(self) -> None:
        for handler in self._logger.handlers[:]:
            self._logger.removeHandler(handler)
            handler.close()

    def update(self, event_type: str, product: Product, **kwargs) -> None:
        """
        Log inventory events.

        Args:
            event_type: Type of event
            product: Product involved in the event
            **kwargs: Additional event data
        """

        if event_type == "product_added":
            message = f"Product added: {product.name} (ID: {product.product_id})"
        elif event_type == "product_removed":
            message = f"Product removed: {product.name} (ID: {product.product_id})"
        elif event_type == "stock_updated":
            old_qty = kwargs.get('old_quantity', 0)
            new_qty = kwargs.get('new_quantity', 0)
            message = (f"Stock updated for {product.name}: "
                      f"{old_qty} -> {new_qty}")
        elif event_type == "low_stock":
            message = (f"LOW STOCK ALERT: {product.name} "
                      f"(Quantity: {product.quantity})")
        elif event_type == "out_of_stock":
            message = f"OUT OF STOCK: {product.name}"
        else:
            message = f"Unknown event: {event_type} for {product.name}"

        self._logger.info(f"{event_type.upper()}: {message}")


class EmailNotificationSystem(InventoryObserver):
    """
    Observer that simulates email notifications for critical inventory events.

    In a real implementation, this would integrate with an email service.
    """

    def __init__(self, admin_email: str = "admin@company.com") -> None:
        """
        Initialize the email notification system.

        Args:
            admin_email: Email address to send notifications to
        """
        self._admin_email = admin_email
        self._sent_notifications: List[Dict[str, Any]] = []

    def update(self, event_type: str, product: Product, **kwargs) -> None:
        """
        Send email notifications for critical events.

        Args:
            event_type: Type of event
            product: Product involved in the event
            **kwargs: Additional event data
        """
        # Only send emails for critical events
        if event_type in ["low_stock", "out_of_stock"]:
            self._send_email_notification(event_type, product, **kwargs)

    def _send_email_notification(
        self,
        event_type: str,
        product: Product,
        **kwargs
    ) -> None:
        """
        Simulate sending an email notification.

        Args:
            event_type: Type of event
            product: Product involved in the event
            **kwargs: Additional event data
        """
        timestamp = datetime.now()

        if event_type == "low_stock":
            subject = f"Low Stock Alert: {product.name}"
            body = (f"Product {product.name} (ID: {product.product_id}) "
                   f"is running low on stock.\n"
                   f"Current quantity: {product.quantity}\n"
                   f"Please reorder soon.")
        elif event_type == "out_of_stock":
            subject = f"Out of Stock Alert: {product.name}"
            body = (f"Product {product.name} (ID: {product.product_id}) "
                   f"is now out of stock.\n"
                   f"Immediate reordering required.")
        else:
            return

        # Simulate email sending (in real implementation, use email service)
        notification = {
            'timestamp': timestamp,
            'to': self._admin_email,
            'subject': subject,
            'body': body,
            'event_type': event_type,
            'product_id': product.product_id
        }

        self._sent_notifications.append(notification)
        print(f"[SIMULATED EMAIL] {subject}")
        print(f"To: {self._admin_email}")
        print(f"Body: {body}")
        print("-" * 50)

    def get_sent_notifications(self) -> List[Dict[str, Any]]:
        """Get a list of all sent notifications."""
        return self._sent_notifications.copy()

    def clear_notifications(self) -> None:
        """Clear the notification history."""
        self._sent_notifications.clear()


class DashboardNotificationSystem(InventoryObserver):
    """
    Observer that maintains real-time dashboard notifications.

    This class collects notifications for display in a dashboard interface.
    """

    def __init__(self, max_notifications: int = 100) -> None:
        """
        Initialize the dashboard notification system.

        Args:
            max_notifications: Maximum number of notifications to keep
        """
        self._max_notifications = max_notifications
        self._notifications: List[Dict[str, Any]] = []

    def update(self, event_type: str, product: Product, **kwargs) -> None:
        """
        Add notification to dashboard.

        Args:
            event_type: Type of event
            product: Product involved in the event
            **kwargs: Additional event data
        """
        notification = {
            'timestamp': datetime.now(),
            'event_type': event_type,
            'product_id': product.product_id,
            'product_name': product.name,
            'message': self._create_message(event_type, product, **kwargs),
            'severity': self._get_severity(event_type)
        }

        self._notifications.insert(0, notification)  # Add to beginning

        # Keep only the most recent notifications
        if len(self._notifications) > self._max_notifications:
            self._notifications = self._notifications[:self._max_notifications]

    def _create_message(
        self,
        event_type: str,
        product: Product,
        **kwargs
    ) -> str:
        """
        Create a user-friendly message for the notification.

        Args:
            event_type: Type of event
            product: Product involved in the event
            **kwargs: Additional event data

        Returns:
            Formatted message string
        """
        if event_type == "product_added":
            return f"New product '{product.name}' added to inventory"
        elif event_type == "product_removed":
            return f"Product '{product.name}' removed from inventory"
        elif event_type == "stock_updated":
            old_qty = kwargs.get('old_quantity', 0)
            new_qty = kwargs.get('new_quantity', 0)
            return f"Stock for '{product.name}' updated: {old_qty} → {new_qty}"
        elif event_type == "low_stock":
            return f"Low stock warning: '{product.name}' ({product.quantity} remaining)"
        elif event_type == "out_of_stock":
            return f"Out of stock: '{product.name}'"
        else:
            return f"Event '{event_type}' for product '{product.name}'"

    def _get_severity(self, event_type: str) -> str:
        """
        Determine the severity level of an event.

        Args:
            event_type: Type of event

        Returns:
            Severity level string
        """
        severity_map = {
            'out_of_stock': 'critical',
            'low_stock': 'warning',
            'product_added': 'info',
            'product_removed': 'info',
            'stock_updated': 'info'
        }
        return severity_map.get(event_type, 'info')

    def get_notifications(self, severity: str = None) -> List[Dict[str, Any]]:
        """
        Get notifications, optionally filtered by severity.

        Args:
            severity: Optional severity filter ('critical', 'warning', 'info')

        Returns:
            List of notifications
        """
        if severity:
            return [n for n in self._notifications if n['severity'] == severity]
        return self._notifications.copy()

    def get_critical_notifications(self) -> List[Dict[str, Any]]:
        """Get only critical notifications."""
        return self.get_notifications('critical')

    def get_warning_notifications(self) -> List[Dict[str, Any]]:
        """Get only warning notifications."""
        return self.get_notifications('warning')

    def clear_notifications(self) -> None:
        """Clear all notifications."""
        self._notifications.clear()

    def get_notification_count(self) -> Dict[str, int]:
        """
        Get count of notifications by severity.

        Returns:
            Dictionary with counts for each severity level
        """
        counts = {'critical': 0, 'warning': 0, 'info': 0}
        for notification in self._notifications:
            severity = notification['severity']
            counts[severity] += 1
        return counts

