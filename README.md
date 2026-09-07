# PY Restaurant Billing System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.x](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Database: MySQL](https://img.shields.io/badge/MySQL-connector-orange.svg)](https://dev.mysql.com/doc/connector-python/en/)
[![CI Workflow](https://github.com/webkolog/py-restaurant-billing-system/actions/workflows/python-tests.yml/badge.svg)](https://github.com/webkolog/py-restaurant-billing-system/actions)

**Version:** 1.0

**Created Date:** 2026-09-07

**Last Updated:** 2026-09-07

**Compatibility:** Python 3.x

**Created By:** Ali Candan ([@webkolog](https://github.com/webkolog))

**Website:** [http://webkolog.net](http://webkolog.net)

**Copyright:** (c) 2026 Ali Candan

**License:** MIT License ([http://mit-license.org](http://mit-license.org))

---

**PY Restaurant Billing System** is an efficient CLI application designed to streamline ordering and receipt generation for small-to-medium food service operations. It features automated MySQL table creation, itemized order tracking, tax calculation, and automated discounts on large orders.

## Features

* **Automated Setup:** Automatically creates the MySQL database (`restaurant_db`) and schema tables on initial startup.
* **Menu Management:** Displays menu pricing loaded directly from the database layer.
* **Interactive Cart System:** Supports multi-item cart accumulation with real-time stock and selection validation.
* **Persistent Order Ledger:** Logs every individual order item, total amount, and precise timestamp directly into MySQL.
* **Dynamic Receipt Billing:** Automatically computes 10% GST and applies a 5% discount on bills exceeding 5,000 PKR/Rs.

## Installation

### 1. Prerequisites
Ensure you have Python 3.x installed along with a running MySQL server.

### 2. Dependencies
Install the required MySQL Connector driver via pip:
```bash
pip install mysql-connector-python

```

### 3. Database Setup

Make sure your MySQL server is running locally on port `3306` with default credentials (`root` user and no password), or adjust `get_connection()` in `py-restaurant-billing-system.py` accordingly.

## Usage

Run the main application script:

```bash
python py-restaurant-billing-system.py

```

### Application Flow

1. Press **ENTER** at the start prompt to trigger schema checks and launch the menu interface.
2. Select items by entering their respective **Item ID**.
3. Specify quantities for each selection.
4. Input `0` when finished adding items.
5. Review the rendered receipt complete with Subtotal, GST (10%), applied Discounts, and the final Grand Total.

## Database Schema

```sql
-- Menu Structure
CREATE TABLE menu (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10,2)
);

-- Orders Structure
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT,
    item_name VARCHAR(100),
    quantity INT,
    price DECIMAL(10,2),
    total DECIMAL(10,2),
    order_time DATETIME
);

```

## Contributing

Contributions are welcome! If you find any issues or have feature requests, feel free to open an issue or submit a pull request on the repository.

## Support

For inquiries, questions, or issues related to this system, please visit [webkolog.net](http://webkolog.net) or reach out via GitHub.

```
