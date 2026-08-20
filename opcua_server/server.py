import asyncio
from asyncua import Server

async def main():

    server = Server()

    # OPC-UA server endpoint
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    # Create namespace
    uri = "http://hmi-web-migration-poc"
    idx = await server.register_namespace(uri)

    # Create Device1
    device = await server.nodes.objects.add_object(idx, "Device1")

    # Create variables
    speed = await device.add_variable(idx, "Speed", 50.0)
    temperature = await device.add_variable(idx, "Temperature", 82.0)
    pressure = await device.add_variable(idx, "Pressure", 10.0)

    # Allow writing to these variables
    await speed.set_writable()
    await temperature.set_writable()
    await pressure.set_writable()

    print("Starting OPC-UA server...")

    async with server:
        print("OPC-UA server is running.")
        print("Endpoint: opc.tcp://localhost:4840/freeopcua/server/")

        while True:
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())