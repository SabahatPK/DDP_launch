from flask import Flask, jsonify, request, render_template
import flask
import numpy as np
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
import cufflinks as cf
cf.go_offline()
import plotly.express as px
from flask import Markup
from flask_cors import CORS
import pandas as pd
import plotly.graph_objects as go
from itertools import cycle
from urllib.request import urlopen
import json

input_data_file = "Data/updatedData.csv"
df = pd.read_csv(input_data_file, encoding='latin1')
print("DATA HAS BEEN LOADED")

class GraphGenerator:
    def generate_choropleth_graph(self):
        input_data_file = 'Data/Data4Pakistan-AllData.csv'  
        df = pd.read_csv(input_data_file)
        choropleth_df = df.loc[df['Year']==2014]
        choropleth_df = choropleth_df[["Province", "District", "Poverty Rate (%)"]]
        # choropleth_df= choropleth_df.sort_values(by=['National poverty rank (N)']).reset_index()
        choropleth_df = choropleth_df.dropna().reset_index(drop=True)
        districts_mapping = {'Attock': 'Attok', 'Batagram': 'Battagram', 'Dera Ghazi Khan': 'Dera Ghazi Kha', 
                        'Gujranwala': 'Gujranwala 1', 'Jacobabad': 'Jakobabad','Jaffarabad': 'Jafarabad',
                        'Karachi City': 'Karachi Central', 'Kohlu': 'Kholu', 
                        'Las Bela': 'Lasbela', 'Malakand PA': 'Malakand P.A.', 
                        'Mirpur Khas': 'Mirphurkhas', 'Narowal': 'Narowal 1','Naushahro Feroze': 'Naushahro Firoz',
                        'Rahim Yar Khan': 'Rahimyar Khan', 'Rajanpur': 'Rajan Pur', 
                        'Tando Allah Yar': 'Tando Allahyar', 'Tando Muhammad Khan': 'Tando M. Khan',
                        'Killa Abdullah': 'Qilla Abdullah', 'Killa Saifullah': 'Qilla Saifullah',
                    } 

        duplicate_areas_df = pd.DataFrame({"Province":["Sindh", "Sindh", "Sindh", "Punjab", "Punjab", "Punjab"], 
                            "District":["Karachi East", "Karachi South", "Karachi west", "Gujranwala 2", "Narowal 2",
                                    "Okara 1"],
                                        "Poverty Rate (%)":[17.0, 17.0, 17.0, 18.0, 21.0, 28.0]   }) 

        gujranwala_areas_df = pd.DataFrame({""})
        for index, district in enumerate(choropleth_df['District']):
            if districts_mapping.get(district):
                choropleth_df['District'][index] = districts_mapping.get(district)
        choropleth_df=choropleth_df.append(duplicate_areas_df).sort_values(by=['District']) 

        with open("Data/pakistan-districts.json", encoding='utf-8', errors='ignore') as read_file:
            districts = json.load(read_file)

        fig = px.choropleth_mapbox(choropleth_df, geojson=districts, locations='District', color='Poverty Rate (%)',
                                featureidkey="properties.NAME_3",
                                mapbox_style="carto-positron",
                                center={'lat':31, 'lon':70},
                                zoom=4,
                                opacity = 0.7
                                )

        # fig.show()
        html_graph = fig.to_html(full_html=False)
        Html_file= open("choropleth_graph/choropleth_graph.html","w")
        Html_file.write(html_graph)
        Html_file.close()
        print("CHOROPLETH GRAPH CREATED")


    def generate_bar_chart(self):
        input_data_file = 'Data/Data4Pakistan-AllData.csv'  
        df = pd.read_csv(input_data_file)
        bar_df = df.loc[df['Year']==2014]
        bar_df = bar_df[["Province", "District", "National poverty rank (N)", "Year"]]
        bar_df= bar_df.sort_values(by=['National poverty rank (N)']).reset_index()
        bar_df.dropna(inplace=True)
        import plotly.graph_objects as go
        plotly_colors_list = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']
        # color_discrete_map = {'Balochistan': 'rgb(255,0,0)', 'Punjab': 'rgb(0,255,0)', 'Sindh': 'rgb(0,0,255)',
        #                                   'Khyber Pakhtunkhwa': 'rgb(150,55,0)', 'Federal Capital Territory': 'rgb(100,0,255)'}

        color_discrete_map = {'Balochistan': '#636EFA', 'Punjab': '#EF553B', 'Sindh': '#00CC96',
                                        'Khyber Pakhtunkhwa': '#AB63FA', 'Federal Capital Territory': '#FFA15A'}

        fig = go.Figure()
        provinces_added = []

        for index, province in enumerate(bar_df["Province"]):
            show_province = False
            if province not in provinces_added:
                provinces_added.append(province)
                show_province = True
                
            fig.add_trace(go.Bar(
                x=bar_df.iloc[[index]]["District"], 
                y=bar_df.iloc[[index]]["National poverty rank (N)"], 
                name= province,
                marker_color=color_discrete_map[province],
                legendgroup = province,
                showlegend = show_province,
            ))

        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(barmode='group', xaxis_tickangle=-45)
        fig.update_xaxes(showticklabels=False)
        # fig.show()
        html_graph = fig.to_html(full_html=False)
        Html_file= open("bar_chart/bar_chart.html","w")
        Html_file.write(html_graph)
        Html_file.close()
        print("BAR CHART CREATED")


    def generate_slope_graphs(self):
        input_data_file = "Data/updatedData.csv"
        df = pd.read_csv(input_data_file, encoding='latin1')
        print('IN SLOPE GRAPHS')
        generated_plots = []
        
    
        palette = cycle(px.colors.qualitative.Bold)

        def create_slope_graphs(starting_year, ending_year, grouped_df, indicator_name):
            for name, group in grouped_df:
                dist_groups = group.groupby(['District'])
                print(name.upper())

                fig = go.Figure()

                # Set axes ranges
                fig.update_xaxes(range=[2004, 2014])
                fig.update_yaxes(range=[0, 100])

                for dis_name, dis_group in dist_groups:
                    dis_group = dis_group.reset_index(drop=True)
            #         print(dis_group)

                    min_year =  dis_group.loc[dis_group['Year']==2004]
                    max_year =  dis_group.loc[dis_group['Year']==2014]

                    if len(min_year) != 0 and  len(max_year) != 0:
                        fig.add_trace(go.Scatter(
                            x=dis_group['Year'],
                            y=dis_group[indicator_name],
                            name=dis_name,
                            mode="lines",
                            opacity = 1,
                            marker = dict(size =0.5 ,  line=dict(width=0.1)),
                        ))
                fig.update_layout(legend_title_text='Cities')       
                # fig.show()
                print("Figure Created")
                # generated_plots.append(fig.to_html(full_html=False))
                html_graph = fig.to_html(full_html=False)
                
                Html_file= open("slope_graphs/{}_slope_graph.html".format(name),"w")
                Html_file.write(html_graph)
                Html_file.close()

        starting_year = 2004
        ending_year = 2014

        indicator_name = 'Poverty Rate (%)'

        new_df = df[['Province', 'District', 'Year' , indicator_name]]
        grouped_df = new_df.groupby(['Province'])

        create_slope_graphs(starting_year, ending_year, grouped_df, indicator_name)
 

graph_generator = GraphGenerator()
graph_generator.generate_slope_graphs()
graph_generator.generate_bar_chart()
graph_generator.generate_choropleth_graph()

    
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
            color_discrete_map = {'Balochistan': 'rgb(255,0,0)', 'Punjab': 'rgb(0,255,0)', 'Sindh': 'rgb(0,0,255)',
                                  'Khyber Pakhtunkhwa': 'rgb(50,255,0)', 'Federal Capital Territory': 'rgb(100,0,255)'}
            new_df = None
            print("Province=", Province, "and Indicator=", x)
            if Province == "allProv":
                new_df = df[df['Year'] == Year].reset_index(drop=True)
                new_df1 = new_df[[y, x]]
                print(new_df1)
                fig = px.scatter(new_df1,x=x, y=y, color=new_df['Province'], color_discrete_map=color_discrete_map)
                fig.update_layout(legend_title_text='Province')
        
            else:    
                new_df = df[(df['Province'] == Province) & (df['Year'] == Year)].reset_index(drop=True)
                new_df1 = new_df[[y, x]]
                print("PROVO={}".format(color_discrete_map[Province]))
                fig = px.scatter(new_df1,x=x, y=y, color=new_df['Province'], color_discrete_map=dict({Province:color_discrete_map[Province]})) 
                fig.update_layout(legend_title_text='Province')
            # fig.show(config=dict(displaylogo=False,
            #                 modeBarButtonsToRemove=["zoomIn2d", 'lasso2d', 'zoom2d']))
            
            output['generated_plot'] = fig.to_html(full_html=False)
            output['is_success'] = True
            output['message'] = 'Plot generated successfully'
            # print("Text=", output['generated_plot'])

        
    except Exception as e:
        print("ERROR RAISED", str(e))
        output['message'] = str(e)
    
    if output['is_success'] is True:
        print("SUCCESSFULL")
        return jsonify(output)
    else:
        print("FAILED")
        return jsonify(output)

 

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=5555, debug=True, use_reloader=False)