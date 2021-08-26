## Fetch Rewards Coding Exercise - Data Analyst

by Nicholas Kopystynsky  
Exercise source [here](https://fetch-hiring.s3.amazonaws.com/data-analyst/ineeddata-data-modeling/data-modeling.html)

### Letter to stakeholder

Dear stakeholder,

I have finished moving the compressed data to our structured database. Most information transitioned without incident however one data quality issue is worth attention.

Some amount of the receipts did not come with item information. Without this info we cannot link users/purchases with different brands and cannot perform any associated analysis. It's worth investigating why this is missing and if there's some pattern in what's missing. Without that we run the risk of bad statistics and making moves on false information.

Besides that about 10-20% of the data is missing things like a user's state or a brand's category. It shouldn't be a major issue unless these specific things are being analyzed. 

The receipts data also has item lists which don't lend themselves to the SQL database easily. It's qualitative data and definitely worth keeping even in it's current format for answering questions like "how have snack purchases grown recently?" The drawbacks being time investment to look into it and that it won't scale up as well outside the SQL database.

Lastly I was able to answer your question about spending and item count on purchases with accepted or rejected bonus points. Accepted points purchases included 8184 items cumulatively and an average of $81.85 per purchase. Rejected points purchases on the other hand were 173 items cumulatively at an average of $23.32 per perchase. 

I'm happy to discuss my findings or clarify anything, just shoot me a message.

Best regards,  
Nicholas Kopystynsky

#### in terminal commands

If you already have Python and docker on your machine you can run the python script in this repository and query the SQL database yourself!

If you don't have a postgres docker container
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

*execute queries like the one below!*

exit postgres
> \q

exit container
> ctrl+c ctrl+d

stop container
> docker stop my-postgres

### Data analysis

Checkout *exploration.ipynb* for a quick and dirty quality check on the data. See a sample of the data and what's missing.

### Queries

When considering average spend from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?  
When considering total number of items purchased from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?  
> SELECT rewardsReceiptStatus, COUNT(purchaseditemcount) AS purchases, SUM(purchaseditemcount) AS items_bought, AVG(totalspent) AS average_spent FROM receipts GROUP BY rewardsReceiptStatus HAVING rewardsReceiptStatus IN ('REJECTED', 'FINISHED');

> rewardsreceiptstatus | purchases | items_bought |   average_spent  
> ----------------------+-----------+--------------+--------------------  
> REJECTED             |        71 |          173 | 23.326055781942017  
> FINISHED             |       518 |         8184 |  80.85430524938356  