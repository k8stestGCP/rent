from google.cloud import pubsub_v1
import asyncio
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path('united-crane-423621-t9', 'verification-book-sub')
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('united-crane-423621-t9', 'verification-rent')

subscriberAuth = pubsub_v1.SubscriberClient()
subscription_auth_path = subscriberAuth.subscription_path('united-crane-423621-t9', 'verification-response')

publisherAuth = pubsub_v1.PublisherClient()
topic_pathAuth = publisherAuth.topic_path('united-crane-423621-t9', 'verification')

def request_verification(token: str, id: str):
    # Initialize Pub/ clien

    messageBook = str(id).encode('utf-8')
    messageAuth = str(token).encode('utf-8')
    print(f"Sending message: {messageBook} to {topic_path}")
    print(f"Sending message: {messageAuth} to {topic_pathAuth}")
    futureAuth = publisherAuth.publish(topic_pathAuth, data=messageAuth)
    futureBook = publisher.publish(topic_path, data=messageBook)
    
    futureAuth.result()  
    futureBook.result()

def process_message(message):
    status = message.data.decode('utf-8')
    if status == "OK":
        return True  
    return False

async def subscribe_to_book_topic():
    event = asyncio.Event()  # Event to signal status change
    tracker = False
    
    def callback(message):
        nonlocal event, tracker
        # Process the message (verify the user) and send the response
        status = message.data.decode('utf-8')

        # Acknowledge the message
        message.ack()
        
        if status == "OK":
            print("Received OK")
            tracker = True
            event.set()  # Set the event to signal status change
        elif status == "ERROR":
            raise Exception("User verification failed")
    # Subscribe to the verification response topica
    subscriber.subscribe(subscription_path, callback=callback)

    # Wait for the event to be set
    await event.wait()
    return tracker

async def subscribe_to_auth_topic():
    event = asyncio.Event()  # Event to signal status change
    tracker = False

    def callback(message):
        nonlocal event, tracker  # Access outer event and tracker variables

        # Process the message (verify the user) and send the response
        status = message.data.decode('utf-8')

        # Acknowledge the message
        message.ack()

        if status == "OK":
            tracker = True  # Update the outer tracker variable
            print("Received OK")
            event.set()  # Set the event to signal status change
        elif status == "ERROR":
            raise Exception("User verification failed")
    # Subscribe to the verification response topic
    subscriber.subscribe(subscription_auth_path, callback=callback)

    # Wait for the event to be set
    await event.wait()

    return tracker