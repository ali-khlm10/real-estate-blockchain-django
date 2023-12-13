from node_module.models import nodeModel


def create_and_update_nodes():
    nodes: nodeModel = nodeModel.objects.all()
    if nodes is None:
        return "there are not any node in database"
    else:
        for node in nodes:
            print(node.node_name)


