import sys
import mintapi

def get_mint_transaction(email, password, file_name):
	mint = mintapi.Mint(email, password)
	data = mint.get_transactions()
	data.to_json(file_name,orient='records')

if __name__ == '__main__':
	email=sys.argv[1]
	password=sys.argv[2]
	file_name=sys.argv[3]
	get_mint_transaction(email, password, file_name)
