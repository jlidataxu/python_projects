# email file
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $DIR/finance.properties

cat $MAIL_FILE | uuencode transaction_new.csv | mail -s "daily billing $(date)" $MAIL_ACCOUNT
