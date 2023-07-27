
"""
sankey.py: a reusable library for sankey visualizations
"""

import plotly.graph_objects as go

lc_map = dict(zip(labels))

# df = df.replace
def _code_mapping(df, src, targ):
    return df, labels

# signature: what is input and output

def make_sankey(df, src, targ, vals):
    """ create a sankey diagram linking src values to
    target values with thickness vals"""

    df, labels = _code_mapping(df, src, targ)
    link = {'source':df[src], 'target':df[targ], 'value':df[vals]}
    # node = {'label': labels}
    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)
    fig.show()

# Get distinct labels
# labels = sorted(list(set(list(df[src]) + list(df[targ]))))
# Get integer codes    codes = list(range(len(labels)))    # Create label to code mapping    lc_map = dict(zip(labels, codes))    # Substitute names for codes in dataframe    df = df.replace({src: lc_map, targ: lc_map})
