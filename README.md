# Image resizer web app

This web app allows you to resize images by running asynchronous task.

## Installation

Resizer app requires Django, Redis and Celery.

### 1.1. Install redis server
```sh
$ sudo apt install redis-server
```
### 1.2. Edit configuration file
you may use any text editor, I use Sublime Text (subl)
```sh
$ sudo subl /etc/redis/redis.conf
```
 - find supervised setting under GENERAL section, by default it is set to '**supervised no**', change it to '**supervised systemd**'
 - add '**bind 127.0.0.1:6379**' under NETWORK section

run redis server with and test with:
```sh
$ redis-server
$ redis-cli ping
```
response should be **PONG**


### 2. Create virtual environment "testenv" and activate it
```sh
$ pip install virtualenv
$ virtualenv testenv
$ source testenv/bin/activate
```

### 3. Clone repository
```sh
$ git clone https://github.com/ArretVice/resizer.git
$ cd resizer/
```

### 4. Install required packages
install from requirements.txt file:
```sh
$ pip install -r requirements.txt
```

or install packages manualy (not recommended):
```sh
$ pip install django Pillow celery redis
```

### 5. Run tests without connection to the message broker
```sh
$ python3 manage.py test --exclude-tag=slow
```

### 6. Launch redis server
```sh
$ redis-server
```
if server already in use, shut it down and relaunch with:
```sh
$ redis-cli shutdown
$ redis-server
```

### 7. Launch celery worker in separate terminal window (requires active testenv)
```sh
$ celery worker -A main
```

### 8. Run full test suite
```sh
$ python3 manage.py test
```

### 9. Migrate database and run server on localhost
```sh
$ python3 manage.py migrate
$ python3 manage.py runserver
```

## Installation complete!
##### Web service will be running at [localhost:8000](http://localhost:8000 "localhost:8000")


## User guide:

#### Uploading image:
1. Click Upload image
2. Click "Choose file", select the image you want to resize
3. Enter desired width and height into corresponding fields
4. Click "Resize" to proceed

You will be redirected to status page, where you would get your resized image ID and status.
Click "Refresh" to check if your image has been resized.
If the image has been resized, it will be displayed below it's status.

#### Checking status:

You may check the status of your image by clicking "Status page" link.
Enter the ID for image and click "Check" to ckeck it's status.

#### Cleaning up:

Resizer app stores resized images and their ID's, so you could retrieve your resized image. However, you may want to clean those files, as well as ID entries in the database, and possibly delete log of all performed operations. Use the following command for that:
```sh
$ python3 manage.py cleardbandfolder
```

#### Checking logs:

If you wish to check performed operations, they are logged in *resizer.log* file.