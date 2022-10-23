from eth_account import Account
import requests
import json
import random
import psycopg2
from config import config, cross, nftport, simplehash, dinary

def insert_batch(name, description):
    """
    Save the name and description for each collection
    Arguments:
        name: collection name
        description: short description for each nft or collection
    """
    sql = "INSERT INTO batchs (name, description, images, attributes) VALUES(%s, %s, '{}', '{}') returning id_batchs;"
    conn = None
    id_of_new_row = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (name, description))
        id_of_new_row = cur.fetchone()[0]
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            
    return id_of_new_row

def insert_emails_list(email_list):
    data_email_list = []
    for email in email_list:
        acct = Account.create(email)
        data_email_list.append((email, acct.privateKey, acct.address))
    sql = "INSERT INTO emails(email, walletpk, wallet) VALUES(%s, %s, %s) ON CONFLICT DO NOTHING"
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.executemany(sql, data_email_list)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return True

def insert_images(images, id_batchs):
    sql = "UPDATE batchs SET images = %s WHERE id_batchs = %s"
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (images, id_batchs))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return True

def insert_images(images, id_batchs):
    sql = "UPDATE batchs SET images = %s WHERE id_batchs = %s"
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (images, id_batchs))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return True

def get_batch_metadata(id_batchs):
    """
    A dataframe from aggregated_investments table in order to save a snapshot
    Returns:
        snapshot: a dataframe with all the relevan fields to save
    """
    sql = "SELECT name, description, images FROM batchs WHERE id_batchs = %s"
    conn = None
    data = []
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (id_batchs,))
        batch_data = cur.fetchone()
        data = {'name': batch_data[0], 'description': batch_data[1], 'images': batch_data[2]}
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return data

def get_emails_to_send(id_batchs):
    """
    A dataframe from aggregated_investments table in order to save a snapshot
    Returns:
        snapshot: a dataframe with all the relevan fields to save
    """
    sql = "SELECT emails.email, emails.wallet FROM sent, emails WHERE sent.id_batchs = %s AND sent.email = emails.email AND sent.tx_hash IS NULL"
    conn = None
    data = []
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (id_batchs,))
        email_users = cur.fetchall()
        for row in email_users:
            data.append({'email': row[0], 'wallet': row[1]})
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return data

def insert_sent_list(sent_list):
    sql = "INSERT INTO sent(id_batchs, email) VALUES(%s, %s) ON CONFLICT DO NOTHING"
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.executemany(sql, sent_list)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return True

def update_sent_list(sent_list):
    sql = "UPDATE sent SET tx_hash = %s WHERE id_batchs = %s AND email = %s"
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.executemany(sql, sent_list)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return True

def send_nft(address, name, description, image_url):
    nftport_params = nftport()
    headers={"Authorization": nftport_params['nftport_secret'], "Content-Type": "application/json"}
    payload = {
        "chain": "polygon",
        "name": name,
        "description": description,
        "file_url": image_url,
        "mint_to_address": address
    }
    response = requests.post('https://api.nftport.xyz/v0/mints/easy/urls', json=payload, headers=headers)
    return response.json()

def send_batch_nfts(id_batchs):
    emails_data = get_emails_to_send(id_batchs = id_batchs)
    batch_data = get_batch_metadata(id_batchs = id_batchs)
    sent_data = []
    for user in emails_data:
        metadata = {
            'name': batch_data['name'],
            'image': random.choice(batch_data['images']['images']),
            'description': batch_data['description'],
        }
        response = send_nft(address=user['wallet'], name=batch_data['name'], description=batch_data['description'], image_url=random.choice(batch_data['images']['images']))
        sent_data.append((response, user['email'], id_batchs))
    return sent_data

def deploy_nfts(id_batchs):
    sent_data = send_batch_nfts(id_batchs)
    if len(sent_data) > 0:
        filtered_sent_data = [(x[0]['transaction_hash'], x[2], x[1]) for x in sent_data]
        update_sent_list(sent_list = filtered_sent_data)

def get_emails_and_txhash(id_batchs):
    """
    A dataframe from aggregated_investments table in order to save a snapshot
    Returns:
        snapshot: a dataframe with all the relevan fields to save
    """
    sql = "SELECT emails.email, emails.wallet, sent.tx_hash FROM sent, emails WHERE sent.id_batchs = %s AND sent.email = emails.email AND sent.tx_hash IS NOT NULL"
    conn = None
    data = []
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (id_batchs,))
        email_users = cur.fetchall()
        for row in email_users:
            data.append({'email': row[0], 'wallet': row[1], 'txid': row[2]})
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return data

def get_wallet_by_email(email):
    """
    A dataframe from aggregated_investments table in order to save a snapshot
    Returns:
        snapshot: a dataframe with all the relevan fields to save
    """
    sql = "SELECT emails.wallet FROM emails WHERE emails.email = %s"
    conn = None
    email_users = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (email,))
        email_users = cur.fetchone()[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return email_users

def get_nfts_by_wallet(wallet):
    simplehash_params = simplehash()
    url = "https://api.simplehash.com/api/v0/nfts/owners?chains=polygon&wallet_addresses=" + wallet
    headers = {
        "accept": "application/json",
        "X-API-KEY": simplehash_params['simplehash_secret']
    }

    response = requests.get(url, headers=headers)
    return (wallet, response.json()['nfts'])

def get_nfts(email):
    data_wallet = get_wallet_by_email(email)
    if data_wallet:
        data = get_nfts_by_wallet(wallet = data_wallet)
        return data
    else:
        return None, None

