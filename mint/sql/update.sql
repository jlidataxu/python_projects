Begin;
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
)	
SELECT 	
	cast (Date as date) ,
	Description,
	Original_Description,
	Case When Transaction_Type = 'debit' then cast (Amount as decimal) else  -1 * cast (Amount as decimal) end as Amount ,
	Transaction_Type,
	Category,
	Account_Name,
	Labels,
	Notes
FROM 	stg.s_transaction
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
FROM 	target.transaction;

Commit;