from node_module.models import nodeModel
import json
import hashlib


def create_and_update_nodes():
    nodes: nodeModel = nodeModel.objects.all()
    if nodes is None:
        return "there are not any node in database"
    else:
        for node in nodes:
            node: nodeModel
            with open(f"real_estate_blockchain/settings_{node.node_port}.py", "w") as file:
                file.write(
                    f"""
from .settings import *
                    
SESSION_COOKIE_NAME = 'real_estate_blockchain_session_port_{node.node_port}'
                    
"""
                )
                file.close()

        # for node in nodes:
        #     node: nodeModel
        #     with open(f'utils/nodes_DB/{node.node_port}_DB.json', 'w') as json_file:
        #         json_file.close()


def create_node_address(info):
    info_str: str = json.dumps(info)
    sha512 = hashlib.sha512()
    sha512.update(info_str.encode('utf-8'))
    sha512_digest = sha512.digest()
    contract_address = sha512_digest[-20:].hex()
    return f'0x{contract_address}'
