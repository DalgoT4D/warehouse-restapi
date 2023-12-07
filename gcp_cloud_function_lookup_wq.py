import functions_framework
from google.cloud import bigquery
import os

@functions_framework.http
def lookup_wq(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    # check the authorization header for api key
    headers = request.headers.get('Authorization', None)
    if headers is None:
        return ("Invalid authorization", 401)

    api_key = headers.split()[-1]

    if api_key != os.environ.get('inrem_api_key', None):
        return ("Invalid authorization", 401)

    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'lat' in request_json and 'long' in request_json:
        q_latitude = request_json['lat']
        q_longitude = request.json['long']
        client = bigquery.Client()
        r = client.query(f"""
            DECLARE target_geo GEOGRAPHY;

            -- Set your target latitude and longitude
            SET target_geo = ST_GEOGPOINT({q_longitude}, {q_latitude});

            WITH distances AS (
            SELECT 
                District_Name, salinity, Arsenic, Iron, Nitrate, Fluoride,
                ST_DISTANCE(
                ST_GEOGPOINT(CAST(longitude AS FLOAT64), CAST(latitude AS FLOAT64)),
                target_geo
                ) AS distance
            FROM 
                `inrem_demo_warehouse.Airbyte`
            )
            SELECT 
                * 
            FROM 
                distances
            ORDER BY 
                distance
            LIMIT 1;
        """)
        results = list(r.result())
        result = results[0]
        return ({
            "result": dict(result.items())
        }, 200)
    else:
        return ("Required parameters: lat and long", 422)

