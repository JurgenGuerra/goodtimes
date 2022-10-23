# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import requests
import json

import psycopg2

from config import config


def create_table_batch():
    sql = """CREATE TABLE IF NOT EXISTS "batchs"(
    "id_batchs" SERIAL PRIMARY KEY,
    "name" TEXT NOT NULL,
    "description" TEXT NOT NULL,
    "images" JSON NOT NULL,
    "attributes" JSON NOT NULL)
    """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def create_table_emails():
    sql = """CREATE TABLE IF NOT EXISTS "emails"(
    "email" TEXT PRIMARY KEY,
    "walletpk" VARCHAR(255) NOT NULL,
    "wallet" VARCHAR(255) NOT NULL)
    """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def create_table_sent():
    sql = """CREATE TABLE IF NOT EXISTS "sent"(
    "email" TEXT NOT NULL,
    "id_batchs" INTEGER NOT NULL,
    "tx_hash" VARCHAR(255) NOT NULL)
    """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def add_foreign_keys():
    sql = """ALTER TABLE
    "sent" ADD CONSTRAINT "sent_destination_foreign" FOREIGN KEY("email") REFERENCES "emails"("email");
ALTER TABLE
    "sent" ADD CONSTRAINT "sent_batch_foreign" FOREIGN KEY("id_batchs") REFERENCES "batchs"("id_batchs");
    """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


create_table_batch()

create_table_emails()

create_table_sent()

add_foreign_keys()

# ! jupytext --to py setup_db.ipynb


