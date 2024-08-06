CREATE SCHEMA IF NOT EXISTS olist;


CREATE TABLE IF NOT EXISTS olist.customers (
    customer_id VARCHAR(255) PRIMARY KEY,
    customer_unique_id VARCHAR(255),
    customer_zip_code_prefix VARCHAR(8),
    customer_city VARCHAR(100),
    customer_state VARCHAR(2)
);

CREATE TABLE IF NOT EXISTS olist.orders (
    order_id VARCHAR(255) PRIMARY KEY,
    customer_id VARCHAR(255),
    order_status VARCHAR(255),
    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES olist.customers (customer_id)         
);

CREATE TABLE IF NOT EXISTS olist.products (
    product_id VARCHAR(255) PRIMARY KEY,
    product_category_name VARCHAR(255),
    product_name_length INT,
    product_description_length INT,
    product_photos_qty INT,
    product_weight_g INT,
    product_length_cm INT,
    product_height_cm INT,
    product_width_cm INT
);

CREATE TABLE IF NOT EXISTS olist.sellers (
    seller_id VARCHAR (255) PRIMARY KEY,
    seller_zip_code_prefix VARCHAR(6),
    seller_city VARCHAR(125),
    seller_state VARCHAR (3)
);

CREATE TABLE IF NOT EXISTS olist.order_items (
    order_id VARCHAR(255),
    order_item_id VARCHAR(255),
    product_id VARCHAR(255),
    seller_id VARCHAR(255),
    shipping_limit_date TIMESTAMP,
    price FLOAT,
    freight_value FLOAT,
    FOREIGN KEY (order_id)  REFERENCES olist.orders (order_id),
    FOREIGN KEY (product_id) REFERENCES olist.products (product_id),
    FOREIGN KEY (seller_id) REFERENCES olist.sellers (seller_id)

);


CREATE TABLE IF NOT EXISTS olist.order_payments (
    order_id VARCHAR(255),
    payment_sequential INT,
    payment_type VARCHAR(20),
    payment_installments INT,
    payment_value FLOAT,
    FOREIGN KEY (order_id) REFERENCES olist.orders (order_id)
);

CREATE TABLE IF NOT EXISTS olist.order_reviews (
    review_id VARCHAR(255),
    order_id VARCHAR(255),
    review_score INT,
    review_comment_title VARCHAR(255),
    review_comment_message VARCHAR(255),
    review_creation_date DATE,
    review_answer_timestamp TIMESTAMP,
    FOREIGN KEY (order_id)  REFERENCES olist.orders (order_id)
);



CREATE TABLE IF NOT EXISTS olist.geolocation_data (
    geolocation_zip_code_prefix VARCHAR(255),
    geolocation_lat FLOAT,
    geolocation_lng FLOAT,
    geolocation_city VARCHAR(125),
    geolocation_state VARCHAR(2)
);


CREATE TABLE IF NOT EXISTS olist.product_category_translation (
    product_category_name varchar(255),
    product_category_name_english varchar(100)
);



-- Load Data from CSV Files
COPY olist.customers FROM '/data/olist_customers_dataset.csv' DELIMITER ',' CSV HEADER;

COPY olist.orders FROM '/data/olist_orders_dataset.csv' DELIMITER ',' CSV HEADER;

COPY olist.products FROM '/data/olist_products_dataset.csv' DELIMITER ',' CSV HEADER;

COPY olist.sellers FROM '/data/olist_sellers_dataset.csv' DELIMITER ',' CSV HEADER;

COPY olist.order_items FROM '/data/olist_order_items_dataset.csv' DELIMITER ',' CSV HEADER;

COPY olist.order_payments FROM '/data/olist_order_payments_dataset.csv' DELIMITER ',' CSV HEADER;

COPY olist.order_reviews FROM '/data/olist_order_reviews_dataset.csv' DELIMITER ',' CSV HEADER;

COPY olist.geolocation_data FROM '/data/olist_geolocation_dataset.csv' DELIMITER ',' CSV HEADER;

COPY olist.product_category_translation FROM '/data/product_category_name_translation.csv' DELIMITER ',' CSV HEADER;
