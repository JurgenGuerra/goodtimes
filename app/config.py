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

from dotenv import dotenv_values
variables = dotenv_values(".env") 


def config():
    config_values = dict(user=variables['USERNAME'],
    password = variables['PASSWORD'],
    host = variables['HOST'],
    port = variables['PORT'],
    database = variables['DATABASE'])
    return config_values


def cross():
    cross_values = dict(cross_secret = variables['CROSS_SECRET'],
    cross_id = variables['CROSS_ID'])
    return cross_values


def nftport():
    nftport_values = dict(nftport_secret = variables['NFTPORT_SECRET'])
    return nftport_values


def simplehash():
    simplehash_values = dict(simplehash_secret = variables['SIMPLEHASH'])
    return simplehash_values


def dinary():
    dinary_values = dict(dinary_secret = variables['CLOUDINARY_URL'])
    return dinary_values

# ! jupytext --to py config.ipynb

# +
# config()
# -




