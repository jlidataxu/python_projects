-- Log load log
-- CREATE TABLE meta.infile_log (
--   id serial not null,
--   feed_name varchar(100),
--   feed_type varchar(100),
--   created_at timestamp default current_timestamp,
--   completed_at timestamp
-- )
insert into meta.infile_log (feed_name, feed_type) values('transaction.json', 'transaction feed');

Begin;
set search_path=pg_catalog,public,stg,target;

drop table if exists stg.temp_json;
create table stg.temp_json (values text);
\copy stg.temp_json from '/tmp/transaction.json';

truncate table stg.transaction;

insert into stg.transaction
select values->>'date' as date,
       values->>'description' as description,
       values->>'original_description' as original_description,
       values->>'amount' as amount,
       values->>'transaction_type' as transaction_type,
       values->>'category' as category,
       values->>'account_name' as account_name,
       values->>'labels' as labels,
       values->>'notes' as notes      
from   (
        select json_array_elements(regexp_replace(values, E'[\\n\\r]+', ' ', 'g' )::json) as values 
           from   stg.temp_json
       ) a;


drop table if exists target.transaction_new;

SELECT  
  cast ((TIMESTAMP WITHOUT TIME ZONE 'epoch' + Date::numeric/1000 * INTERVAL '1 second') as date) ,
  Description,
  Original_Description,
  Case When Transaction_Type = 'debit' then cast (Amount as decimal) else  -1 * cast (Amount as decimal) end as Amount ,
  Transaction_Type,
  Category,
  Account_Name,
  Labels,
  Notes
INTO target.transaction_new
FROM  stg.transaction
EXCEPT  
SELECT  
  Date,
  Description,
  Original_Description,
  Amount,
  Transaction_Type,
  Category,
  Account_Name,
  Labels,
  Notes
FROM  target.transaction;

INSERT INTO target.transaction (  
  Date,
  Description,
  Original_Description,
  Amount,
  Transaction_Type,
  Category,
  Account_Name,
  Labels,
  Notes
) SELECT * FROM target.transaction_new;

-- get output file
\copy target.transaction_new to '/tmp/transaction_new.csv' with csv header;

UPDATE meta.infile_log
SET completed_at = current_timestamp
WHERE id = (select max(id) from meta.infile_log where feed_type = 'transaction feed');

Commit;
