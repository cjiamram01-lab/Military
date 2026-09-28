import pika

# Connection parameters
credentials = pika.PlainCredentials('admin', 'Bangy123#')  # Use your credentials
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='192.168.16.159',
        port=5672,
        credentials=credentials
    )
)

# Create a channel
channel = connection.channel()

# Declare the same queue
queue_name = 'test_queue'
channel.queue_declare(queue=queue_name, durable=True)

def callback(ch, method, properties, body):
    print(f" [x] Received: {body.decode()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Set up consumer
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()