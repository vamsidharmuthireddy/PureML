from pureml.utils.constants import PATH_CONFIG
from pureml.utils.config import load_config
from collections import OrderedDict

def create_nodes(components):
    # print(components)

    nodes = [{'id': component['name'], 'text': component['name']} for component in components]


    return nodes


def create_extra_nodes(nodes, edges):
    # print(components)
    
    node_nodes = [i['id'] for i in nodes]
    edge_nodes = sum([[i['from']]+[i['to']] for i in edges], [])

    extra_nodes = list(set([n for n in edge_nodes if n not in node_nodes]))

    nodes = nodes + [{'id': n, 'text':n} for n in extra_nodes]


    return nodes




def create_edges(components):
    
    edges = []

    def add_node(node_from, node_to):
        edge_id = '--->'.join([node_from, node_to])
        edge = {
            'id': edge_id,
            'from': node_from,
            'to': node_to            
        }

        edges.append(edge)


    for n in components:
        if 'parent' in n.keys():
            node_parent = n['parent']
            node_to = n['name']
                    

            if node_parent is not None:

                if type(node_parent) == list:
                
                    for node_from in node_parent:
                        add_node(node_from, node_to)

                else:
                    add_node(node_parent, node_to)



    return edges




def create_pipeline():
    config = load_config()

    load_data = config['load_data']
    transformer = list(config['transformer'].values())
    dataset = config['dataset']



    pipeline_components = []

    if len(load_data) > 0:
        pipeline_components.append(load_data)
    
    if len(transformer) > 0:
        pipeline_components = pipeline_components + transformer
    
    if len(dataset) > 0:
        pipeline_components.append(dataset)

    # print(pipeline_components)


    edges = create_edges(components=pipeline_components)

    nodes = create_nodes(components=pipeline_components)

    nodes = create_extra_nodes(nodes, edges)
    
    pipeline = {
        'edges': edges,
        'nodes': nodes
    }

    return pipeline





    




# const nodes = [
#   {
#     id: '1',
#     text: '1'
#   },
#   {
#     id: '2',
#     text: '2'
#   }
# ];

# const edges = [
#   {
#     id: '1-2',
#     from: '1',
#     to: '2'
#   }
# ];

