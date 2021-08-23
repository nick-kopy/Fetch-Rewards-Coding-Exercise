'''
Script written by (mostly) Nicholas Kopystynsky for a take home test.
'''

import json
import gzip
import psycopg2

def populate_sql(url, table):
    '''Populates an existing SQL database with .json.gz zip file data'''
    
    # Start with Python's connection to PostgreSQL database
    # Note: must have a postgres docker container running locally

    conn = psycopg2.connect(dbname='postgres',
                            host='localhost',
                            user='postgres',
                            password='123456')
    
    cur = conn.cursor()
    
    # Defining some variables that change depending on what data you want
    if table == 'brands':
        keys = ['_id_$oid', 'barcode', 'brandCode', 'category', 
                'categoryCode', 'cpg_$ref', 'topBrand', 'name']
        schema = '''
            CREATE TABLE brands (
                _id VARCHAR(24), 
                barcode BIGINT, 
                brandCode VARCHAR(64),
                category VARCHAR(64),
                categoryCode VARCHAR(64),
                cpg VARCHAR(24),
                topBrand BOOL,
                name VARCHAR(64)
            );
            '''
        empty_query = '''
            INSERT INTO brands
            VALUES (
            '{0}', '{1}', '{2}', '{3}', '{4}', '{5}', {6}, '{7}'
            );
            '''
    elif table == 'users':
        keys = ['_id_$oid', 'state', 'createdDate_$date', 'lastLogin_$date',
                'role', 'active']
        schema = '''
            CREATE TABLE users (
                _id VARCHAR(24),
                state VARCHAR(2),
                createdDate VARCHAR(13),
                lastLogin VARCHAR(13),
                role VARCHAR(12),
                active BOOL
            );
            '''
        empty_query = '''
            INSERT INTO users
            VALUES (
            '{0}', '{1}', '{2}', '{3}', '{4}', {5}
            );
            '''
    elif table == 'receipts':
        keys = ['_id_$oid', 'bonusPointsEarned', 'bonusPointsEarnedReason',
                'createDate_$date', 'dateScanned_$date', 'finishedDate_$date',
                'modifyDate_$date', 'pointsAwardedDate_$date', 'pointsEarned',
                'purchaseDate_$date', 'purchasedItemCount',
                'rewardsReceiptStatus', 'totalSpent', 'userId']
        schema = '''
            CREATE TABLE receipts (
                _id VARCHAR(24),
                bonusPointsEarned INT,
                bonusPointsEarnedReason VARCHAR(128),
                createDate VARCHAR(13),
                dateScanned VARCHAR(13),
                finishedDate VARCHAR(13),
                modifyDate VARCHAR(13),
                pointsAwardedDate VARCHAR(13),
                pointsEarned REAL,
                purchaseDate VARCHAR(13),
                purchasedItemCount INT,
                rewardsReceiptStatus VARCHAR(12),
                totalSpent REAL,
                userId VARCHAR(24)
            );
            '''
        empty_query = '''
            INSERT INTO receipts
            VALUES (
            '{0}', '{1}', '{2}', '{3}', '{4}', '{5}', {6}, '{7}',
            '{8}', '{9}', '{10}', '{11}', '{12}', '{13}'
            );
            '''
    else:
        print("Couldn't tell what data you wanted")
        return None
    
    cur.execute(schema)
    
    # Now data. First unzip raw data
    with gzip.open(url, 'r') as file:
        bytes_data = file.read()
        data_str = bytes_data.decode('utf-8')

    # Separate different rows of data, list of strings
    data = data_str.split('\n')

    # Loops through each "row" and inserts into SQL database
    for i in range(len(data)-1):
        # Get data from row
        vals = row_to_sql(data, i, keys)
        
        # Populate empty query with row data
        query = empty_query.format(*vals)

        # Replacing 'NULL' varchar with NULL type
        query = query.replace("'NULL'", "NULL")

        cur.execute(query)
    
    conn.commit()

# Useful recursive function to flatten any given JSON row
# Copied from https://www.geeksforgeeks.org/flattening-json-objects-in-python/

def flatten_json(y):
    out = {}
  
    def flatten(x, name =''):
          
        # If the Nested key-value 
        # pair is of dict type
        if type(x) is dict:
              
            for a in x:
                flatten(x[a], name + a + '_')
                  
        # If the Nested key-value
        # pair is of list type
        elif type(x) is list:
              
            i = 0
              
            for a in x:                
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x
  
    flatten(y)
    return out

def row_to_sql(data, num, keys):
    # Returns a list of values (as strings) at a given row 
    # so it can fit into SQL
    
    row = flatten_json(json.loads(data[num]))

    vals = ['NULL'] * len(keys)

    # All 'NULL' unless data is available
    for i, k in enumerate(keys):
        if k in row.keys():
            a = row[k]
            if isinstance(a, str):
                a = a.replace("'", '')
            vals[i] = a
    
    return vals

if __name__ == '__main__':
    populate_sql(url='data/users.json.gz', table='users')
    populate_sql(url='data/brands.json.gz', table='brands')
    populate_sql(url='data/receipts.json.gz', table='receipts')
    
    print('SQL tables generated successfully')