import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
from ast import literal_eval
from cdqa.pipeline import QAPipeline


external_stylesheets = ['assets/design.css', 'spinner.css']
path_to_dataset = 'dataset.csv'
path_to_model = 'models/bert_qa.joblib'

df = pd.read_csv(path_to_dataset, converters={'paragraphs': literal_eval})
cdqa_pipeline = QAPipeline(reader=path_to_model)
cdqa_pipeline.fit_retriever(df=df)
app = dash.Dash(__name__ , external_stylesheets=external_stylesheets)

app.title = 'cdqa-app'
app.layout = html.Div([
    html.Div(html.H1('Question Answering Visualization')),
    dcc.Tabs(id='tabs', children=[
        dcc.Tab(label='Choose a text from the dropdown', value='tab-1',children = [
            html.Div(html.H6('Choose an example from the below list')),
            dcc.Dropdown(
                id='query-dropdown',
                options=[{"label": i, "value": i} for i in df['question_text']],
                value = "Choose a text from the list",
                placeholder="Select a question or type your own question"),
            html.Div(html.H6('Answer')),
            html.Div(id='output-container-answer'),
            html.Div(html.H6('Passage Context')),
            html.Div(id='output-container-context'),
            html.Div(html.H6('Original Document')),
            html.Div(id='output-container-document')
        ]),
        dcc.Tab(label='Input own text', value='tab-2', children=[
            html.Div(html.H6('Type your own question')),
            dcc.Textarea(
                id='textarea',
                placeholder='Input your text here',
                style={'width': '100%', 'height': 100},
            ),
            html.Button('Submit', id='textarea_submit', n_clicks=0),
            html.Div(html.H6('Answer')),
            html.Div(id='output-container-answer2'),
            html.Div(html.H6('Passage Context')),
            html.Div(id='output-container-context2'),
            html.Div(html.H6('Original Document')),
            html.Div(id='output-container-document2')
        ]),
    ]),
], style={'padding': '60px 100px 60px 100px'})
#'background-image': 'url(https://hougumlaw.com/wp-content/uploads/2016/05/light-website-backgrounds-light-color-background-images-light-color-background-images-for-website-1024x640-300x188.jpg)'})


@app.callback(
    [dash.dependencies.Output('output-container-answer', 'children'),
    dash.dependencies.Output('output-container-context', 'children'),
    dash.dependencies.Output('output-container-document', 'children')],
    [dash.dependencies.Input('query-dropdown', 'value')])
def update_tab1(value):
    #return (df[df['question_text']==value]['short_answers']),(df[df['question_text']==value]['paragraphs']),(df[df['question_text']==value]['title'])
    prediction = cdqa_pipeline.predict(query=value)
    return (prediction[0], prediction[2], prediction[1])

@app.callback(
    [dash.dependencies.Output('output-container-answer2', 'children'),
    dash.dependencies.Output('output-container-context2', 'children'),
    dash.dependencies.Output('output-container-document2', 'children')],
    [dash.dependencies.Input('textarea_submit', 'n_clicks')],
    [dash.dependencies.State('textarea', 'value')]
)
def update_tab2(n_clicks, value):
    if n_clicks > 0:
        #return (df[df['question_text']==value]['short_answers']),(df[df['question_text']==value]['paragraphs']),(df[df['question_text']==value]['title'])
        prediction = cdqa_pipeline.predict(query=value)
        return (prediction[0], prediction[2], prediction[1])
    else:
        return [None,None,None]


if __name__ == '__main__':
    app.run_server(debug=True)

