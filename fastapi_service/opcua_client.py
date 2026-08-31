from asyncua import Client
import yaml

OPC_UA_URL = "opc.tcp://localhost:4840/freeopcua/server/"

class OPCUAClient:

    def __init__(self):

        self.client = Client(OPC_UA_URL)
        self.nodes = {}
        self.tag_config = {}

    def load_tag_config(self):

        with open("tags.yaml", "r") as file:

            config = yaml.safe_load(file)

        self.tag_config = config.get("tags", {})
    # CONNECT

    async def connect(self):
        await self.client.connect()
        print("Connected to OPC-UA server.")
        self.load_tag_config()
        await self.discover_nodes()

    # DISCONNECT

    async def disconnect(self):

        await self.client.disconnect()
        print("Disconnected from OPC-UA server.")

    # AUTO DISCOVER OPC-UA NODES

    async def discover_nodes(self):
        objects = self.client.nodes.objects

        # Find Machine

        production_line = await self.find_child(
            objects,
            "ProductionLine1"
        )

        machine = await self.find_child(
            production_line,
            "Machine1"
        )

        # Categories under Machine

        categories = [
            "Telemetry",
            "Controls",
            "Status"
        ]

        # Discover every variable automatically

        for category_name in categories:

            category = await self.find_child(
                machine,
                category_name
            )

            children = await category.get_children()

            for node in children:

                # Get node class
                node_class = await node.read_node_class()

                # We only want Variable nodes
                if node_class.name != "Variable":
                    continue

                browse_name = await node.read_browse_name()

                tag_name = browse_name.Name

                self.nodes[tag_name] = node

                print(
                    f"Discovered: {category_name}/{tag_name}"
                )

        print(
            f"Discovered {len(self.nodes)} OPC-UA nodes."
        )

    # FIND CHILD NODE

    async def find_child(self, parent, name):
        children = await parent.get_children()
        for child in children:
            browse_name = await child.read_browse_name()
            if browse_name.Name == name:
                return child

        raise Exception(
            f"Node '{name}' not found."
        )

    # =========================================================
    # READ VALUE
    # =========================================================

    async def read_value(self, tag):

        if tag not in self.nodes:

            raise Exception(
                f"Unknown tag: {tag}"
            )

        return await self.nodes[tag].read_value()


    # =========================================================
    # WRITE VALUE
    # =========================================================

# =========================================================
# WRITE VALUE
# =========================================================

    async def write_value(self, tag, value):

        if tag not in self.nodes:

            raise Exception(
                f"Unknown tag: {tag}"
            )

        # Get tag configuration from tags.yaml
        config = self.tag_config.get(tag)

        if not config:

            raise Exception(
                f"No configuration found for tag: {tag}"
            )

        tag_type = config.get("type")

        # Only controls and commands can be written
        writable_types = [
            "control",
            "command"
        ]

        if tag_type not in writable_types:

            raise PermissionError(
                f"Tag '{tag}' is read-only "
                f"(type: {tag_type})"
            )

        node = self.nodes[tag]

        # Read existing value to determine data type
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