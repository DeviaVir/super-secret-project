test: build/venv
	@( . build/venv/bin/activate;  \
	    cd src && \
	    coverage erase; \
		nosetests --with-xunit --xunit-file=../build/nosetests.xml \
			--with-coverage --cover-package=project --cover-min-percentage 100 --cover-xml --cover-xml-file=../build/coverage.xml \
			test \
	)

clean:
	rm -Rf build/
	-docker-compose kill
	-docker-compose rm -f

build/venv: build/venv/bin/activate

build/venv/bin/activate: requirements.txt
	@mkdir -p build
	@test -d build/venv || virtualenv --system-site-packages build/venv
	@( . build/venv/bin/activate;  \
		pip install -r requirements.txt; \
		pip install -r src/test/requirements.txt; \
	)

build/docker-image:
	docker-compose build

run: build/docker-image
	docker-compose up -d

stop:
	docker-compose down

integration: run only-integration
	
only-integration:
	docker run -e HOSTNAME=memcached -e PORT=11211 --rm --link project_memcached_1:memcached -it project_app memcache --action set --key test --value "Hello world!"
	docker run -e HOSTNAME=memcached -e PORT=11211 --rm --link project_memcached_1:memcached -it project_app memcache --action get --key test

file-integration:
	docker run -e HOSTNAME=memcached -e PORT=11211 --rm --link project_memcached_1:memcached -it project_app memcache --action file_set --key test --filename in.dat
	docker run -e HOSTNAME=memcached -e PORT=11211 --rm --link project_memcached_1:memcached -it project_app memcache --action file_get --key test --filename out.dat

lint: build/venv
	@( . build/venv/bin/activate; \
		find src -not -path 'src/test*' -name '*.py' | xargs pylint --rcfile pylintrc \
	)

composetest:
	-docker-compose kill
	-docker-compose rm -f
	docker-compose build
	docker-compose run test

.PHONY: composetest test
