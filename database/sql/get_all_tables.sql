CREATE OR REPLACE FUNCTION get_barcodes()
    RETURNS TABLE(id integer, eurocube_id integer, last_check date) AS $$
    SELECT * from barcodes;
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION get_eurocube()
    RETURNS TABLE(id integer, date_of_manufacture date, wear_level integer) AS $$
    SELECT * from eurocube;
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION get_partner()
    RETURNS TABLE(id integer, name text, TIN integer, OGRN integer, city text, street text, building integer) AS $$
    SELECT * from partner;
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION get_order()
    RETURNS TABLE(id integer, partner_id integer, cost integer, order_date date) AS $$
    SELECT * from "order";
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION get_order_list()
RETURNS TABLE (order_id integer, eurocube_id integer, product_id integer, eurocube_return bool) AS $$
    SELECT * from order_list;
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION get_actions()
RETURNS TABLE (id integer, eurocube_id integer, status text, action_date date) AS $$
    SELECT * from actions;
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION get_product()
RETURNS TABLE (id integer, name text, danger_level integer, cost_per_ton integer) AS $$
    SELECT * from product;
$$ LANGUAGE sql;