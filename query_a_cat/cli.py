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
@click.argument('query', default="")
@click.option('--result-type', type=click.Choice(['hits', 'uids', 'summary', 'full']))
@click.option('--limit', type=int, default=-1, help="limit number of returned records")
@click.option('--verbose/--no-verbose', default=False, help="print urls of HTTP requests")
def csw_query_command(csw_endpoint, query, result_type, limit, verbose):
    """Query CSW, output results in JSON to stdout
    """
    csw_client = query_a_cat.util.csw_client.CSWClient(csw_endpoint, verbose)
    if not result_type == "hits":
        records = csw_client.csw_query(query, result_type, limit)
        print(json.dumps(records, indent=4))
    else:
        result = csw_client.get_hits(query)
        print(json.dumps(result))

@cli.command(name="csw-download")
@click.argument('csw-endpoint')
@click.argument('dest-dir')
@click.argument('query', default="")
@click.option('--limit', type=int, default=-1, help="limit number of returned records")
@click.option('--verbose/--no-verbose', default=False, help="print urls of HTTP requests")

def csw_query_download_command(csw_endpoint, dest_dir, query, limit, verbose):
    """Query CSW, download results
    """
    csw_client = query_a_cat.util.csw_client.CSWClient(csw_endpoint, verbose)
    records = csw_client.csw_query(query, "download", limit, dest_dir)
    nr_records = len(records)
    print(f"downloaded {nr_records} record(s) in {dest_dir}")

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()
