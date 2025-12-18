from typing import MutableMapping, Any, Callable, Awaitable

type Scope = MutableMapping[str, Any]
type Message = MutableMapping[str, Any]
type Receive = Callable[[], Awaitable[Message]]
type Send = Callable[[Message], Awaitable[None]]


total_connections = 0


async def handle_lifespan(scope: Scope, receive: Receive, send: Send) -> None:
    while True:
        message = await receive()
        
        if message["type"] == "lifespan.startup":
            print("Lifespan startup event received")
            await send({"type": "lifespan.startup.complete"})
            
        elif message["type"] == "lifespan.shutdown":
            print("Lifespan shutdown event received")
            await send({"type": "lifespan.shutdown.complete"})
            return
        

async def hello_endpoint(scope: Scope, receive: Receive, send: Send) -> None:
    response_start = {
        "type": "http.response.start",
        "status": 200,
        "headers": [
            [b"content-type", b"text/plain"],
        ],
    }
    await send(response_start)
    
    response_body = {
        "type": "http.response.body",
        "body": b"Hello, world!",
        "more_body": False,
    }
    await send(response_body)


async def goodbye_endpoint(scope: Scope, receive: Receive, send: Send) -> None:
    response_start = {
        "type": "http.response.start",
        "status": 200,
        "headers": [
            [b"content-type", b"text/plain"],
        ],
    }
    await send(response_start)
    
    response_body = {
        "type": "http.response.body",
        "body": b"Goodbye, world...",
        "more_body": False,
    }
    await send(response_body)


async def not_found_endpoint(scope: Scope, receive: Receive, send: Send) -> None:
    response_start = {
        "type": "http.response.start",
        "status": 404,
        "headers": [
            [b"content-type", b"text/plain"],
        ],
    }
    await send(response_start)
    
    response_body = {
        "type": "http.response.body",
        "body": b"Not Found",
        "more_body": False,
    }
    await send(response_body)


async def handle_http(scope: Scope, receive: Receive, send: Send) -> None:
    while True:
        message = await receive()
        print(f"HTTP received message: {message}")
        
        if message["type"] == "http.disconnect":
            print("HTTP client disconnected")
            return
        
        if message["type"] == "http.request":
            if scope["path"] == "/hello" and scope["method"] == "GET":
                await hello_endpoint(scope, receive, send)
            elif scope["path"] == "/goodbye" and scope["method"] == "GET":
                await goodbye_endpoint(scope, receive, send)
            else:
                await not_found_endpoint(scope, receive, send)
            return
        

async def app(scope: Scope, receive: Receive, send: Send) -> None:
    global total_connections
    total_connections += 1
    current_connection = total_connections
    print(f"Connection {current_connection}: Scope: {scope}")
    
    if scope["type"] == "lifespan":
        await handle_lifespan(scope, receive, send)
    elif scope["type"] == "http":
        await handle_http(scope, receive, send)
    
    print(f"Connection {current_connection}: Completed")


def main():
    import uvicorn
    
    uvicorn.run(
        app,
        port=5000,
        log_level="info",
        use_colors=False,
    )


if __name__ == "__main__":
    main()