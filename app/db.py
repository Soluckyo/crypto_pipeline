from psycopg2 import pool
import psycopg2
import time
import os

connection_pool = pool.SimpleConnectionPool(
    minconn=2,
    maxconn=8,
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)

def get_connection():
    return connection_pool.getconn()

def release_connection(conn):
    connection_pool.putconn(conn)
