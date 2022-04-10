import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc


application = app = Dash(
    '__name__',
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
)

server = app.server


app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Data Visualization Solution</title>
        {%favicon%}
        {%css%}
        <link rel="stylesheet" href="https://unpkg.com/aos@next/dist/aos.css" />
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <script src="https://unpkg.com/aos@next/dist/aos.js"></script>
        <script>
            window.addEventListener('load', function() {

                AOS.init({

                // Global settings:
                disable: false, // accepts following values: 'phone', 'tablet', 'mobile', boolean, expression or function
                startEvent: 'DOMContentLoaded', // name of the event dispatched on the document, that AOS should initialize on
                initClassName: 'aos-init', // class applied after initialization
                animatedClassName: 'aos-animate', // class applied on animation
                useClassNames: false, // if true, will add content of `data-aos` as classes on scroll
                disableMutationObserver: false, // disables automatic mutations' detections (advanced)
                debounceDelay: 50, // the delay on debounce used while resizing window (advanced)
                throttleDelay: 99, // the delay on throttle used while scrolling the page (advanced)

                // Settings that can be overridden on per-element basis, by `data-aos-*` attributes:
                offset: 120, // offset (in px) from the original trigger point
                delay: 0, // values from 0 to 3000, with step 50ms
                duration: 500, // values from 0 to 3000, with step 50ms
                easing: 'ease', // default easing for AOS animations
                once: true, // whether animation should happen only once - while scrolling down
                mirror: false, // whether elements should animate out while scrolling past them
                anchorPlacement: 'top-bottom', // defines which position of the element regarding to window should trigger the animation

                });

            });
        </script>
    </body>
</html>
'''


df = pd.read_excel('quarterly-advertising-spend.xlsx')
melt = pd.melt(df, id_vars=['Category'], var_name='Quarter', value_name='Spend')


def chart_1():
    fig = px.bar(melt, x="Spend", y="Category", color="Quarter", barmode="group", orientation='h')
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    return fig


def chart_2():
    fig = px.bar(melt, x="Category", y="Spend", color="Quarter")
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    return fig


def chart_3():
    percentages = get_percentages()
    fig = go.Figure([
        go.Bar(
            name = 'Quarter 2 (22.8k Total Spend)',
            x = df['Category'],
            y = df['Quarter 2']
        ),
        go.Bar(
            name = 'Quarter 3 (25.9k Total Spend)',
            x = df['Category'],
            y = df['Quarter 3'],
            text = percentages,
            textposition='outside',
            textfont_color='red'
        )
    ])
    fig.update_layout(barmode='group', xaxis_title='Category', yaxis_title='Spend', legend_title_text='Quarter')
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig.update_yaxes(dtick=2000, range=[0, 18000])
    return fig


def get_percentages():
    percentages = []
    q2_spendings = df['Quarter 2'].tolist()
    q3_spendings = df['Quarter 3'].tolist()
    num_categories = 10
    i = 0
    while(i < num_categories):
        q2_value = q2_spendings[i]
        q3_value = q3_spendings[i]
        if q2_value > 0 and q3_value > 0:
            p = round((q3_value - q2_value) / q2_value * 100)
            percentages.append(f'{p}%')
        else:
            percentages.append(' ')
        i = i + 1
    return percentages


app.layout = html.Div([

    html.Div([
        dbc.NavbarSimple(brand="Data Visualization Solution by Naif", color="#ffffff", class_name='shadow-sm', fluid='lg')
    ], **{'data-aos':'fade-up'}),

    dbc.Container([

        html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4('Introduction', className='card-title'),
                            html.P("I have created a Dash application to display my solution. I have used Plotly to create the charts. Bootstrap was used to create the GUI. Furthermore, along with this Dash application I have created several slides to display my solution and I have provided a link to the GitHub repository of this Dash application.", className='card-text'),
                            html.Div([
                                dbc.Card([
                                    dbc.CardHeader("Links"),
                                    dbc.CardBody([
                                        dbc.Row([
                                            dbc.Col([
                                                html.A([
                                                    html.Img(src='/static/github.png', height='50px', **{'data-aos':'zoom-in', 'data-aos-delay':'500'})
                                                ], href='https://github.com/MrNaifS/dash-app')
                                            ], class_name='text-center'),
                                            dbc.Col([
                                                html.Div("View the code of this Dash application by visiting the GitHub repository.", **{'data-aos':'zoom-in', 'data-aos-delay':'500'})
                                            ], class_name='d-none d-lg-block'),
                                            dbc.Col([
                                                html.A([
                                                    html.Img(src='/static/powerpoint.png', height='50px', **{'data-aos':'zoom-in', 'data-aos-delay':'500'})
                                                ], href='/static/data-visualization-solution-by-naif.pdf', download=True)
                                            ], class_name='border-start text-center'),
                                            dbc.Col([
                                                html.Div("If the Dash application is not sufficient, view these slides that I have created.", **{'data-aos':'zoom-in', 'data-aos-delay':'500'})
                                            ], class_name='d-none d-lg-block')
                                        ], class_name='d-flex align-items-center')
                                    ])
                                ], class_name='shadow-sm')
                            ], **{'data-aos':'zoom-in'})
                        ])
                    ], class_name='shadow-sm')
                ])
            ], class_name='mt-4', id='test')
        ], **{'data-aos':'fade-up'}),

        html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4('Step 1', className='card-title'),
                            html.P('I have mentioned the advantages and disadvantages of each of the four given data view options. Switch between the following tabs to see my analysis of each option.', className='card-text'),
                            html.Div([
                                dbc.Card([
                                    dbc.CardHeader(
                                        dbc.Tabs([
                                                dbc.Tab(label="Option 1", tab_id="option-1"),
                                                dbc.Tab(label="Option 2", tab_id="option-2"),
                                                dbc.Tab(label="Option 3", tab_id="option-3"),
                                                dbc.Tab(label="Option 4", tab_id="option-4"),
                                        ], id='tabs', active_tab="option-1")
                                    ),
                                    dbc.CardBody(
                                        dbc.Row([
                                            dbc.Col([
                                                html.Img(id='tab-image', src='/static/option-1.png', className='img-fluid', **{'data-aos':'zoom-in', 'data-aos-delay':'500'})
                                            ], className='text-center d-flex align-items-center', lg=6),
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Table([
                                                        html.Thead([
                                                            html.Tr([
                                                                html.Th([
                                                                    html.I(className="bi bi-plus-circle me-2"),
                                                                    "Advantages"
                                                                ]),
                                                                html.Th([
                                                                    html.I(className="bi bi-dash-circle me-2"),
                                                                    "Disadvantages"
                                                                ])
                                                            ])
                                                        ]),
                                                        html.Tbody([
                                                            html.Tr([
                                                                html.Td("All spendings of the two quarters are shown."),
                                                                html.Td("Hard to analyze how spending has changed between the two quarters.")
                                                            ]),
                                                            html.Tr([
                                                                html.Td("All spendings for all relevant channels are shown."),
                                                                html.Td("Hard to analyze how spending varies by channel.")
                                                            ])
                                                        ])
                                                    ], id='tab-table')
                                                ], **{'data-aos':'zoom-in', 'data-aos-delay':'500'})
                                            ], lg=6)
                                        ], class_name='g-3')
                                    )
                                ], class_name='shadow-sm')
                            ], **{'data-aos':'zoom-in'})
                        ])
                    ], class_name='shadow-sm')
                ])
            ], class_name='mt-4')
        ], **{'data-aos':'fade-up'}),

        html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4('Step 2', className='card-title'),
                            html.P('I have created two visuals that can be used to communicate the data. They have advantages but I do not consider them to be the most ideal options.', className='card-text'),
                            dbc.Row([
                                dbc.Col([
                                    html.Div([
                                        dbc.Card([
                                            dbc.CardHeader("Pairwise Horizontal Bars"),
                                            dbc.CardBody([
                                                html.Div([
                                                    dcc.Graph(figure=chart_1())
                                                ], **{'data-aos':'zoom-in', 'data-aos-delay':'500'})
                                            ])
                                        ], class_name='shadow-sm')
                                    ], **{'data-aos':'zoom-in'})
                                ], lg=6),
                                dbc.Col([
                                    html.Div([
                                        dbc.Card([
                                            dbc.CardHeader("Stacked Bars"),
                                            dbc.CardBody([
                                                html.Div([
                                                    dcc.Graph(figure=chart_2())
                                                ], **{'data-aos':'zoom-in', 'data-aos-delay':'500'})
                                            ])
                                        ], class_name='shadow-sm')
                                    ], **{'data-aos':'zoom-in'})
                                ], lg=6),
                            ], class_name='g-3')
                        ])
                    ], class_name='shadow-sm')
                ])
            ], class_name='mt-4')
        ], **{'data-aos':'fade-up'}),

        html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4('Step 3', className='card-title'),
                            html.P('I have chosen the following chart to be the most effective way of communicating the data. It is advantageous because the spendings of each quarter and of each category can be compared side by side with a percentage value that indicates the changes between the two quarters.', className='card-text'),
                            html.Div([
                                dbc.Card([
                                    dbc.CardHeader("Pairwise Vertical Bars"),
                                    dbc.CardBody([
                                        html.P("From the following chart we can see that direct mail continues to be the highest category in terms of spending with a 10% increase in the third quarter. Furthermore, spending on radio advertisements has decreased by 28% in the third quarter. Meanwhile, during the third quarter the company has started spending on mobile advertisements unlike the second quarter where the company did not spend at all on mobile advertisements.", className="card-text"),
                                        html.Div([
                                            dcc.Graph(figure=chart_3())
                                        ], **{'data-aos':'zoom-in', 'data-aos-delay':'500'})
                                    ])
                                ], class_name='shadow-sm')
                            ], **{'data-aos':'zoom-in'})
                        ])
                    ], class_name='shadow-sm')
                ])
            ], class_name='mt-4')
        ], **{'data-aos':'fade-up'})

    ], class_name='pb-4', fluid='lg')
    
])


@app.callback(
    Output("tab-image", "src"),
    Output("tab-table", "children"),
    Input("tabs", "active_tab")
)
def tab_content(active_tab):

    image = f'/static/{active_tab}.png'
    table_header = [html.Thead(html.Tr([html.Th([html.I(className="bi bi-plus-circle me-2"), "Advantages"]), html.Th([html.I(className="bi bi-dash-circle me-2"), "Disadvantages"])]))]

    if active_tab == 'option-1':
        row1 = html.Tr([html.Td("All spendings of the two quarters are shown."), html.Td("Hard to analyze how spending has changed between the two quarters.")])
        row2 = html.Tr([html.Td("All spendings for all relevant channels are shown."), html.Td("Hard to analyze how spending varies by channel.")])
        table_body = [html.Tbody([row1, row2])]
        return image, table_header + table_body
    
    elif active_tab == 'option-2':
        row1 = html.Tr([html.Td("Easy to analyze how spending varies by channel for a quarter."), html.Td("Total spending of Q2 is not shown. Thus, analyzing  how spending has changed between the two quarters is impossible.")])
        row2 = html.Tr([html.Td("Easy to understand."), html.Td("Cannot immediately determine the spendings by channel since only percentages are shown.")])
        row3 = html.Tr([html.Td(""), html.Td("Total spending of Q3 is in millions but it is actually in thousands.")])
        row4 = html.Tr([html.Td(""), html.Td("Several channels are combined into a single category.")])
        row5 = html.Tr([html.Td(""), html.Td("Percentages are misleading since total spendings of the two quarters are not equal.")])
        table_body = [html.Tbody([row1, row2, row3, row4, row5])]
        return image, table_header + table_body
    
    elif active_tab == 'option-3':
        table_header = [html.Thead(html.Tr([html.Th([html.I(className="bi bi-dash-circle me-2"), "Disadvantages"])]))]
        row1 = html.Tr([html.Td("Total spendings are not shown. Thus, analyzing  how spending has changed between the two quarters is impossible.")])
        row2 = html.Tr([html.Td("Cannot determine the spendings by channel since only percentages are shown.")])
        row3 = html.Tr([html.Td("Cannot immediately determine the percentage of each channel.")])
        row4 = html.Tr([html.Td("Hard to determine the mapping between the labels and the stacked bars.")])
        table_body = [html.Tbody([row1, row2, row3, row4])]
        return image, table_header + table_body
    
    else:
        row1 = html.Tr([html.Td("Easy to analyze how spending has changed between the two quarters."), html.Td("Cannot distinguish between Q2 and Q3 since the bars are not labeled.")])
        row2 = html.Tr([html.Td("Easy to analyze how spending varies by channel."), html.Td("Spendings are in thousands but the y-axis is in millions.")])
        table_body = [html.Tbody([row1, row2])]
        return image, table_header + table_body


if __name__ == '__main__':
    app.run_server(debug=False)