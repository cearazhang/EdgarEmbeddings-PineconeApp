import plotly.graph_objects as go

source = [0, 0]
target = [1, 2]
value = [2, 1]

# 0 goes to 1, with a thickness of 2

lk = {'source': source, 'target': target, "value": value}
sk = go.Sankey(link=lk)
fig = go.Figure(sk)
fig.show()

