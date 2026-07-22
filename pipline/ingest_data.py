
import click
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from tqdm.auto import tqdm


dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

# function to ingest the data from the sorce
def ingest_data(
    url: str,
    target_table: str,
    engine: Engine,
    chunksize: int = 100000,
) -> None:
    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize,
    )

    first = True

    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.head(0).to_sql(name=target_table, con=engine, if_exists='replace')
            first = False

        df_chunk.to_sql(name=target_table, con=engine, if_exists='append')


@click.command()
@click.option('--pg-user', default='root', show_default=True, help='Postgres username')
@click.option('--pg-pass', default='root', show_default=True, help='Postgres password')
@click.option('--pg-host', default='localhost', show_default=True, help='Postgres host')
@click.option('--pg-port', default='5432', show_default=True, help='Postgres port')
@click.option('--pg-db', default='ny_taxi', show_default=True, help='Postgres database name')
@click.option('--year', type=int, default=2021, show_default=True, help='Data year')
@click.option('--month', type=int, default=1, show_default=True, help='Data month')
@click.option('--chunksize', type=int, default=100000, show_default=True, help='Rows per chunk')
@click.option('--target-table', default='yellow_taxi_data_1_2021', show_default=True, help='Target table')
@click.option(
    '--prefix',
    default='https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/',
    show_default=True,
    help='URL prefix for the dataset',
)
def main(
    pg_user: str,
    pg_pass: str,
    pg_host: str,
    pg_port: str,
    pg_db: str,
    year: int,
    month: int,
    chunksize: int,
    target_table: str,
    prefix: str,
):
    engine = create_engine(
        f'postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'
    )

    url = f'{prefix}yellow_tripdata_{year:04d}-{month:02d}.csv.gz'

    ingest_data(
        url=url,
        target_table=target_table,
        engine=engine,
        chunksize=chunksize,
    )


if __name__ == '__main__':
    main()






