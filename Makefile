venv/bin/python:
	virtualenv --python=python2 venv
	venv/bin/pip install -r requirements.txt

run: venv/bin/python
	venv/bin/python app.py

test: venv/bin/python
	venv/bin/python app.py &
	-venv/bin/python test_client.py
	pkill python

clean:
	rm -rf venv
	rm -f *.db
	rm -f *.pyc
