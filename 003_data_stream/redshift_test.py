import psycopg2

try:
    rs_conn = psycopg2.connect(
        host="my-redshift-cluster.cl3xx4umwp5d.eu-central-1.redshift.amazonaws.com",
        port="5439",
        user="awsuser",
        password="rMSP$w0tswp",
        dbname="dev"
    )
    print("Połączenie udane!")
except psycopg2.OperationalError as e:
    print(f"Błąd połączenia: {e}")