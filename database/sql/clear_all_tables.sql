CREATE OR REPLACE FUNCTION clear_barcodes()
RETURNS void as $$
    DELETE FROM barcodes;
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION clear_eurocube()
RETURNS void as $$
    DELETE FROM eurocube;
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION clear_order()
RETURNS void as $$
    DELETE FROM "order";
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION clear_order_list()
RETURNS void as $$
    DELETE FROM order_list;
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION clear_barcodes()
RETURNS void as $$
    DELETE FROM barcodes;
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION clear_actions()
RETURNS void as $$
    DELETE FROM actions;
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION clear_product()
RETURNS void as $$
    DELETE FROM product;
$$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION clear_partner()
RETURNS void as $$
    DELETE FROM partner;
$$ LANGUAGE sql;
