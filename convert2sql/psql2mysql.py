import re

def convert_pg_to_mysql(pg_sql_file, mysql_sql_file):
    with open(pg_sql_file, 'r') as pg_file:
        pg_sql = pg_file.read()

    # Convert CREATE TABLE syntax
    mysql_sql = pg_sql.replace('DOUBLE PRECISION', 'DOUBLE')
    mysql_sql = re.sub(r'COPY (\w+) FROM STDIN WITH NULL \'\' CSV;', '', mysql_sql)

    # Prepare for LOAD DATA INFILE syntax
    table_name = re.search(r'CREATE TABLE (\w+)', mysql_sql).group(1)
    csv_file_path = 'output.csv'  # Assuming the CSV file is named output.csv
    load_data_infile = f"LOAD DATA INFILE '{csv_file_path}' INTO TABLE {table_name} " \
                       f"FIELDS TERMINATED BY ',' ENCLOSED BY '\"' " \
                       f"LINES TERMINATED BY '\\n' " \
                       f"IGNORE 1 LINES;"

    # Combine the converted CREATE TABLE and LOAD DATA INFILE
    mysql_sql = mysql_sql + '\n' + load_data_infile

    # Write the converted SQL to a new file
    with open(mysql_sql_file, 'w') as mysql_file:
        mysql_file.write(mysql_sql)

# Convert the SQL file
convert_pg_to_mysql('cars_info.sql', 'cars_info_mysql.sql')


# 功能不完整