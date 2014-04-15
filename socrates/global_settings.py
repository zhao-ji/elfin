# coding: utf-8

import logging

logging.basicConfig(filename='log/run.log',
                    filemode='w',
                    format='%(asctime)s %(levelname)-8s \
                                %(name)-15s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO
                    )

import redis

