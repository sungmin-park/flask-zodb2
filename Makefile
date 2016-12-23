setup: venv
	venv/bin/pip install --upgrade pip==9.0.1
	venv/bin/pip install -e .
	venv/bin/pip install -r requirements.txt

venv:
	virtualenv -p python3.5 venv
