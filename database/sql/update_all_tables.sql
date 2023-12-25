CREATE OR REPLACE FUNCTION update_barcodes(id integer, input_eurocube_id integer)

RETURNS void as $$
    UPDATE barcodes SET eurocube_id = input_eurocube_id
    WHERE barcodes.id = id;
$$ LANGUAGE sql;



CREATE OR REPLACE FUNCTION update_eurocube(id integer, input_usage_count integer)
RETURNS void as $$
    UPDATE eurocube SET usage_count = input_usage_count
    WHERE eurocube.id = id;
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION update_partner(id integer, input_name text, input_TIN integer, input_OGRN integer,
                                          input_city text, input_street text, input_building integer)
RETURNS void as $$
    UPDATE partner SET name = input_name, TIN = input_TIN, OGRN = input_OGRN, city = input_city,
                       street = input_street, building = input_building
    WHERE partner.id = id;
$$ LANGUAGE sql;





CREATE OR REPLACE FUNCTION update_product(id integer, input_name text, input_danger_level integer, input_cost_per_token integer)
RETURNS void as $$
    UPDATE product SET (name, danger_level, cost_per_ton) = (input_name, input_danger_level, input_cost_per_token)
    WHERE product.id = id;
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION update_order_list(order_id integer, eurocube_id integer, input_product_id integer)
RETURNS void AS $$
    UPDATE order_list SET product_id = input_product_id
    WHERE order_list.order_id = order_id AND order_list.eurocube_id = eurocube_id;
$$ LANGUAGE sql;