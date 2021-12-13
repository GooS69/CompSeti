import asyncio


async def handle_client(reader, writer):
    address = writer.get_extra_info('peername')
    print("Client:", address)
    while True:
        request = (await reader.read(1024)).decode('utf8')
        if not request:
            break
        response = str(request)
        print(f"Message '{response}' from {address}")
        writer.write(response.encode('utf8'))
        await writer.drain()
    print(f"Connection closed {address}")
    writer.close()


async def run_server():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 5050)
    async with server:
        await server.serve_forever()

asyncio.get_event_loop().run_until_complete(run_server())