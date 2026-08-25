from asyncua import Client

OPC_UA_URL = "opc.tcp://localhost:4840/freeopcua/server/"

class OPCUAClient:

    def __init__(self):
        self.client = Client(OPC_UA_URL)
        self.nodes = {}

    async def connect(self):

        await self.client.connect()

        print("Connected to OPC-UA server.")

        await self.discover_nodes()

    async def disconnect(self):

        await self.client.disconnect()

        print("Disconnected from OPC-UA server.")

    async def discover_nodes(self):

        objects = self.client.nodes.objects

        production_line = await self.find_child(
            objects,
            "ProductionLine1"
        )

        machine = await self.find_child(
            production_line,
            "Machine1"
        )

        telemetry = await self.find_child(
            machine,
            "Telemetry"
        )

        controls = await self.find_child(
            machine,
            "Controls"
        )

        status = await self.find_child(
            machine,
            "Status"
        )

        # ---------------------------------------------------------
        # Telemetry
        # ---------------------------------------------------------

        telemetry_names = [
            "MotorSpeed",
            "MotorTemperature",
            "MotorCurrent",
            "ProcessTemperature",
            "ProcessPressure",
            "TankLevel",
            "Vibration",
            "FlowRate",
            "MotorPower",
        ]

        for name in telemetry_names:

            node = await self.find_child(
                telemetry,
                name
            )

            self.nodes[name] = node

        # ---------------------------------------------------------
        # Controls
        # ---------------------------------------------------------

        control_names = [
            "SpeedSetpoint",
            "TemperatureSetpoint",
            "StartCommand",
            "StopCommand",
        ]

        for name in control_names:

            node = await self.find_child(
                controls,
                name
            )

            self.nodes[name] = node

        # ---------------------------------------------------------
        # Status
        # ---------------------------------------------------------

        status_names = [
            "MachineRunning",
            "MachineStatus",
            "FaultActive",
            "HighTemperatureAlarm",
            "HighPressureAlarm",
            "ProductionCount",
        ]

        for name in status_names:

            node = await self.find_child(
                status,
                name
            )

            self.nodes[name] = node

        print(
            f"Discovered {len(self.nodes)} OPC-UA nodes."
        )

    async def find_child(self, parent, name):

        children = await parent.get_children()

        for child in children:

            browse_name = await child.read_browse_name()

            if browse_name.Name == name:
                return child

        raise Exception(
            f"Node '{name}' not found."
        )

    async def read_value(self, tag):

        if tag not in self.nodes:
            raise Exception(
                f"Unknown tag: {tag}"
            )

        return await self.nodes[tag].read_value()

    async def write_value(self, tag, value):

        if tag not in self.nodes:
            raise Exception(
                f"Unknown tag: {tag}"
            )

        node = self.nodes[tag]

        current_value = await node.read_value()

        if isinstance(current_value, bool):
            value = bool(value)

        elif isinstance(current_value, float):
            value = float(value)

        elif isinstance(current_value, int):
            value = int(value)

        elif isinstance(current_value, str):
            value = str(value)

        await node.write_value(value)