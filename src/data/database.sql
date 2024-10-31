CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(255),
    price FLOAT NOT NULL,
    supplier_id INT,
    stock_quantity INT,
    CONSTRAINT fk_supplier
        FOREIGN KEY(supplier_id)
            REFERENCES suppliers(id)
);

CREATE TABLE suppliers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact_info VARCHAR(255),
    country VARCHAR(255)
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date TIMESTAMP,
    order_status VARCHAR(255),
    CONSTRAINT fk_customer
        FOREIGN KEY(customer_id)
            REFERENCES customers(id)
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    price_at_purchase FLOAT,
    CONSTRAINT fk_order
        FOREIGN KEY(order_id)
            REFERENCES orders(id),
    CONSTRAINT fk_product
        FOREIGN KEY (product_id)
            REFERENCES products(id)
);

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    email VARCHAR(255)
);

CREATE TABLE shipments (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL UNIQUE,
    shipped_date TIMESTAMP,
    delivery_date TIMESTAMP,
    shipping_cost INT,
    CONSTRAINT fk_order
        FOREIGN KEY(order_id)
            REFERENCES orders(id)
);
