#Source
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENTDIR="$(dirname "$DIR")"
source  $PARENTDIR/venv/bin/activate
source $DIR/finance.properties

python pull.py $MINT_USER $MINT_PASS $TRANSACTION_FILE
