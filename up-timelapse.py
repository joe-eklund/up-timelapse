import click
import requests

import logging
import os

from datetime import datetime
from urllib.parse import urlparse

@click.group
@click.option(
    '--log-level',
    default='INFO',
    type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                      case_sensitive=False),
    help='Logging level to use.'
)
def cli(log_level):
    logging.basicConfig(level=log_level)

@cli.command()
@click.option(
    '--url',
    '-u',
    multiple=True,
    help='URL(s) of camera(s) to grab screenshot (e.g. http://192.168.1.1/snap.jpeg)'
)
@click.option(
    '--save-location',
    default='./',
    help='Folder to save snapshots to.'
)
def grab_screens(url, save_location):
    logging.info('Grabbing screens.')
    create_output_dir(save_location=save_location)
    for u in url:
        logging.debug(f'Grabbing screen from: {u}.')
        data = requests.get(u, stream=True)
        camera_folder = os.path.join(save_location, urlparse(u).netloc)
        create_output_dir(save_location=camera_folder)
        ts = datetime.fromtimestamp(datetime.timestamp(datetime.now()))
        screen_path = os.path.join(camera_folder, f'{ts}.jpg')
        logging.debug(f'Saving screen to {screen_path}.')
        with open(screen_path,'wb') as f:
            for chunk in data.iter_content():
                f.write(chunk) 

def create_output_dir(save_location):
    logging.info(f'Verifying output directory: {save_location}.')
    logging.debug('Checking if output directory exists.')
    if not os.path.isdir(save_location):
        logging.debug('Creating new output directory.')
        os.makedirs(save_location)
    else:
        logging.debug('Output directory already exists.')

if __name__ == '__main__':
    cli()