"""
Unit tests for The Shahs Luxury Clothing Brand System
"""

import unittest
from datetime import datetime
from luxury_brand import (
    Product, Category, InventoryItem, Customer, 
    LuxuryBrand, initialize_sample_brand
)


class TestProduct(unittest.TestCase):
    """Test Product class"""
    
    def test_create_product(self):
        """Test creating a product"""
        product = Product(
            "TEST001", 
            "Designer Dress", 
            Category.HAUTE_COUTURE,
            5000.00,
            "Dior",
            "Beautiful evening dress"
        )
        self.assertEqual(product.product_id, "TEST001")
        self.assertEqual(product.name, "Designer Dress")
        self.assertEqual(product.category, Category.HAUTE_COUTURE)
        self.assertEqual(product.price, 5000.00)
        self.assertEqual(product.designer, "Dior")
        self.assertIsInstance(product.created_at, datetime)
    
    def test_product_str(self):
        """Test product string representation"""
        product = Product("TEST001", "Designer Dress", Category.HAUTE_COUTURE,
                         5000.00, "Dior")
        self.assertEqual(str(product), "Designer Dress by Dior - $5,000.00")
    
    def test_product_to_dict(self):
        """Test product to dictionary conversion"""
        product = Product("TEST001", "Designer Dress", Category.HAUTE_COUTURE,
                         5000.00, "Dior", "Test description")
        product_dict = product.to_dict()
        self.assertEqual(product_dict['product_id'], "TEST001")
        self.assertEqual(product_dict['name'], "Designer Dress")
        self.assertEqual(product_dict['category'], "Haute Couture")
        self.assertEqual(product_dict['price'], 5000.00)


class TestInventoryItem(unittest.TestCase):
    """Test InventoryItem class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.product = Product("TEST001", "Designer Dress", 
                              Category.HAUTE_COUTURE, 5000.00, "Dior")
        self.inventory = InventoryItem(self.product, 10, "M")
    
    def test_create_inventory(self):
        """Test creating inventory item"""
        self.assertEqual(self.inventory.product, self.product)
        self.assertEqual(self.inventory.quantity, 10)
        self.assertEqual(self.inventory.size, "M")
    
    def test_add_stock(self):
        """Test adding stock"""
        self.inventory.add_stock(5)
        self.assertEqual(self.inventory.quantity, 15)
    
    def test_add_negative_stock_raises_error(self):
        """Test that adding negative stock raises error"""
        with self.assertRaises(ValueError):
            self.inventory.add_stock(-5)
    
    def test_remove_stock(self):
        """Test removing stock"""
        self.inventory.remove_stock(3)
        self.assertEqual(self.inventory.quantity, 7)
    
    def test_remove_too_much_stock_raises_error(self):
        """Test that removing too much stock raises error"""
        with self.assertRaises(ValueError):
            self.inventory.remove_stock(15)
    
    def test_remove_negative_stock_raises_error(self):
        """Test that removing negative stock raises error"""
        with self.assertRaises(ValueError):
            self.inventory.remove_stock(-5)


class TestCustomer(unittest.TestCase):
    """Test Customer class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.customer = Customer("C001", "John Doe", "john@email.com", 
                                "+1-555-0100", True)
        self.product = Product("TEST001", "Designer Dress", 
                              Category.HAUTE_COUTURE, 5000.00, "Dior")
    
    def test_create_customer(self):
        """Test creating a customer"""
        self.assertEqual(self.customer.customer_id, "C001")
        self.assertEqual(self.customer.name, "John Doe")
        self.assertEqual(self.customer.email, "john@email.com")
        self.assertTrue(self.customer.vip_status)
        self.assertEqual(len(self.customer.purchase_history), 0)
    
    def test_add_purchase(self):
        """Test adding a purchase"""
        self.customer.add_purchase(self.product, 2, 10000.00)
        self.assertEqual(len(self.customer.purchase_history), 1)
        self.assertEqual(self.customer.purchase_history[0]['product_id'], "TEST001")
        self.assertEqual(self.customer.purchase_history[0]['quantity'], 2)
        self.assertEqual(self.customer.purchase_history[0]['total_amount'], 10000.00)
    
    def test_get_total_spent(self):
        """Test calculating total spent"""
        self.customer.add_purchase(self.product, 1, 5000.00)
        self.customer.add_purchase(self.product, 2, 10000.00)
        self.assertEqual(self.customer.get_total_spent(), 15000.00)
    
    def test_customer_str(self):
        """Test customer string representation"""
        self.assertEqual(str(self.customer), "John Doe (VIP) - john@email.com")
        
        non_vip = Customer("C002", "Jane Doe", "jane@email.com", vip_status=False)
        self.assertEqual(str(non_vip), "Jane Doe - jane@email.com")


class TestLuxuryBrand(unittest.TestCase):
    """Test LuxuryBrand class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.brand = LuxuryBrand("Test Brand")
        self.product = Product("TEST001", "Designer Dress", 
                              Category.HAUTE_COUTURE, 5000.00, "Dior")
        self.customer = Customer("C001", "John Doe", "john@email.com", 
                                vip_status=True)
    
    def test_create_brand(self):
        """Test creating a brand"""
        self.assertEqual(self.brand.brand_name, "Test Brand")
        self.assertEqual(len(self.brand.products), 0)
        self.assertEqual(len(self.brand.customers), 0)
    
    def test_add_product(self):
        """Test adding a product"""
        self.brand.add_product(self.product)
        self.assertEqual(len(self.brand.products), 1)
        self.assertIn("TEST001", self.brand.products)
    
    def test_add_duplicate_product_raises_error(self):
        """Test that adding duplicate product raises error"""
        self.brand.add_product(self.product)
        with self.assertRaises(ValueError):
            self.brand.add_product(self.product)
    
    def test_add_inventory(self):
        """Test adding inventory"""
        self.brand.add_product(self.product)
        self.brand.add_inventory("TEST001", 10, "M")
        inventory = self.brand.get_inventory_status("TEST001")
        self.assertEqual(len(inventory), 1)
        self.assertEqual(inventory[0].quantity, 10)
        self.assertEqual(inventory[0].size, "M")
    
    def test_add_inventory_same_size_increases_quantity(self):
        """Test that adding inventory for same size increases quantity"""
        self.brand.add_product(self.product)
        self.brand.add_inventory("TEST001", 10, "M")
        self.brand.add_inventory("TEST001", 5, "M")
        inventory = self.brand.get_inventory_status("TEST001")
        self.assertEqual(len(inventory), 1)
        self.assertEqual(inventory[0].quantity, 15)
    
    def test_add_inventory_different_sizes(self):
        """Test adding inventory for different sizes"""
        self.brand.add_product(self.product)
        self.brand.add_inventory("TEST001", 10, "M")
        self.brand.add_inventory("TEST001", 8, "L")
        inventory = self.brand.get_inventory_status("TEST001")
        self.assertEqual(len(inventory), 2)
    
    def test_get_product(self):
        """Test getting a product"""
        self.brand.add_product(self.product)
        retrieved = self.brand.get_product("TEST001")
        self.assertEqual(retrieved, self.product)
    
    def test_list_products(self):
        """Test listing products"""
        product2 = Product("TEST002", "Handbag", Category.HANDBAGS, 
                          3000.00, "Chanel")
        self.brand.add_product(self.product)
        self.brand.add_product(product2)
        products = self.brand.list_products()
        self.assertEqual(len(products), 2)
    
    def test_list_products_by_category(self):
        """Test listing products by category"""
        product2 = Product("TEST002", "Handbag", Category.HANDBAGS, 
                          3000.00, "Chanel")
        self.brand.add_product(self.product)
        self.brand.add_product(product2)
        
        haute_couture = self.brand.list_products(Category.HAUTE_COUTURE)
        self.assertEqual(len(haute_couture), 1)
        self.assertEqual(haute_couture[0].category, Category.HAUTE_COUTURE)
    
    def test_add_customer(self):
        """Test adding a customer"""
        self.brand.add_customer(self.customer)
        self.assertEqual(len(self.brand.customers), 1)
        self.assertIn("C001", self.brand.customers)
    
    def test_add_duplicate_customer_raises_error(self):
        """Test that adding duplicate customer raises error"""
        self.brand.add_customer(self.customer)
        with self.assertRaises(ValueError):
            self.brand.add_customer(self.customer)
    
    def test_get_customer(self):
        """Test getting a customer"""
        self.brand.add_customer(self.customer)
        retrieved = self.brand.get_customer("C001")
        self.assertEqual(retrieved, self.customer)
    
    def test_process_purchase(self):
        """Test processing a purchase"""
        self.brand.add_product(self.product)
        self.brand.add_inventory("TEST001", 10, "M")
        self.brand.add_customer(self.customer)
        
        total = self.brand.process_purchase("C001", "TEST001", 2, "M")
        
        # Check purchase was recorded
        self.assertEqual(len(self.customer.purchase_history), 1)
        self.assertEqual(total, 10000.00)
        
        # Check inventory was updated
        inventory = self.brand.get_inventory_status("TEST001")
        self.assertEqual(inventory[0].quantity, 8)
    
    def test_process_purchase_insufficient_inventory(self):
        """Test that purchase with insufficient inventory raises error"""
        self.brand.add_product(self.product)
        self.brand.add_inventory("TEST001", 1, "M")
        self.brand.add_customer(self.customer)
        
        with self.assertRaises(ValueError):
            self.brand.process_purchase("C001", "TEST001", 5, "M")
    
    def test_process_purchase_invalid_customer(self):
        """Test that purchase with invalid customer raises error"""
        self.brand.add_product(self.product)
        self.brand.add_inventory("TEST001", 10, "M")
        
        with self.assertRaises(ValueError):
            self.brand.process_purchase("C999", "TEST001", 2, "M")
    
    def test_process_purchase_invalid_product(self):
        """Test that purchase with invalid product raises error"""
        self.brand.add_customer(self.customer)
        
        with self.assertRaises(ValueError):
            self.brand.process_purchase("C001", "INVALID", 2, "M")
    
    def test_get_vip_customers(self):
        """Test getting VIP customers"""
        vip_customer = Customer("C001", "VIP John", "vip@email.com", 
                               vip_status=True)
        regular_customer = Customer("C002", "Regular Jane", "regular@email.com",
                                   vip_status=False)
        
        self.brand.add_customer(vip_customer)
        self.brand.add_customer(regular_customer)
        
        vip_customers = self.brand.get_vip_customers()
        self.assertEqual(len(vip_customers), 1)
        self.assertTrue(vip_customers[0].vip_status)


class TestSampleBrand(unittest.TestCase):
    """Test sample brand initialization"""
    
    def test_initialize_sample_brand(self):
        """Test that sample brand is initialized correctly"""
        brand = initialize_sample_brand()
        
        self.assertEqual(brand.brand_name, "The Shahs Luxury Collection")
        self.assertGreater(len(brand.products), 0)
        self.assertGreater(len(brand.customers), 0)
        
        # Check that inventory was added
        for product_id in brand.products.keys():
            inventory = brand.get_inventory_status(product_id)
            self.assertGreater(len(inventory), 0)
        
        # Check that VIP customers exist
        vip_customers = brand.get_vip_customers()
        self.assertGreater(len(vip_customers), 0)


if __name__ == "__main__":
    unittest.main()
