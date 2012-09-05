

bootstrap.py: create_bootstrap.py
	./create_bootstrap.py
	chmod u+x bootstrap.py

database.db: init_db.py keygen.py
	python2 init_db.py

venv: bootstrap.py
	./bootstrap.py -p python2 venv
	chmod u+x venv/bin/activate

.PHONY: clean run

clean:
	- rm -rf venv bootstrap.py

run: keygen.py
	python keygen.py

uwsgi:
	venv/bin/uwsgi -H venv -w keygen:app -s uwsgi.sock -M

# vim: tabstop=8 noexpandtab
