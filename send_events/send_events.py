#!/usr/bin/env python

# https://jira.deutsche-glasfaser.de/browse/REQ-2929
import logging
from socket import gaierror

import requests, click
from urllib3.exceptions import NewConnectionError


def getlogger():
    LOGGER = 'sf_send_events'
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    formatter = logging.Formatter(FORMAT)
    log = logging.getLogger(LOGGER)
    ch = logging.FileHandler(filename=f'{LOGGER}.log')
    ch.setFormatter(formatter)
    log.addHandler(ch)
    return log


@click.command()
@click.argument('filename')
@click.option('--isp', type=click.Choice(['DGH', 'DGB', 'NEW'], case_sensitive=False), default='DGH')
def sendEvents(filename, isp='DGH'):
    url = 'https://jsonplaceholder.typicode.com/posts'
    log = getlogger()
    with open(filename, 'r') as f:
        for cnt, line in enumerate(f):
            customer_id = line.rstrip('\n')
            try:
                response = requests.post(url, data = {'isp': isp.upper(), 'customer_id': customer_id, 'event':'create' })
                if response.status_code != 201:
                    log.info(f'ERROR for customer {customer_id} : response code {response.status_code}')
                    # append to error

                else:
                    log.info(f'Succes for customer {customer_id} : response code {response.status_code}')
                    log.debug(response.json())
                    # append to out
            except :
                print(f'ERROR for customer {customer_id} : ConnectionError')


if __name__ == '__main__':
    sendEvents()
