"""
Luxury Clothing Brand Management System
A sophisticated system for managing luxury fashion items, inventory, and customers.
"""

from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum


class Category(Enum):
    """Luxury clothing categories"""
    HAUTE_COUTURE = "Haute Couture"
    READY_TO_WEAR = "Ready-to-Wear"
    ACCESSORIES = "Accessories"
    SHOES = "Shoes"
    JEWELRY = "Jewelry"
    HANDBAGS = "Handbags"


class Product:
    """Represents a luxury fashion product"""
    
    def __init__(self, product_id: str, name: str, category: Category, 
                 price: float, designer: str, description: str = ""):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.designer = designer
        self.description = description
        self.created_at = datetime.now()
    
    def __str__(self):
        return f"{self.name} by {self.designer} - ${self.price:,.2f}"
    
    def __repr__(self):
        return f"Product(id={self.product_id}, name={self.name}, category={self.category.value})"
    
    def to_dict(self) -> Dict:
        """Convert product to dictionary"""
        return {
            'product_id': self.product_id,
            'name': self.name,
            'category': self.category.value,
            'price': self.price,
            'designer': self.designer,
            'description': self.description,
            'created_at': self.created_at.isoformat()
        }


class InventoryItem:
    """Represents inventory for a product"""
    
    def __init__(self, product: Product, quantity: int, size: str = "One Size"):
        self.product = product
        self.quantity = quantity
        self.size = size
        self.last_updated = datetime.now()
    
    def add_stock(self, amount: int):
        """Add stock to inventory"""
        if amount < 0:
            raise ValueError("Amount must be positive")
        self.quantity += amount
        self.last_updated = datetime.now()
    
    def remove_stock(self, amount: int):
        """Remove stock from inventory"""
        if amount < 0:
            raise ValueError("Amount must be positive")
        if amount > self.quantity:
            raise ValueError("Insufficient stock")
        self.quantity -= amount
        self.last_updated = datetime.now()
    
    def __str__(self):
        return f"{self.product.name} (Size: {self.size}) - Qty: {self.quantity}"


class Customer:
    """Represents a luxury brand customer"""
    
    def __init__(self, customer_id: str, name: str, email: str, 
                 phone: str = "", vip_status: bool = False):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone
        self.vip_status = vip_status
        self.purchase_history: List[Dict] = []
        self.created_at = datetime.now()
    
    def add_purchase(self, product: Product, quantity: int, total_amount: float):
        """Record a purchase"""
        purchase = {
            'product_id': product.product_id,
            'product_name': product.name,
            'quantity': quantity,
            'total_amount': total_amount,
            'date': datetime.now().isoformat()
        }
        self.purchase_history.append(purchase)
    
    def get_total_spent(self) -> float:
        """Calculate total amount spent by customer"""
        return sum(purchase['total_amount'] for purchase in self.purchase_history)
    
    def __str__(self):
        vip = " (VIP)" if self.vip_status else ""
        return f"{self.name}{vip} - {self.email}"


class LuxuryBrand:
    """Main luxury clothing brand management system"""
    
    def __init__(self, brand_name: str):
        self.brand_name = brand_name
        self.products: Dict[str, Product] = {}
        self.inventory: Dict[str, List[InventoryItem]] = {}
        self.customers: Dict[str, Customer] = {}
    
    def add_product(self, product: Product):
        """Add a new product to the catalog"""
        if product.product_id in self.products:
            raise ValueError(f"Product {product.product_id} already exists")
        self.products[product.product_id] = product
        self.inventory[product.product_id] = []
    
    def add_inventory(self, product_id: str, quantity: int, size: str = "One Size"):
        """Add inventory for a product"""
        if product_id not in self.products:
            raise ValueError(f"Product {product_id} not found")
        
        product = self.products[product_id]
        
        # Check if inventory item with this size already exists
        for item in self.inventory[product_id]:
            if item.size == size:
                item.add_stock(quantity)
                return
        
        # Create new inventory item
        inventory_item = InventoryItem(product, quantity, size)
        self.inventory[product_id].append(inventory_item)
    
    def get_product(self, product_id: str) -> Optional[Product]:
        """Get product by ID"""
        return self.products.get(product_id)
    
    def list_products(self, category: Optional[Category] = None) -> List[Product]:
        """List all products, optionally filtered by category"""
        products = list(self.products.values())
        if category:
            products = [p for p in products if p.category == category]
        return sorted(products, key=lambda p: p.name)
    
    def add_customer(self, customer: Customer):
        """Add a new customer"""
        if customer.customer_id in self.customers:
            raise ValueError(f"Customer {customer.customer_id} already exists")
        self.customers[customer.customer_id] = customer
    
    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Get customer by ID"""
        return self.customers.get(customer_id)
    
    def process_purchase(self, customer_id: str, product_id: str, 
                        quantity: int, size: str = "One Size"):
        """Process a customer purchase"""
        if customer_id not in self.customers:
            raise ValueError(f"Customer {customer_id} not found")
        if product_id not in self.products:
            raise ValueError(f"Product {product_id} not found")
        
        customer = self.customers[customer_id]
        product = self.products[product_id]
        
        # Find inventory item
        inventory_item = None
        for item in self.inventory[product_id]:
            if item.size == size:
                inventory_item = item
                break
        
        if not inventory_item or inventory_item.quantity < quantity:
            raise ValueError("Insufficient inventory")
        
        # Process purchase
        inventory_item.remove_stock(quantity)
        total_amount = product.price * quantity
        customer.add_purchase(product, quantity, total_amount)
        
        return total_amount
    
    def get_inventory_status(self, product_id: str) -> List[InventoryItem]:
        """Get inventory status for a product"""
        if product_id not in self.inventory:
            raise ValueError(f"Product {product_id} not found")
        return self.inventory[product_id]
    
    def get_vip_customers(self) -> List[Customer]:
        """Get all VIP customers"""
        return [c for c in self.customers.values() if c.vip_status]
    
    def __str__(self):
        return f"{self.brand_name} - {len(self.products)} products, {len(self.customers)} customers"


def initialize_sample_brand() -> LuxuryBrand:
    """Initialize a sample luxury brand with data"""
    brand = LuxuryBrand("The Shahs Luxury Collection")
    
    # Add sample products
    products = [
        Product("HC001", "Silk Evening Gown", Category.HAUTE_COUTURE, 15000.00, 
                "Valentino", "Exquisite hand-embroidered silk evening gown"),
        Product("RTW001", "Cashmere Blazer", Category.READY_TO_WEAR, 3500.00,
                "Armani", "Premium Italian cashmere blazer"),
        Product("BAG001", "Crocodile Leather Handbag", Category.HANDBAGS, 8500.00,
                "Hermès", "Authentic crocodile leather with gold hardware"),
        Product("SHOE001", "Patent Leather Pumps", Category.SHOES, 1200.00,
                "Louboutin", "Classic red sole patent leather pumps"),
        Product("JWL001", "Diamond Tennis Bracelet", Category.JEWELRY, 25000.00,
                "Cartier", "18K white gold with 5ct diamonds"),
        Product("ACC001", "Silk Scarf", Category.ACCESSORIES, 450.00,
                "Versace", "100% silk twill scarf with baroque print"),
    ]
    
    for product in products:
        brand.add_product(product)
        # Add inventory
        if product.category == Category.SHOES:
            for size in ["36", "37", "38", "39", "40"]:
                brand.add_inventory(product.product_id, 3, size)
        elif product.category in [Category.HAUTE_COUTURE, Category.READY_TO_WEAR]:
            for size in ["XS", "S", "M", "L"]:
                brand.add_inventory(product.product_id, 2, size)
        else:
            brand.add_inventory(product.product_id, 5, "One Size")
    
    # Add sample customers
    customers = [
        Customer("C001", "Sofia Martinez", "sofia.m@email.com", "+1-555-0101", True),
        Customer("C002", "James Chen", "james.chen@email.com", "+1-555-0102", True),
        Customer("C003", "Emma Thompson", "emma.t@email.com", "+1-555-0103", False),
        Customer("C004", "Alexander Petrov", "alex.petrov@email.com", "+1-555-0104", True),
    ]
    
    for customer in customers:
        brand.add_customer(customer)
    
    return brand


if __name__ == "__main__":
    # Demo usage
    brand = initialize_sample_brand()
    print(f"\n{'='*60}")
    print(f"  {brand.brand_name}")
    print(f"{'='*60}\n")
    
    print("📋 Product Catalog:")
    print("-" * 60)
    for product in brand.list_products():
        print(f"  • {product}")
    
    print("\n👥 VIP Customers:")
    print("-" * 60)
    for customer in brand.get_vip_customers():
        print(f"  • {customer}")
    
    print(f"\n{'='*60}\n")
