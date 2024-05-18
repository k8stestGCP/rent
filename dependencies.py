from fastapi import Depends, HTTPException, status, Request
from pubsub import request_verification, subscribe_to_book_topic, subscribe_to_auth_topic
from models import Rent
import asyncio

async def verify_token(request: Request, id: int):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not provided"
        )
    token = token.split("Bearer ")[1]

    request_verification(token, id)
    try:

        resultBook=subscribe_to_book_topic(),
        resultAuth=subscribe_to_auth_topic()
        
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User verification failed"
        )
    print(resultBook, resultAuth)
    return resultBook and resultAuth
