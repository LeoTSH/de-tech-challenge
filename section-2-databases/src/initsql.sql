CREATE USER govtech;
CREATE DATABASE govtech;
GRANT ALL PRIVILEGES ON DATABASE govtech TO govtech;

\connect govtech;

CREATE SCHEMA IF NOT EXISTS govtech;

CREATE TABLE IF NOT EXISTS govtech.item (
  "item_id" varchar(50),
  "item_name" varchar(50),
  "manufacturer_name" varchar(50),
  "cost" numeric,
  "weight" numeric,
  PRIMARY KEY ("item_id")
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
  "items_bought" varchar[],
  "total_item_price" numeric[],
  "total_item_weight" numeric[],
  PRIMARY KEY ("transaction_id")
);

COPY govtech.customer
FROM '/usr/src/data/final_data.csv'
DELIMITER ','
CSV HEADER;

CREATE UNIQUE INDEX item_index
ON govtech.item (item_id);

CREATE UNIQUE INDEX customer_index
ON govtech.customer (member_id);

CREATE UNIQUE INDEX transaction_index
ON govtech.transaction (item_id);