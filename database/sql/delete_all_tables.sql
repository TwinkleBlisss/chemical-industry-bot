CREATE OR REPLACE FUNCTION delete_from_barcodes(id integer)
RETURNS void as $$
    DELETE FROM barcodes WHERE barcodes.id = id;
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION delete_from_eurocube(id integer)
RETURNS void as $$
    DELETE FROM eurocube WHERE eurocube.id = id;
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION delete_from_partner(id integer)
RETURNS void as $$
    DELETE FROM partner WHERE partner.id = id;
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION delete_from_order(id integer)
RETURNS void as $$
    DELETE FROM "order" WHERE "order".id = id;
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION delete_from_order_list(order_id integer, eurocube_id integer)
RETURNS void as $$
    DELETE FROM order_list WHERE order_list.order_id = order_id AND order_list.eurocube_id = eurocube_id;
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION delete_from_actions(id integer)
RETURNS void as $$
    DELETE FROM actions WHERE actions.id = id;
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION delete_from_product(id integer)
RETURNS void as $$
    DELETE FROM product WHERE product.id = id;
$$ LANGUAGE sql;