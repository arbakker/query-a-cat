""" main entry file query-a-cat application
"""
import json
import click
import query_a_cat.util.csw_client

@click.group()
def cli():
    """empty function for click group commands
    """
    pass

@cli.command(name="csw")
@click.argument('csw-endpoint')
@click.argument('query')
@click.option('--result-type', type=click.Choice(['hits', 'uids', 'summary', 'full']))
@click.option('--limit', type=int, default=-1)
def csw_query_command(csw_endpoint, query, result_type, limit):
    """Query CSW
    """
    csw_client = query_a_cat.util.csw_client.CSWClient(csw_endpoint)
    if not result_type == "hits":
        records = csw_client.get_records_filter(query, result_type, limit)
        print(json.dumps(records, indent=4))
    else:
        result = csw_client.get_hits(query)
        print(json.dumps(result))

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()
