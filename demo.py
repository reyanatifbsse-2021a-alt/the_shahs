#!/usr/bin/env python3
"""
Demo script showcasing The Shahs Luxury Collection Management System
"""

from luxury_brand import initialize_sample_brand, Category


def print_separator():
    """Print a visual separator"""
    print("\n" + "="*70 + "\n")


def demo():
    """Run a demonstration of the luxury brand system"""
    
    # Initialize the brand with sample data
    brand = initialize_sample_brand()
    
    print_separator()
    print("🏆 WELCOME TO THE SHAHS LUXURY COLLECTION")
    print_separator()
    
    # Show brand overview
    print("📊 BRAND OVERVIEW")
    print("-" * 70)
    print(f"Brand Name: {brand.brand_name}")
    print(f"Total Products: {len(brand.products)}")
    print(f"Total Customers: {len(brand.customers)}")
    print(f"VIP Customers: {len(brand.get_vip_customers())}")
    
    print_separator()
    
    # Show product catalog by category
    print("📋 PRODUCT CATALOG BY CATEGORY")
    print("-" * 70)
    for category in Category:
        products = brand.list_products(category)
        if products:
            print(f"\n{category.value}:")
            for product in products:
                print(f"  • {product.name} by {product.designer} - ${product.price:,.2f}")
    
    print_separator()
    
    # Show VIP customers
    print("⭐ VIP CUSTOMERS")
    print("-" * 70)
    for customer in brand.get_vip_customers():
        print(f"  • {customer.name} ({customer.email})")
    
    print_separator()
    
    # Simulate a purchase
    print("💳 SIMULATING A PURCHASE")
    print("-" * 70)
    customer_id = "C001"
    product_id = "SHOE001"
    size = "38"
    quantity = 1
    
    customer = brand.get_customer(customer_id)
    product = brand.get_product(product_id)
    
    print(f"Customer: {customer.name}")
    print(f"Product: {product.name}")
    print(f"Size: {size}")
    print(f"Quantity: {quantity}")
    
    # Check inventory before purchase
    inventory_before = brand.get_inventory_status(product_id)
    qty_before = sum(item.quantity for item in inventory_before if item.size == size)
    print(f"Inventory before: {qty_before} units")
    
    # Process the purchase
    total = brand.process_purchase(customer_id, product_id, quantity, size)
    print(f"\n✅ Purchase successful!")
    print(f"Total Amount: ${total:,.2f}")
    
    # Check inventory after purchase
    inventory_after = brand.get_inventory_status(product_id)
    qty_after = sum(item.quantity for item in inventory_after if item.size == size)
    print(f"Inventory after: {qty_after} units")
    
    print_separator()
    
    # Show customer purchase history
    print(f"🛍️ PURCHASE HISTORY - {customer.name}")
    print("-" * 70)
    for i, purchase in enumerate(customer.purchase_history, 1):
        print(f"\nPurchase #{i}:")
        print(f"  Product: {purchase['product_name']}")
        print(f"  Quantity: {purchase['quantity']}")
        print(f"  Total: ${purchase['total_amount']:,.2f}")
        print(f"  Date: {purchase['date']}")
    
    print(f"\nTotal Spent: ${customer.get_total_spent():,.2f}")
    
    print_separator()
    
    # Calculate total inventory value
    total_value = 0
    total_items = 0
    for product_id, inventory_items in brand.inventory.items():
        product = brand.get_product(product_id)
        for item in inventory_items:
            total_items += item.quantity
            total_value += item.quantity * product.price
    
    print("📈 INVENTORY STATISTICS")
    print("-" * 70)
    print(f"Total Items in Stock: {total_items}")
    print(f"Total Inventory Value: ${total_value:,.2f}")
    
    # Calculate revenue
    total_revenue = sum(
        customer.get_total_spent() 
        for customer in brand.customers.values()
    )
    print(f"Total Revenue: ${total_revenue:,.2f}")
    
    print_separator()
    
    print("✨ Demo completed successfully!")
    print("\nTo interact with the system, run: python3 cli.py")
    print_separator()


if __name__ == "__main__":
    demo()
