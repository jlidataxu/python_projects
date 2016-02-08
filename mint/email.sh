# email file
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $DIR/finance.properties
PARENTDIR="$(dirname "$DIR")"
source  $PARENTDIR/venv/bin/activate

python gmail.py $MAIL_ACCOUNT "daily billing $(date)"  $MAIL_DIR $MAIL_FILE
