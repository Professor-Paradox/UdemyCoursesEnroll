DIR="$(dirname $0)"
cd $DIR

python -m venv env
source env/bin/activate
python courses.py
