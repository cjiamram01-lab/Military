import pika
import time

# Connection parameters
credentials = pika.PlainCredentials('admin', 'Bangy123#')  # Use your credentials
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='192.168.16.159',
        port=5672,
        credentials=credentials
    )
)

try:
    # Create a channel
    channel = connection.channel()

    # Declare a queue
    queue_name = 'test_queue'
    channel.queue_declare(queue=queue_name, durable=True)

    # Send test messages
    for i in range(5):
        message = f"Test message {i + 1}"
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            )
        )
        print(f" [x] Sent: {message}")
        time.sleep(1)  # Wait 1 second between messages

finally:
    # Close the connection
    connection.close()