import pandas as pd
import sqlite3

def cleanData(filename):
    df = pd.read_parquet(filename,engine='auto')

    print("There are {0} rows and {1} columns".format(df.shape[0],df.shape[1]))


    for c in df.columns:
        if df[c].isnull().values.any():
            print("There are Nan( or None) in {0}".format(c))

    df = df.dropna(how='any')

    print("Now there are {0} rows and {1} columns".format(
        df.shape[0], df.shape[1]))


    df.rename(columns={df.columns[9]: "price_after_discount"},inplace=True)

    df.rename(columns={df.columns[10]: "items_left_in_stocks"},inplace=True)

    return df

def createTable(df):


    try:
        db = sqlite3.connect('aboutyou.db')
        c = db.cursor()


        sql_create = """CREATE TABLE sales (ID INTEGER PRIMARY KEY, product_id int, brand_name text, category_name text,
        product_group_name text, product_group_gender text, style_group text,
         season text, items_sold text, price_before_discount text, price_after_discount text, 
         items_left_in_stocks int, active_since_days int, dayofyear int, normalized_number_of_visitors int, 
         discount int, is_sale_campaign_day int, is_holiday int)"""

        c.execute(sql_create)

        df.to_sql('sales', db, if_exists="replace", index=False)

        sql_alter = """ALTER TABLE sales RENAME TO tmp"""

        c.execute(sql_alter)

        sql_create = """CREATE TABLE sales (ID INTEGER PRIMARY KEY, product_id int, brand_name text,
         category_name text,product_group_name text, product_group_gender text, style_group text,
         season text, items_sold text, price_before_discount text, price_after_discount text,
         items_left_in_stocks int, active_since_days int, dayofyear int, normalized_number_of_visitors int,
         discount int, is_sale_campaign_day int, is_holiday int)"""

        c.execute(sql_create)

        sql_insert = """ INSERT INTO sales (product_id, brand_name, category_name,
        product_group_name, product_group_gender, style_group,
         season, items_sold, price_before_discount, price_after_discount,
         items_left_in_stocks, active_since_days, dayofyear, normalized_number_of_visitors,
         discount, is_sale_campaign_day, is_holiday)
         SELECT product_id, brand_name, category_name,
        product_group_name, product_group_gender, style_group,
         season, items_sold, price_before_discount, price_after_discount,
         items_left_in_stocks, active_since_days, dayofyear, normalized_number_of_visitors,
         discount, is_sale_campaign_day, is_holiday FROM tmp"""

        c.execute(sql_insert)

        sql_drop = "DROP TABLE tmp"

        c.execute(sql_drop)

        db.commit()


    except sqlite3.Error as e:
        print(e)

    return db



