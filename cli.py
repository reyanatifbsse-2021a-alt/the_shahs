#!/usr/bin/env python3
"""
Command Line Interface for The Shahs Luxury Clothing Brand
"""

import sys
from luxury_brand import (
    LuxuryBrand, Product, Customer, Category, 
    initialize_sample_brand
)


class LuxuryBrandCLI:
    """CLI for luxury brand management"""
    
    def __init__(self, brand: LuxuryBrand):
        self.brand = brand
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*70)
        print(f"  {self.brand.brand_name.upper()}")
        print("="*70)
        print("\n📱 Main Menu:")
        print("  1. View Product Catalog")
        print("  2. View Products by Category")
        print("  3. Check Product Inventory")
        print("  4. View Customers")
        print("  5. View VIP Customers")
        print("  6. Process Purchase")
        print("  7. View Customer Purchase History")
        print("  8. Brand Statistics")
        print("  0. Exit")
        print("-"*70)
    
    def view_catalog(self):
        """Display all products"""
        print("\n" + "="*70)
        print("  PRODUCT CATALOG")
        print("="*70)
        products = self.brand.list_products()
        if not products:
            print("  No products available.")
            return
        
        for product in products:
            print(f"\n  ID: {product.product_id}")
            print(f"  Name: {product.name}")
            print(f"  Designer: {product.designer}")
            print(f"  Category: {product.category.value}")
            print(f"  Price: ${product.price:,.2f}")
            if product.description:
                print(f"  Description: {product.description}")
            print("  " + "-"*66)
    
    def view_by_category(self):
        """Display products by category"""
        print("\n📂 Select Category:")
        categories = list(Category)
        for i, cat in enumerate(categories, 1):
            print(f"  {i}. {cat.value}")
        
        try:
            choice = int(input("\nEnter category number: "))
            if 1 <= choice <= len(categories):
                category = categories[choice - 1]
                print(f"\n{'='*70}")
                print(f"  {category.value.upper()}")
                print("="*70)
                products = self.brand.list_products(category)
                if not products:
                    print(f"  No products in {category.value} category.")
                else:
                    for product in products:
                        print(f"  • {product}")
            else:
                print("  ❌ Invalid category number.")
        except ValueError:
            print("  ❌ Invalid input.")
    
    def check_inventory(self):
        """Check inventory for a product"""
        product_id = input("\nEnter Product ID: ").strip().upper()
        try:
            product = self.brand.get_product(product_id)
            if not product:
                print(f"  ❌ Product {product_id} not found.")
                return
            
            print(f"\n📦 Inventory for {product.name}:")
            print("-"*70)
            inventory_items = self.brand.get_inventory_status(product_id)
            if not inventory_items:
                print("  No inventory available.")
            else:
                for item in inventory_items:
                    print(f"  Size {item.size}: {item.quantity} units")
        except ValueError as e:
            print(f"  ❌ Error: {e}")
    
    def view_customers(self):
        """Display all customers"""
        print("\n" + "="*70)
        print("  CUSTOMERS")
        print("="*70)
        if not self.brand.customers:
            print("  No customers registered.")
            return
        
        for customer in self.brand.customers.values():
            vip = "⭐ VIP" if customer.vip_status else "Regular"
            print(f"\n  ID: {customer.customer_id}")
            print(f"  Name: {customer.name}")
            print(f"  Email: {customer.email}")
            print(f"  Status: {vip}")
            print(f"  Total Spent: ${customer.get_total_spent():,.2f}")
            print("  " + "-"*66)
    
    def view_vip_customers(self):
        """Display VIP customers"""
        print("\n" + "="*70)
        print("  ⭐ VIP CUSTOMERS")
        print("="*70)
        vip_customers = self.brand.get_vip_customers()
        if not vip_customers:
            print("  No VIP customers.")
            return
        
        for customer in vip_customers:
            print(f"\n  {customer.name}")
            print(f"  Email: {customer.email}")
            print(f"  Total Spent: ${customer.get_total_spent():,.2f}")
            print(f"  Purchases: {len(customer.purchase_history)}")
            print("  " + "-"*66)
    
    def process_purchase(self):
        """Process a customer purchase"""
        print("\n" + "="*70)
        print("  💳 PROCESS PURCHASE")
        print("="*70)
        
        customer_id = input("\nCustomer ID: ").strip().upper()
        product_id = input("Product ID: ").strip().upper()
        size = input("Size (or press Enter for 'One Size'): ").strip() or "One Size"
        
        try:
            quantity = int(input("Quantity: "))
            
            total = self.brand.process_purchase(customer_id, product_id, quantity, size)
            
            customer = self.brand.get_customer(customer_id)
            product = self.brand.get_product(product_id)
            
            print("\n  ✅ Purchase completed successfully!")
            print(f"  Customer: {customer.name}")
            print(f"  Product: {product.name}")
            print(f"  Quantity: {quantity}")
            print(f"  Size: {size}")
            print(f"  Total Amount: ${total:,.2f}")
            
        except ValueError as e:
            print(f"  ❌ Error: {e}")
        except Exception as e:
            print(f"  ❌ Unexpected error: {e}")
    
    def view_purchase_history(self):
        """View customer purchase history"""
        customer_id = input("\nEnter Customer ID: ").strip().upper()
        customer = self.brand.get_customer(customer_id)
        
        if not customer:
            print(f"  ❌ Customer {customer_id} not found.")
            return
        
        print(f"\n{'='*70}")
        print(f"  PURCHASE HISTORY - {customer.name}")
        print("="*70)
        
        if not customer.purchase_history:
            print("  No purchase history.")
            return
        
        for i, purchase in enumerate(customer.purchase_history, 1):
            print(f"\n  Purchase #{i}")
            print(f"  Product: {purchase['product_name']}")
            print(f"  Quantity: {purchase['quantity']}")
            print(f"  Amount: ${purchase['total_amount']:,.2f}")
            print(f"  Date: {purchase['date']}")
            print("  " + "-"*66)
        
        print(f"\n  Total Spent: ${customer.get_total_spent():,.2f}")
    
    def show_statistics(self):
        """Display brand statistics"""
        print("\n" + "="*70)
        print("  📊 BRAND STATISTICS")
        print("="*70)
        
        print(f"\n  Total Products: {len(self.brand.products)}")
        print(f"  Total Customers: {len(self.brand.customers)}")
        print(f"  VIP Customers: {len(self.brand.get_vip_customers())}")
        
        # Calculate total inventory
        total_inventory = 0
        for items in self.brand.inventory.values():
            total_inventory += sum(item.quantity for item in items)
        print(f"  Total Inventory Items: {total_inventory}")
        
        # Products by category
        print("\n  Products by Category:")
        for category in Category:
            count = len(self.brand.list_products(category))
            if count > 0:
                print(f"    • {category.value}: {count}")
        
        # Total revenue
        total_revenue = sum(
            customer.get_total_spent() 
            for customer in self.brand.customers.values()
        )
        print(f"\n  Total Revenue: ${total_revenue:,.2f}")
    
    def run(self):
        """Run the CLI"""
        print("\n👑 Welcome to The Shahs Luxury Collection Management System")
        
        while True:
            self.display_menu()
            choice = input("\nSelect an option: ").strip()
            
            if choice == "1":
                self.view_catalog()
            elif choice == "2":
                self.view_by_category()
            elif choice == "3":
                self.check_inventory()
            elif choice == "4":
                self.view_customers()
            elif choice == "5":
                self.view_vip_customers()
            elif choice == "6":
                self.process_purchase()
            elif choice == "7":
                self.view_purchase_history()
            elif choice == "8":
                self.show_statistics()
            elif choice == "0":
                print("\n👋 Thank you for using The Shahs Luxury Collection!")
                print("   Goodbye!\n")
                break
            else:
                print("\n  ❌ Invalid option. Please try again.")
            
            input("\nPress Enter to continue...")


def main():
    """Main entry point"""
    # Initialize with sample data
    brand = initialize_sample_brand()
    
    # Run CLI
    cli = LuxuryBrandCLI(brand)
    cli.run()


if __name__ == "__main__":
    main()
