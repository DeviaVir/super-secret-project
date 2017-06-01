```
# easy
$ python setup.py install

# alternatively
$ cd ~/into/the/project/directory
$ make clean build/venv
$ source build/venv/bin/activate
$ cd src
$ python -m project.main

# running the chunk test

$ make run
$ docker run -e HOSTNAME=memcached -e PORT=11211 --entrypoint=/bin/bash --rm --link project_memcached_1:memcached -it project_app
$ dd if=/dev/urandom of=in.dat bs=1048576 count=250
$ python -m project.main memcache --action file_set --key test5 --filename /app/in.dat
$ python -m project.main memcache --action file_get --key test5 --filename /app/out.dat
# compare files
$ diff /app/in.dat /app/out.dat
```

