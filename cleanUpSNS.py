import boto3

client = boto3.client('sns')


def is_disabled(endpoint_arn):
    attributes = client.get_endpoint_attributes(EndpointArn=endpoint_arn)
    enabled = attributes['Attributes']['Enabled']
    if enabled == 'false':
        print(', '.join(attributes))
    return enabled == 'false'


def clean_up_subscription(subscription_arn, endpoint_arn):
    print(subscription_arn)
    print(client.unsubscribe(SubscriptionArn=subscription_arn))
    print(endpoint_arn)
    print(client.delete_endpoint(EndpointArn=endpoint_arn))


def list_subscriptions_per_topic(topic_arn):
    subscriptions_deleted = 0
    result = client.list_subscriptions_by_topic(TopicArn=topic_arn)
    next_token = result['NextToken']
    subscriptions_processed = 0
    while next_token is not None:
        subscriptions = result['Subscriptions']
        subscriptions_processed = subscriptions_processed + len(subscriptions)
        for sub in subscriptions:
            endpoint_arn = sub['Endpoint']
            subscription_arn = sub['SubscriptionArn']
            if is_disabled(endpoint_arn):
                subscriptions_deleted = subscriptions_deleted + 1
                print('Deleting subscription')
                print('===================================================================================')
                print(subscriptions_deleted)
                clean_up_subscription(subscription_arn, endpoint_arn)
        print(subscriptions_processed)
        result = client.list_subscriptions_by_topic(TopicArn=topic_arn, NextToken=next_token)
        next_token = result['NextToken']
    print('Subscriptions deleted ' + str(subscriptions_deleted))


if __name__ == '__main__':
    list_subscriptions_per_topic('MY-ARN')