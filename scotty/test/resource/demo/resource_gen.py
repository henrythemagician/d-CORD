import logging

logger = logging.getLogger(__name__)

def deploy(context):
    resource = context.v1.resource
    logger.info('Hey there,')
    logger.info('I\'m resource generator {}'.format(resource.name))
    endpoint = {
        'url': 'https://demo.resouces',
        'user': 'scotty',
        'password': '***********',
    }
    logger.info('endpoint: {}'.format(endpoint))
    return endpoint

def clean(context):
    resource = context.v1.resource
    logger.info('I\'m resource cleaner {}'.format(resource.name))
    pass
