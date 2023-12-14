from node_module.models import nodeModel


def create_and_update_nodes():
    nodes: nodeModel = nodeModel.objects.all()
    if nodes is None:
        return "there are not any node in database"
    else:
        for node in nodes:
            with open(f"real_estate_blockchain/settings_{node.node_port}.py", "") as file:
                file.write(
                    f"""
from .settings import *
                    
SESSION_COOKIE_NAME = 'real_estate_blockchain_session_port_{node.node_port}'
                    
"""
                )
                file.close()
