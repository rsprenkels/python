#!/usr/bin/env python

import requests, click

@click.command()
@click.argument('filename')
@click.option('--isp',
              type=click.Choice(['DGH', 'DGB', 'NEW'], case_sensitive=False))
def sendEvents(filename, isp='DGH'):
    url = 'https://jsonplaceholder.typicode.com/posts'

    with open(filename, 'r') as f:
        for cnt, line in enumerate(f):
            customer_id = line.rstrip('\n')
            response = requests.post(url, data = {'isp': isp.upper(), 'customer_id': customer_id, 'event':'create' })

            print(response.json())

if __name__ == '__main__':
    sendEvents()