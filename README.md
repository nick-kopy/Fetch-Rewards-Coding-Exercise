## Fetch Rewards Coding Exercise - Data Analyst

by Nicholas Kopystynsky

#### in terminal commands

If you don't have the docker container
> docker run -d -p 5432:5432 --name my-postgres -e POSTGRES_PASSWORD=123456 postgres

Otherwise open existing docker container
> docker run my-postgres

Run python script (only needs to be run once)
> python fetch.py

within terminal (local)
> docker exec -it my-postgres bash

within terminal (container)
will ask for password (123456)
> psql -h localhost -p 5432 -U postgres -W

see what databases are present (should include fetch)
> \l

connect to Fetch database
> \c postgres

list tables
> \dt

execute queries