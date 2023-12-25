DROP FUNCTION IF EXISTS create_all_tables();

CREATE FUNCTION create_all_tables() RETURNS void as $$
    CREATE TABLE barcodes (
      id integer PRIMARY KEY,
      eurocube_id integer,
      last_check date DEFAULT CURRENT_DATE
    );

    CREATE TABLE eurocube (
      id serial PRIMARY KEY,
      date_of_manufacture date,
      usage_count integer
    );


    CREATE TABLE partner (
      id serial PRIMARY KEY,
      name text,
      TIN integer,
      OGRN integer,
      city text,
      street text,
      building integer
    );

    CREATE TABLE "order" (
      id serial PRIMARY KEY,
      partner_id integer,
      cost integer,
      order_date date
    );

    CREATE TABLE order_list (
      order_id integer,
      eurocube_id integer,
      product_id integer DEFAULT NULL,
      eurocube_return bool DEFAULT true,
      PRIMARY KEY (order_id, eurocube_id)
    );

    CREATE TABLE actions (
      id serial PRIMARY KEY,
      eurocube_id integer,
      status text CHECK ( status = 'arrived' OR status = 'leaves'),
      action_date date DEFAULT CURRENT_DATE
    );

    CREATE TABLE product (
      id serial PRIMARY KEY,
      name text,
      danger_level integer CHECK (danger_level >= 0 AND danger_level <= 3),
      cost_per_ton integer
    );

    ALTER TABLE order_list ADD FOREIGN KEY (order_id) REFERENCES "order" (id);

    ALTER TABLE "order" ADD FOREIGN KEY (partner_id) REFERENCES partner (id);

    ALTER TABLE order_list  ADD FOREIGN KEY (eurocube_id) REFERENCES eurocube (id);

    ALTER TABLE actions ADD FOREIGN KEY (eurocube_id) REFERENCES eurocube (id);

    ALTER TABLE barcodes ADD FOREIGN KEY (eurocube_id) REFERENCES eurocube (id);

    ALTER TABLE order_list ADD FOREIGN KEY (product_id) REFERENCES product (id);

    CREATE INDEX name_idx ON product(name);
$$ LANGUAGE sql;