1) add return types and data types for services - Not needed for now , partially done
2) add auth make sure right people are accessing it - Not needed
3) use session in requests
4) monkey patch only required libs - Not needed
5) push error-urls ( 404, 401, 408 etc ) into separate output files, although they are already getting printed and written to log files
6) canonical host names. The use might want bbc.com also as it is canonical to bbc.co.uk in some cases
7) Ignore files ( urls end with .pdf. .mp3 etc )
8) Add S3 output - Not needed
9) Add MongoDB output - Done
10) Add Postgres output - Not needed
11) Setup Proxy Services ( Request Modify, Free Proxy, Paid Proxy) - Setup done , but not usable, implementation pending
12) Setup Captcha bypass - Not needed
13) Factory method and dependency injection - Partially done, rest not needed for now
14) No difference between http and https ( mark both as crawled ) - Done
15) Input url validation and modification - Done
16) Dockerize - Will do on Sunday if time, simple docker file only
17) README.md - Working