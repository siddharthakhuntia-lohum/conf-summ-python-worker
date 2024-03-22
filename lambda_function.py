import json
from application import process_jobs as process_event


def lambda_handler(event, context):
    """
    Lambda handler function.
    :param event: Event data passed to the function.
    :param context: Lambda context object.
    :return: A dictionary containing a success message.
    """
    try:
        # Your processing logic here
        process_event(event)

        # Return a success response
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Worker function executed successfully'})
        }
    except Exception as e:
        # Return an error response
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error occurred', 'error': str(e)})
        }
