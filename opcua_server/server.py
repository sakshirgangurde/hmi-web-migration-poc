import asyncio
from asyncua import Server
from simulator import simulate
from nodes import create_nodes

async def main():
    server = Server()

    # Configure OPC-UA server
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    # Create namespace
    uri = "http://hmi-web-migration-poc"
    idx = await server.register_namespace(uri)

    # Create OPC-UA information model
    nodes = await create_nodes(server, idx)
    print("Starting OPC-UA server...")

    # Start OPC-UA server
    async with server:
        print("OPC-UA server is running.")

        print(
            "Endpoint: "
            "opc.tcp://localhost:4840/freeopcua/server/")

        # Start simulator
        await simulate(nodes)

if __name__ == "__main__":
    asyncio.run(main())