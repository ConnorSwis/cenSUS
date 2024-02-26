from census import Census
from flask import Flask, request, jsonify, after_this_request, render_template, send_from_directory
from dotenv import load_dotenv
import os

load_dotenv()

c = Census(os.getenv("CENSUS_API_KEY"), year=2019)


def query_census_data(variables, fips):
    state_code = fips[:2] 
    county_code = fips[2:] 
    results = c.acs5.state_county(variables, state_code, county_code)
    return results

app = Flask(__name__)

@app.route('/census', methods=['GET'])
def get_census_data():
    @after_this_request
    def add_header(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    
    variables = request.args.get('variables')
    if variables:
        variables = variables.split(',')
        if "NAME" not in variables:
            variables.insert(0, "NAME")
    else:
        return jsonify({'error': 'At least one variable is required'}), 400
    fips = request.args.get('fips')
    if not fips:
        return jsonify({'error': 'FIPS code is required'}), 400
    results = query_census_data(variables, fips)
    return jsonify(results[0])

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
