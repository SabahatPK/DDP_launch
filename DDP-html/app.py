from flask import Flask, jsonify, request, render_template
import flask
import pandas as pd
import numpy as np
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
import cufflinks as cf
cf.go_offline()
import plotly.express as px
from flask import Markup
from flask_cors import CORS
import pandas as pd


input_data_file = "Data/updatedData.csv"
df = pd.read_csv(input_data_file, encoding='latin1')
print("DATA HAS BEEN LOADED")


app = Flask(__name__)
CORS(app)


@app.route('/generate_scatter_plot', methods=['POST'])
def generate_scatter_plot():
    output = {
            'generated_plot': None,
            'is_success': False,
            'message': ''
            }
    
    try:
        if request.method=='POST':

            data = request.get_json()
            
            Province = data['province']            
            Year = 2008
            x = data['indicator'] 
            y = "Poverty Rate (%)"
            new_df = None
            print("Province=", Province, "and Indicator=", x)
            if Province == "allProv":
                new_df = df[df['Year'] == Year].reset_index(drop=True)
            else:    
                new_df = df[(df['Province'] == Province) & (df['Year'] == Year)].reset_index(drop=True)
            new_df = new_df[[y, x]]
            fig = px.scatter(new_df,x=x, y=y) 
            # fig.show(config=dict(displaylogo=False,
            #                 modeBarButtonsToRemove=["zoomIn2d", 'lasso2d', 'zoom2d']))
            
            output['generated_plot'] = fig.to_html(full_html=False)
            output['is_success'] = True
            output['message'] = 'Plot generated successfully'
            # print("Text=", output['generated_plot'])

        
    except Exception as e:
        print("ERROR RAISED")
        output['message'] = str(e)
    
    if output['is_success'] is True:
        print("SUCCESSFULL")
        return jsonify(output)
    else:
        print("FAILED")
        return jsonify(output)

          

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=5555, debug=True, use_reloader=False)