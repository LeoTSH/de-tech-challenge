CREATE USER govtech WITH PASSWORD 'govtech';
CREATE DATABASE govtech;
GRANT ALL PRIVILEGES ON DATABASE govtech TO govtech;

\connect govtech;

CREATE SCHEMA IF NOT EXISTS govtech;

CREATE TABLE IF NOT EXISTS govtech.product (
  "product_id" varchar(50),
  "product_name" varchar(50),
  "manufacturer_name" varchar(50),
  "cost" numeric,
  "weight" numeric,
  PRIMARY KEY ("product_id")
);

CREATE TABLE IF NOT EXISTS govtech.customer (
  "member_id" varchar(50),
  "name" varchar(50),
  "first_name" varchar(30),
  "last_name" varchar(30),
  "above_18" boolean,
  "age" numeric,
  "dob" varchar(10),
  "mobile" varchar(8),
  "email" varchar(50),
  PRIMARY KEY ("member_id")
);

CREATE TABLE IF NOT EXISTS govtech.transaction (
  "transaction_id" varchar(50),
  "member_id" varchar(50),
  "products_bought" varchar[],
  "total_product_price" numeric,
  "total_product_weight" numeric,
  PRIMARY KEY ("transaction_id"),
  CONSTRAINT fk_customer
    FOREIGN KEY(member_id) 
	  REFERENCES govtech.customer(member_id)
);

COPY govtech.customer
FROM '/usr/src/data/final_data.csv'
DELIMITER ','
CSV HEADER;

CREATE UNIQUE INDEX product_index
ON govtech.product (product_id);

CREATE UNIQUE INDEX customer_index
ON govtech.customer (member_id);

CREATE UNIQUE INDEX transaction_index
ON govtech.transaction (transaction_id);