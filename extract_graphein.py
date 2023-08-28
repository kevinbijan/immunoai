from graphein.protein.config import ProteinGraphConfig
from graphein.protein.visualisation import plotly_protein_structure_graph
from graphein.protein.edges.distance import add_hydrogen_bond_interactions, add_peptide_bonds
from graphein.protein.graphs import construct_graph
from graphein.protein.features.nodes.amino_acid import amino_acid_one_hot
from graphein.ml import ProteinGraphListDataset, GraphFormatConvertor
import graphein.protein as gp
import torch_geometric
import dgl
import torch
import warnings
warnings.filterwarnings('ignore')

config = ProteinGraphConfig(**{"node_metadata_functions": [amino_acid_one_hot]})

target = "/edward-slow-vol/CPSC_552/alpha_structure/rank_1_prediction_Immunogenicity_00045.pdb"

def convert_graphein(x):
    g = construct_graph(config=config, path= x)

    convertor = GraphFormatConvertor(src_format="nx", dst_format="pyg")
    g = gp.extract_subgraph_from_chains(g, ["A","B"])

    data = convertor(g)

    # for idx, (n, d) in enumerate(g.nodes(data=True)):
    #     print(d)

    # one hot
    a = torch_geometric.utils.to_torch_coo_tensor(data['edge_index'])
    one_hot = [d['amino_acid_one_hot'] for n, d in g.nodes(data=True)]
    node_features = torch.tensor(one_hot)
    data.x = node_features

    row, col = data.edge_index

    g = dgl.graph((row, col))

    g.ndata['x'] = data['coords']
    g.ndata['f'] = data['x']
    g.edata['d'] = torch_geometric.utils.to_edge_index(a)[1]
    g.edata['w'] = torch.unsqueeze(torch.ones(g.edata['d'].shape),1)
    return g

print(convert_graphein(target))


# original
# if data.edge_index is not None:
#     row, col = data.edge_index
# else:
#     row, col, _ = data.adj_t.t().coo()

# g = dgl.graph((row, col))

# for attr in data.node_attrs():
#     g.ndata[attr] = data[attr]
# for attr in data.edge_attrs():
#     if attr in ['edge_index', 'adj_t']:
#         continue
#     g.edata[attr] = data[attr]

# return g