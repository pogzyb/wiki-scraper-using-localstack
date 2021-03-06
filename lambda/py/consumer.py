import logging
import base64
import json

logger = logging.getLogger(__name__)


def lambda_handler(event, context):
    """
    Process events from the Kinesis stream.
    **Nothing fancy happens; just logs the data.

    :param event: the event that this function will process
    :param context: context object for the function
    :return:
    """
    logger.info(f'lambda handler is processing [{len(event["Records"])}] events.')
    for record in event['Records']:
        decoded = base64.b64decode(record['kinesis']['data'])
        payload = json.loads(decoded)
        logger.info(f'event data: {payload}')
