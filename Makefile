prodceleryworkers:
	cd contentcuration/ && celery -A contentcuration worker -l info

setupdryrun:
	nanobox evar add dry-run DJANGO_SETTINGS_MODULE=contentcuration.dry_run_settings


collectstatic: migrate
	python contentcuration/manage.py collectstatic --noinput
	python contentcuration/manage.py collectstatic_js_reverse
	python contentcuration/manage.py loadconstants

migrate:
	python contentcuration/manage.py migrate || true

ensurecrowdinclient:
  ls -l crowdin-cli.jar || curl -L https://storage.googleapis.com/le-downloads/crowdin-cli/crowdin-cli.jar -o crowdin-cli.jar

makemessages:
	# generate frontend messages
	npm run makemessages
	# generate backend messages
	python contentcuration/manage.py makemessages

uploadmessages: ensurecrowdinclient
	java -jar /contentcuration/crowdin-cli.jar upload sources

# we need to depend on makemessages, since CrowdIn requires the en folder to be populated
# in order for it to properly extract strings
downloadmessages: ensurecrowdinclient makemessages
	java -jar crowdin-cli.jar download

compilemessages:
	python contentcuration/manage.py compilemessages

# When using apidocs, this should clean out all modules
clean-docs:
	$(MAKE) -C docs clean

docs: clean-docs
	# Adapt to apidocs
	# sphinx-apidoc -d 10 -H "Python Reference" -o docs/py_modules/ kolibri kolibri/test kolibri/deployment/ kolibri/dist/
	$(MAKE) -C docs html
