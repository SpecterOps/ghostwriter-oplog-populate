import json
import csv
from dataclasses import dataclass

from pathlib import Path

from asyncio.exceptions import TimeoutError

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError
from graphql.error.graphql_error import GraphQLError

import oplog_generator

# Class definitions
class JSONFileError(Exception):
    """Raised when the JSON config file could not be read"""

@dataclass
class Credential:
    """Credentail objects represent credential configs"""
    url: str
    password: str
    username: str

# Main function definition
def main():
    """
    oplog_populate obtains an authenticated Ghostwriter GraphQL client, then makes API requests
    to create a sample client "SpecterPops", a sample project "SAMPLE PROJECT", 
    and a sample oplog "SpecterPops Sample Oplog". It attempts to read sample oplog entries from
    the file '/auto_populate_oplog/config/oplog.csv". If this file is missing, oplog_generator
    is called to create a sample oplog. This sample oplog has 5000 entries by default.
    """
    config = read_json_config()

    # Load configs
    credentials = load_credential_configs(config)

    try:
        # Use credential configs to get a Ghostwriter token
        gw_auth_token = get_logon_token(credentials)

        # Set up token-based authentication
        headers = {"Authorization": f"Bearer {gw_auth_token}"}
        transport = AIOHTTPTransport(credentials.url, headers=headers)
        authenticated_client = Client(transport=transport, fetch_schema_from_transport=True)

        client_operation = create_sample_client(authenticated_client)

        project_operation = create_sample_project(
            authenticated_client,
            client_operation["insert_client_one"]["id"]
        )

        oplog_operation = create_sample_oplog(
            authenticated_client,
            project_operation["insert_project_one"]["id"]
        )

        populate_oplog(
            authenticated_client,
            oplog_operation["insert_oplog_one"]["id"]
        )

    except TimeoutError:
        print("TimeoutError")
    except TransportQueryError as e:
        print("TransportQueryError" + str(e))
    except GraphQLError as e:
        print("GraphQLError: " + str(e))

def load_credential_configs(config):
    """
    load_credential_configs loads Ghostwriter credentials from a 'credentials' JSON object.

    This JSON object must have the following properties:

    gw_url - the link to Ghostwriter
    gw_password - the password for the ghostwriter account
    gw_username - the username for the ghostwriter account

    @param config - the JSON object to read configurations from
    @return Credential - a credential struct containing the credential information
    """
    CREDENTIALS = "credentials"
    GHOSTWRITER_URL = "gw_url"
    GHOSTWRITER_PASS = "gw_password"
    GHOSTWRITER_USER = "gw_username"

    return Credential(
        config[CREDENTIALS][GHOSTWRITER_URL],
        config[CREDENTIALS][GHOSTWRITER_PASS],
        config[CREDENTIALS][GHOSTWRITER_USER]
    )

# Function definitions
def get_logon_token(credentials):
    """
    get_logon_token obtains an authentication token from ghostwriter
    
    # @param credentials an object containing the ghostwriter URL, username, and password
    # @return the ghostwriter authentication token
    """

    # Prepare our initial unauthenticated GraphQL client
    transport = AIOHTTPTransport(credentials.url)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Define our gql query
    get_logon_token_query = gql(
        """
        mutation login_mutation($password: String!, $username: String!) {
            login(password: $password, username: $username) {
                token expires
            }
        }
        """
    )
    get_logon_token_query_params = {
        "password": credentials.password,
        "username": credentials.username
    }

    # Login and get our token
    login_result = client.execute(
        get_logon_token_query,
        variable_values=get_logon_token_query_params
    )
    return login_result["login"]["token"]

def create_sample_client(gql_client):
    """
    create_sample_project issues Ghostwriter GraphQL API requests
    to generate a sample client: 'SpecterPops'

    @param gql_client - the GraphQL API client to use when issuing API requests
    @return result - the ID of the new 'SpecterPops' client
    """

    CLIENT_NAME = "SpecterPops"
    CLIENT_CODENAME = "SAMPLE CLIENT"
    TIMEZONE = "America/Los_Angeles"

    # Define our gql query
    sample_client = gql(
        """
        mutation create_sample_client(
            $client_name: String!,
            $code_name: String!,
            $timezone: String!
        ) {
            insert_client_one(
                object: {
                    name: $client_name, 
                    codename: $code_name, 
                    timezone: $timezone
                }
            ) {
                id
            }
        }
        """
    )

    create_sample_client_param = {
        "client_name": CLIENT_NAME,
        "code_name": CLIENT_CODENAME,
        "timezone": TIMEZONE
    }

    result = gql_client.execute(sample_client, variable_values=create_sample_client_param)
    return result

def create_sample_project(gql_client, client_id):
    """
    create_sample_project issues Ghostwriter GraphQL API requests
    to generate a sample project: 'SAMPLE PROJECT'

    @param gql_client - the GraphQL API client to use when issuing API requests
    @param client_id - the ID of the owner client of the sample project
    @return result - the ID of the new 'SAMPLE PROJECT' project
    """

    SAMPLE_PROJECT_CODENAME = "SAMPLE PROJECT"
    START_DATE = "2024-04-23"
    END_DATE = "2025-04-23"

    sample_project = gql(
        """
        mutation create_sample_project(
            $client_id: bigint!, 
            $code_name: String!,
            $start_date: date!, 
            $end_date: date!
        ) {
            insert_project_one(
                object: {
                    clientId: $client_id,
                    codename: $code_name,
                    startDate: $start_date,
                    endDate: $end_date,
                    projectTypeId: "1"
                }
            ) {
                id
            }
        }
        """
    )

    create_sample_project_param = {
        "client_id": client_id,
        "code_name": SAMPLE_PROJECT_CODENAME,
        "start_date": START_DATE,
        "end_date": END_DATE
    }

    result = gql_client.execute(sample_project, variable_values=create_sample_project_param)
    return result

def create_sample_oplog(gql_client, project_id):
    """
    create_sample_oplog issues Ghostwriter GraphQL API requests
    to generate a sample oplog: 'SpecterPops Sample Oplog'

    @param gql_client - the GraphQL API client to use when issuing API requests
    @param project_id - the ID of the owner project of the sample oplog
    @return result - the ID of the new 'SpecterPops Sample Oplog' oplog
    """

    SAMPLE_OPLOG_NAME = "SpecterPops Sample Oplog"

    sample_oplog = gql(
        """
        mutation create_sample_oplog(
            $project_id: bigint!, 
            $name: String!
        ) {
            insert_oplog_one(
                object: {
                    projectId: $project_id,
                    name: $name
                }
            ) {
                id
            }
        }
        """
    )

    create_sample_oplog_param = {
        "project_id": project_id,
        "name": SAMPLE_OPLOG_NAME
    }

    result = gql_client.execute(sample_oplog, variable_values=create_sample_oplog_param)
    return result

def populate_oplog(gql_client, oplog_id):
    """
    populate_oplog issues Ghostwriter GraphQL API requests
    to fill an oplog with entries. This function attempts to read these entries
    from 'config/oplog.csv'. If this file does not exist, this function calls 
    oplog_generator to try to generate randomized 5000 entries.

    @param gql_client - the GraphQL API client to use when issuing API requests
    @param oplog_id - the ID of the oplog the function populates
    @return result - the IDs of the new oplog entries 
    """

    CSV_FILE_NAME = "config/oplog.csv"
    NUM_ENTRIES = 5000
    csv_path = Path(__file__).parent / CSV_FILE_NAME
    csv_file = None
    ghostwriter_csv = None
    try:
        csv_file = csv_path.open()
        ghostwriter_csv = csv.DictReader(csv_file)
    except FileNotFoundError:
        print("Oplog Not Found: Generating an oplog")

        # Generate NUM_ENTRIES entries
        oplog_generator.generate_oplog(CSV_FILE_NAME, NUM_ENTRIES)

        # Open the CSV containing the newly generated entries
        csv_file = csv_path.open()
        ghostwriter_csv = csv.DictReader(csv_file)

    gql_prefix = (
        """
        mutation populate_oplog {
            insert_oplogEntry(
                objects: ["""
    )

    gql_postfix = (
        """
                ]
            ) {
                returning {
                    id
                }
            }
        }
        """
    )

    index = 0

    # For every entry, validate the entry, and append to the GQL query
    for oplog_entry in ghostwriter_csv:
        oplog_entry = validate_oplog_entry(oplog_entry)
        append_string = (
            f'\n{{'
            f'oplog: "{oplog_id}", '
            f'startDate: "{oplog_entry["start_date"]}", '
            f'endDate: "{oplog_entry["end_date"]}", '
            f'sourceIp: "{oplog_entry["source_ip"]}", '
            f'destIp: "{oplog_entry["dest_ip"]}", '
            f'tool: "{oplog_entry["tool"]}", '
            f'userContext: "{oplog_entry["user_context"]}", '
            f'command: "{oplog_entry["command"]}", '
            f'description: "{oplog_entry["description"]}", '
            f'comments: "{oplog_entry["comments"]}", '
            f'operatorName: "{oplog_entry["operator_name"]}"'
            f'}},'
        )
        index = index + 1
        gql_prefix += append_string

    # Removes the externeous ','
    gql_prefix = gql_prefix[:-1]

    # Concatenate prefix and postfix for the full GQL query
    gql_query = gql_prefix + gql_postfix

    result = gql_client.execute(gql(gql_query))

    csv_file.close()

    return result


def read_json_config():
    """
    read_json_config reads from a JSON file 'config/config.json' and returns a JSON object

    @return configs - a JSON object representation of the file
    """
    # Define JSON config name constants
    CONFIG_FILE_NAME = "config/config.json"

    configs = None

    config_path = Path(__file__).parent / CONFIG_FILE_NAME
    with config_path.open() as config_file:
        configs = json.load(config_file)

    if not configs:
        raise JSONFileError("Could not read JSON config file")

    return configs

def validate_oplog_entry(dictionary):
    """
    validate_oplog_entry takes a dictionary, and performs 
    input validation on every value in the dictionary

    @param dictionary - the input dictionary
    @return dictionary - a validated dictionary
    """
    validation_dict = {"\\": "\\\\","\"": "\\\""}
    for key in dictionary:
        validated_string = dictionary[key]
        for k,v in validation_dict.items():
            validated_string = validated_string.replace(k, v)
        dictionary[key] = validated_string
    return dictionary

if __name__ == "__main__":
    main()
