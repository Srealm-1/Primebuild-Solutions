from django.db import models

class Product(models.Model):
    """
    Represents a product in your store's inventory.
    Includes essential details like name, description, price, and stock.
    """

    name = models.CharField(
        max_length=255,
        help_text="Name of the product."
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Optional detailed description of the product."
    )
    sku = models.CharField(
        max_length=100,
        # unique=True,
        help_text="Unique stock keeping unit (SKU) for product identification."
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price of the product."
    )
    stock_quantity = models.PositiveIntegerField(
        default=0,
        help_text="Number of items currently in stock."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the product is currently active and available for purchase."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the product was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the product was last updated."
    )

    class Meta:
        # Ordering, table name, and verbose names are optional
        ordering = ['-created_at']  # Newest products first
        verbose_name = "Product"
        verbose_name_plural = "Products"
        # db_table = "products"  # Uncomment to override the default table name

    def __str__(self):
        """String representation of a Product object."""
        return f"{self.name} (SKU: {self.sku})"

    def get_price_with_tax(self, tax_rate=0.15):
        """
        Returns the product price plus a specified tax rate.
        Default tax_rate = 15% (0.15).
        """
        return round(self.price * (1 + tax_rate), 2)


