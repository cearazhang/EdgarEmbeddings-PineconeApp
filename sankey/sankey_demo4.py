import plotly.graph_objects as go

# link certain genes to cancers
source = [0, 0, 1, 1, 1, 2, 2, 2]
target = [3, 4, 5, 3, 5, 3, 4, 5]
value = [1, 1, 1, 1, 2, 2, 0.5, 1]
# node 3 goes to node 2 with thickness 3

label = ['stomach', 'lung', 'brain', 'Gx', 'Gy', 'Gz']

link_colors = ['lightgray'] * 8
link_colors[0] = 'yellow'
link_colors[3] = 'rgba(145, 154, 232, 0.5)'
link_colors[5] = '#f4b212'
# makes left side one color, and right side another
node_colors = ['mediumslateblue'] * 3 + ['palegoldenrod'] * 3

lk = {'source': source, 'target': target, 'value': value,
      'line': {'color': 'black', 'width': 2},
      'color': link_colors}

node = {'label': label, 'pad': 50, 'thickness': 50,
        'line': {'color': 'black', 'width': 2},
        'color': node_colors}
# pad defines spacing, thickness defines thickness of the node

sk = go.Sankey(link=lk, node=node)
fig = go.Figure(sk)
fig.show()

