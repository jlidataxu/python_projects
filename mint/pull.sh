#Source
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENTDIR="$(dirname "$DIR")"
source  $PARENTDIR/venv/bin/activate
source $DIR/finance.properties

mintapi --keyring $MINT_USER -t -f $TRANSACTION_FILE 
