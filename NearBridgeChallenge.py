from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Load the data
df = pd.read_excel("data.xlsx")
# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# Define the layout of the dashboard
app.layout = dbc.Container([
dbc.Row([
dbc.Col(html.H1("NEAR Bridge Activity Dashboard"), className="mb-2")
]),
dbc.Tabs([
dbc.Tab(label='Overview', tab_id='tab-overview'),
dbc.Tab(label='User Behavior', tab_id='tab-user-behavior'),
dbc.Tab(label='Grail Program Impact', tab_id='tab-grail-impact'),
dbc.Tab(label='Deep Dive', tab_id='tab-deep-dive'),
], id='tabs', active_tab='tab-overview'),
html.Div(id='content')
])

# Callback to render the content of each tab
@app.callback(Output('content', 'children'), [Input('tabs', 'active_tab')])
def render_content(tab):
    if tab == 'tab-overview':
        return render_overview()
    elif tab == 'tab-user-behavior':
        return render_user_behavior()
    elif tab == 'tab-grail-impact':
        return render_grail_impact()
    elif tab == 'tab-deep-dive':
        return render_deep_dive()

def render_overview():
    total_volume = df['amount_usd'].sum()
    volume_over_time = px.line(df, x='block_timestamp', y='amount_usd', title='Bridging Volume Over Time')
    inbound_outbound = df.groupby('direction')['amount_usd'].sum().reset_index()
    inbound_outbound_pie = px.pie(inbound_outbound, names='direction', values='amount_usd', title='Inbound vs Outbound')
    top_chains = df.groupby('source_chain')['amount_usd'].sum().nlargest(5).reset_index()
    top_chains_bar = px.bar(top_chains, x='source_chain', y='amount_usd', title='Top 5 Source Chains')
    top_tokens = df.groupby('symbol')['amount_usd'].sum().nlargest(5).reset_index()
    top_tokens_bar = px.bar(top_tokens, x='symbol', y='amount_usd', title='Top 5 Bridged Tokens')

    return html.Div([
    dbc.Row([
    dbc.Col(html.H2(f"Total Bridged Volume: ${total_volume:,.2f}"), className="mb-4")
    ]),
    dbc.Row([
    dbc.Col(dcc.Graph(figure=volume_over_time), width=6),
    dbc.Col(dcc.Graph(figure=inbound_outbound_pie), width=6),
    ]),
    dbc.Row([
    dbc.Col(dcc.Graph(figure=top_chains_bar), width=6),
    dbc.Col(dcc.Graph(figure=top_tokens_bar), width=6),
    ]),
    ])

def render_user_behavior():
    # Placeholder: Add logic for user behavior analysis here
    return html.Div([
    html.H3("User Behavior"),
    # Add user behavior charts and metrics here
    ])

def render_grail_impact():
    # Placeholder: Add logic for Grail program impact analysis here
    return html.Div([
    html.H3("Grail Program Impact"),
    # Add Grail program impact charts and metrics here
    ])

def render_deep_dive():
    # Placeholder: Add logic for deep dive analysis here
    return html.Div([
    html.H3("Deep Dive"),
    # Add deep dive analysis components here
    ])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
