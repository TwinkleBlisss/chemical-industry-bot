CREATE OR REPLACE FUNCTION scan_barcode(input_barcode_id integer)
RETURNS TABLE(id integer, date_of_manufacture date, usage_count integer) AS $$
    SELECT eurocube.id, eurocube.date_of_manufacture, eurocube.usage_count FROM eurocube
    JOIN barcodes ON eurocube.id = barcodes.eurocube_id
    WHERE barcodes.id = input_barcode_id;
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION add_barcodes(input_barcode_id integer, input_eurocube_id integer)
RETURNS void AS $$
    INSERT INTO barcodes VALUES (input_barcode_id, input_eurocube_id);
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION add_eurocube(input_barcode_id integer, date_of_manufacture date, usage_count integer)
RETURNS void AS $$
    INSERT INTO eurocube(date_of_manufacture, usage_count) VALUES (date_of_manufacture, usage_count);
    INSERT INTO barcodes VALUES (input_barcode_id, (SELECT eurocube.id FROM eurocube ORDER BY eurocube.id DESC LIMIT 1))
$$ LANGUAGE sql;




CREATE OR REPLACE FUNCTION add_order(partner_id integer, cost integer, order_date date)
RETURNS void as $$
    INSERT INTO "order"(partner_id, cost, order_date) VALUES (partner_id, cost, order_date);
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION add_product(name text, danger_level integer, cost_per_ton integer)
RETURNS void as $$
    INSERT INTO product(name, danger_level, cost_per_ton) VALUES (name, danger_level, cost_per_ton);
$$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION add_partner(name text, tin integer, ogrn integer, city text, street text, building integer)
RETURNS void as $$
    INSERT INTO partner(name, tin, ogrn, city, street, building) VALUES (name, tin, ogrn, city, street, building);
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION get_order(order_id integer)
RETURNS integer as $$
    SELECT id from "order" WHERE id = order_id;
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION add_actions(eurocube_id integer, status text)
RETURNS void as $$
    INSERT INTO actions(eurocube_id, status) VALUES (eurocube_id, status);
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION add_order_list(order_id integer, eurocube_id integer)
RETURNS void AS $$
    INSERT INTO order_list(order_id, eurocube_id) VALUES (order_id, eurocube_id)
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION get_product_id(name text)
RETURNS integer as $$
    SELECT id FROM product WHERE product.name = name;
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION change_usage_count()
RETURNS TRIGGER as $$
    BEGIN
    IF (SELECT actions.status FROM actions ORDER BY actions.id DESC LIMIT 1) = 'arrived' THEN
        UPDATE eurocube SET usage_count = (SELECT eurocube.usage_count FROM eurocube
        WHERE eurocube.id =  (SELECT actions.eurocube_id FROM actions ORDER BY actions.id DESC LIMIT 1)) + 1;
    END IF;
    RETURN NEW;
    END;
$$ LANGUAGE PLPGSQL;

DROP TRIGGER IF EXISTS add_actions_trigger on actions;

CREATE TRIGGER add_actions_trigger
    AFTER INSERT
    ON actions
    FOR EACH STATEMENT
    EXECUTE PROCEDURE change_usage_count();