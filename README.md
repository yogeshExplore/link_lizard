### Important
* For a production project, I would use celery, rabbitmq/kafka, dockerized producer/consumer to achieve if high scale is needed.
* For the assignment purpose I have just used gevent and take care of thread-safety
* If you want I can explain the project over call or you can run it once in the debug mode.

### Dependency
* python 3.10.2 ( You can pyenv to maintain multiple version of python in your system )
* pipenv ( For virtual environment)

### Setup 
* cd link_lizard
* pipenv install ( I have created .venv directory so that the dependency would be installed in that directory only )
* pipenv shell ( or other way to activate virtual env)
* create .env and copy the content of .env.dist to .env. Please change environment variable accordingly

### Run
#### Arguments
```
--url 
```
The website url you want to crawl, example http://bbc.co.uk , http://example.com, http://docs.celeryq.dev, http://gevent.org
Default is http://example.com ( It has no links, so please pass this)

```
--workers
```
Gevent workers, please do not put a high number, the target website can block you ( proxy and capcha is not implement yet)
Also you can affect the real users of the website

**Put `--workers 1` if you want to debug it, monkey patch is only applied if workers are greater that 1. It helps in debugging**

```
--output
```
How do you want to save the output
Currently supporting `file` and `mongodb` ( For mongo db , please update the `.env`)
Default `file`

```
--type
```
Might be required in future, if you want to add other kind of crawlers
For now only `--type website_links` works
Default is `website_links`

From your activated virtualenv please run `python -m app.main --url 'http://bbc.co.uk' --workers 50 --output file --type website_links`
The result file would be present in output directory

### Highlights of projects
1) Tried to used OOPS, SOLID and 12-factor app design
2) app.connection module - connection wrapper, can be used in any project. Generally I would ship this to python libs which the organisation can install and use
3) app.services ( store services ) - based on input, I inject the storage engine. It can be also be done via Factory method and dependency injection via configuration file
These services are also reusable and not not dependent on anything
4) app_logging.py - Control complete logging of app and injected in the very beginning. The log files are stored in logs directory and rotated automatically.
5) proxy - Is not implemented yet, but the lrequest service can directly use it when request start failing
6) config.py - Handles environment (maily from os or .env )
7) setting.py - Control all the setting of app
8) main.py - Entry point
9) services.lrequest.lizard_request.py -> Handle all request and retries
10) website_links.py -> Basically use gevent and all other services to give the desired results
11) The project make sure there is no deadlock or thread-safety is considered.
12) All edge cases are considered ( http == https, remove fragment, what is queue is empty, no url requested twice)
13) Result is written into file or db in chunks


### Todos

1) add return types and data types for services - Not needed for now , partially done
2) add auth make sure right people are accessing it - Not needed
3) use session in requests
4) monkey patch only required libs - Not needed
5) push error-urls ( 404, 401, 408 etc ) into separate output files, although they are already getting printed and written to log files
6) canonical host names. The use might want bbc.com also as it is canonical to bbc.co.uk in some cases
7) Ignore files ( urls end with .pdf. .mp3 etc ) - Not needed
8) Add S3 output - Not needed
9) Add MongoDB output - Done
10) Add Postgres output - Not needed
11) Setup Proxy Services ( Request Modify, Free Proxy, Paid Proxy) - Setup done , but not usable, implementation pending
12) Setup Captcha bypass - Not needed
13) Factory method and dependency injection - Partially done, rest not needed for now
14) No difference between http and https ( mark both as crawled ) - Done
15) Input url validation and modification - Done
16) Dockerize - Will do on Sunday if time, simple docker file only
17) README.md - Partially done
