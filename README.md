# The Shahs Luxury Collection 👑

A sophisticated luxury clothing brand management system designed for high-end fashion retailers.

## Overview

The Shahs Luxury Collection is a comprehensive Python-based management system for luxury fashion brands. It provides tools for managing products, inventory, customers, and sales transactions with a focus on premium user experience and data integrity.

## Features

✨ **Product Management**
- Comprehensive product catalog with designer attribution
- Support for multiple luxury categories (Haute Couture, Ready-to-Wear, Accessories, Shoes, Jewelry, Handbags)
- Detailed product information including descriptions and pricing

📦 **Inventory Management**
- Size-based inventory tracking
- Automated stock updates on purchases
- Real-time inventory status reporting

👥 **Customer Management**
- VIP customer tracking and identification
- Complete purchase history
- Customer spending analytics

💳 **Transaction Processing**
- Secure purchase processing
- Automatic inventory deduction
- Transaction history tracking

📊 **Analytics & Reporting**
- Brand statistics and metrics
- Revenue tracking
- Category-based product analysis

## Installation

### Requirements
- Python 3.7 or higher

### Setup
1. Clone the repository:
```bash
git clone https://github.com/reyanatifbsse-2021a-alt/the_shahs.git
cd the_shahs
```

2. No additional dependencies required - uses only Python standard library!

## Usage

### Running the CLI Application

Launch the interactive command-line interface:

```bash
python3 cli.py
```

The CLI provides an intuitive menu-driven interface for:
- Browsing the product catalog
- Checking inventory levels
- Managing customer information
- Processing purchases
- Viewing analytics

### Using as a Python Module

```python
from luxury_brand import LuxuryBrand, Product, Customer, Category

# Create a new luxury brand
brand = LuxuryBrand("My Luxury Brand")

# Add a product
product = Product(
    product_id="LUX001",
    name="Silk Evening Gown",
    category=Category.HAUTE_COUTURE,
    price=12000.00,
    designer="Valentino",
    description="Exquisite hand-embroidered gown"
)
brand.add_product(product)

# Add inventory
brand.add_inventory("LUX001", quantity=5, size="M")

# Add a customer
customer = Customer(
    customer_id="C001",
    name="Jane Smith",
    email="jane@example.com",
    vip_status=True
)
brand.add_customer(customer)

# Process a purchase
total = brand.process_purchase("C001", "LUX001", quantity=1, size="M")
print(f"Purchase total: ${total:,.2f}")
```

### Sample Data

The system comes with pre-loaded sample data featuring:
- 6 luxury products across different categories
- 4 sample customers (including VIP members)
- Inventory across multiple sizes

Initialize the sample brand:

```python
from luxury_brand import initialize_sample_brand

brand = initialize_sample_brand()
```

## Running Tests

Execute the comprehensive test suite:

```bash
python3 -m unittest test_luxury_brand.py -v
```

The test suite includes:
- Product management tests
- Inventory tracking tests
- Customer management tests
- Transaction processing tests
- Error handling validation

## Project Structure

```
the_shahs/
├── luxury_brand.py      # Core business logic and models
├── cli.py              # Command-line interface
├── test_luxury_brand.py # Comprehensive test suite
└── README.md           # This file
```

## Core Classes

### Product
Represents a luxury fashion item with designer attribution, category, and pricing.

### InventoryItem
Manages stock levels for products with size-specific tracking.

### Customer
Tracks customer information, VIP status, and purchase history.

### LuxuryBrand
Main system orchestrator managing products, inventory, and customers.

## Categories

- **Haute Couture** - Exclusive, custom-fitted high fashion
- **Ready-to-Wear** - Premium off-the-rack collections
- **Accessories** - Luxury fashion accessories
- **Shoes** - Designer footwear
- **Jewelry** - Fine jewelry pieces
- **Handbags** - Designer bags and purses

## Example Workflow

1. **Browse Products**: View the complete catalog or filter by category
2. **Check Availability**: Verify inventory levels and available sizes
3. **Process Sale**: Select customer, product, size, and quantity
4. **Track History**: Review customer purchase history and spending
5. **Analyze Performance**: View brand statistics and metrics

## License

This project is part of the academic curriculum.

## Authors

The Shahs Team - Luxury Fashion Technology Division
