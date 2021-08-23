## Fetch Rewards Coding Exercise - Data Analyst

by Nicholas Kopystynsky

#### in terminal commands

If you don't have the docker container
> docker run -d -p 5432:5432 --name my-postgres -e POSTGRES_PASSWORD=123456 postgres

Otherwise open existing docker container
> docker start my-postgres

Run python script (only needs to be run once, even if you exit the docker container)
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

exit postgres
> \q

exit container
> ctrl+c ctrl+d

stop container
> docker stop my-postgres

### Queries

When considering average spend from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?
When considering total number of items purchased from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?
> SELECT rewardsReceiptStatus, COUNT(purchaseditemcount) AS purchases, SUM(purchaseditemcount) AS items_bought, AVG(totalspent) AS average_spent FROM receipts GROUP BY rewardsReceiptStatus HAVING rewardsReceiptStatus IN ('REJECTED', 'FINISHED');

 rewardsreceiptstatus | purchases | items_bought |   average_spent
----------------------+-----------+--------------+--------------------
 REJECTED             |        71 |          173 | 23.326055781942017
 FINISHED             |       518 |         8184 |  80.85430524938356

#### Source
https://fetch-hiring.s3.amazonaws.com/data-analyst/ineeddata-data-modeling/data-modeling.html