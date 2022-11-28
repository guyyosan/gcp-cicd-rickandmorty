
from flask import Flask, jsonify
import requests
import shlex
from healthcheck import HealthCheck, EnvironmentDump

health = HealthCheck()
envdump = EnvironmentDump()


app = Flask(__name__)

app.add_url_rule("/healthcheck", "healthcheck", view_func=lambda: health.run())
app.add_url_rule("/environment", "environment", view_func=lambda: envdump.run())

# he
# TODO: flexible endpoint query params?
@app.route("/chars/sp/<species>/st/<status>/o/<origin>", methods=["GET"])
def get_chars(species, status, origin):
    url = "https://rickandmortyapi.com/graphql"

    query = """query {
  locations(page: $page filter: {name: $name}) {
    info {
      next
    }
    results {
      id
      name
    }
  }
}"""

    query_params = {"page": 1, "name": origin}

    r = execute_gql_query(query, query_params, url)
    locations = r["data"]["locations"]["results"]
    while r["data"]["locations"]["info"]["next"]:
        query_params["page"] = r["data"]["locations"]["info"]["next"]
        r = execute_gql_query(query, query_params, url)
        locations_to_add = r["data"]["locations"]["results"]
        locations += locations_to_add

    earth_ids = []
    for location in locations:
        earth_ids.append(location["id"])

    query = """query {
  characters(page: $page filter: {species: $species status: $status }) {
    info {
      next
    }
    results {
      name
      species
      status
      image
      location {
        name
      }
      origin {
        id
      }
    }
  }
}"""
    query_params = {"page": 1, "species": species, "status": status}

    r = execute_gql_query(query, query_params, url)
    chars = r["data"]["characters"]["results"]
    while r["data"]["characters"]["info"]["next"]:
        query_params["page"] = r["data"]["characters"]["info"]["next"]
        r = execute_gql_query(query, query_params, url)
        chars_to_add = r["data"]["characters"]["results"]
        chars += chars_to_add

    chars_by_origin = []
    for char in chars:
        if char["species"] != species:
            continue
        if not char["origin"]["id"]:
            continue
        if char["origin"]["id"] not in earth_ids:
            continue

        chars_by_origin.append({"name": char["name"], "location": char["location"]["name"], "image": char["image"]})

    return jsonify(chars_by_origin)


# returns results as json
def execute_gql_query(query, query_params, url):
    compressed_query = " ".join(shlex.split(query, posix=False))
    for k, v in query_params.items():
        if isinstance(v, str):
            compressed_query = compressed_query.replace(f"${k}", f'"{v}"')
        else:
            compressed_query = compressed_query.replace(f"${k}", str(v))
    r = requests.get(f"{url}?query={compressed_query}")
    return r.json()
