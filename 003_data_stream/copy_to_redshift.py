import boto3
import configparser
import psycopg2

# Dane konfiguracyjne do Redshift
parser = configparser.ConfigParser()
parser.read("pipeline.conf")
dbname = parser.get("aws_creds", "database")
user = parser.get("aws_creds", "username")
password = parser.get("aws_creds", "password")
host = parser.get("aws_creds", "host")
port = parser.get("aws_creds", "port")

# Nawiązanie połączenia z klastrem Redshift.
rs_conn = psycopg2.connect(
    "dbname=" + dbname
    + " user=" + user
    + " password=" + password
    + " host=" + host
    + " port=" + port)

# Dane konfiguracyjne S3
parser = configparser.ConfigParser()
parser.read("pipeline.conf")
account_id = parser.get("aws_boto_credentials", "account_id")
iam_role = parser.get("aws_creds", "iam_role")
bucket_name = parser.get("aws_boto_credentials", "bucket_name")

# Wykonanie przedstawionego polecenia COPY w celu wczytania pliku do Redshift.
file_path = ("s3://" + bucket_name + "/order_extract.csv")
role_string = ("arn:aws:iam::" + account_id + ":role/" + iam_role)

sql = "COPY myschema.my_table_copy_python"
sql = sql + " from %s "
sql = sql + " iam_role %s;"

# Utworzenie obiektu kursora i wykonanie polecenia COPY.
cur = rs_conn.cursor()
cur.execute(sql,(file_path, role_string))

# Zamknięcie kursora i zatwierdzenie transakcji.
cur.close()
rs_conn.commit()

# Zamknięcie połączenia.
rs_conn.close()
