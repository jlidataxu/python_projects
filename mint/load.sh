#load file
#Source
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $DIR/finance.properties
PSQL="psql -d $DB_NAME -U $DB_USER -h $DB_SERVER  -f "
sql_file=sql/load.sql
export PGPASSWORD=$DB_PASS
ec=`$PSQL "$DIR/$sql_file"`
