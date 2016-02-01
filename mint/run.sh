DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
/bin/bash pull.sh
/bin/bash load.sh
/bin/bash email.sh
