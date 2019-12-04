"""[summary]

Raises:
    Exception: [description]

Returns:
    [type] -- [description]
"""

import os
import sys
import base64
import urllib.parse
import requests
from lxml import etree

class CSWClient:
    def __init__(self, url, verbose):
        self.username = ""
        self.password = ""
        self.url = url
        self.ns = {"csw":"http://www.opengis.net/cat/csw/2.0.2",
        "gmd":"http://www.isotc211.org/2005/gmd", "dc":"http://purl.org/dc/elements/1.1/", "dct":"http://purl.org/dc/terms/"}
        self.session = requests.Session()
        self.url_template = "{0}?request=GetRecords&Service=CSW&Version=2.0.2&typeNames=gmd:MD_Metadata&resultType={1}{2}{3}"
        self.query_template = "&constraint={0}&constraintLanguage=CQL_TEXT&constraint_language_version=1.1.0"
        self.start_pos_template = "&startPosition={0}"
        self.load_csw_credentials()
        self.verbose = verbose

    def load_csw_credentials(self):
        if 'CSW_USERNAME' in os.environ:
            self.username = os.environ['CSW_USERNAME']
        if 'CSW_PASSWORD' in os.environ:
            self.password = os.environ['CSW_PASSWORD']

    def get_record_url(self, record_id):
        get_record_url = "{0}?request=GetRecordById&service=CSW&version=2.0.2&elementSetName=full&outputFormat=application/xml&outputSchema=http://www.isotc211.org/2005/gmd&id={1}".format(self.url, record_id)
        return get_record_url

    def get_record(self, record_id):
        get_record_url = self.get_record_url(record_id)
        response = self.get_request(get_record_url)
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        root = etree.fromstring(response.content, parser=parser)
        xml_md = root.xpath('.//gmd:MD_Metadata', namespaces=self.ns)
        if xml_md:
            xml_md = xml_md[0]
        else:
            return ""
        xml_md_str = etree.tostring(xml_md, pretty_print=True)
        return xml_md_str

    def csw_query(self, query, result_type, limit, dest_dir=None):
        index = 1
        results = []
        if query:
            query_quoted = urllib.parse.quote(query)
        while True:
            if limit != -1 and index >= limit:
                break
            query_string = ""
            if query:
                query_string = self.query_template.format(query_quoted)
            start_pos = self.start_pos_template.format(index)
            url = self.url_template.format(self.url, "results", start_pos, query_string)
            response = self.get_request(url)
            if response.status_code != 200:
                break
            search_result = self.get_search_result(response.content)
            nr_records = self.get_number_records(search_result, 'numberOfRecordsReturned')
            if result_type in ["uids", "full", "download"]:
                query_results = self.get_md_identifiers(response.content)
            else:
                query_results = self.get_md_fields(response.content)
            results.extend(query_results)
            if nr_records < 10:
                break
            index += 10
        if result_type == "full":
            return self.get_xml_records(results)
        if result_type == "download":
            self.get_xml_records_download(results, dest_dir)
        return results

    def get_xml_records_download(self, uids, dest_dir):
        for uid in uids:
            xml_md_str = self.get_record(uid)
            dest_path = os.path.join(dest_dir, f"{uid}.xml")
            with open(dest_path, 'w') as md_file:
                md_file.write(xml_md_str.decode("utf-8"))

    def get_xml_records(self, uids):
        results = []
        for uid in uids:
            xml_md_str = self.get_record(uid)
            xml_md_base64 = base64.b64encode(xml_md_str).decode('ascii')
            result = {}
            result["uid"] = uid
            result["md_record"] = xml_md_base64
            result["encoding"] = "base64"
            results.append(result)
        return results

    def get_request(self, url):
        try:
            if self.verbose:
                print(url)
            if not self.password or not self.username:
                response = self.session.get(url)
            else:
                response = self.session.get(url, auth=requests.auth.HTTPBasicAuth(
                    self.username, self.password))
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
            sys.exit(1)
        return response

    def get_hits(self, query):
        query_string = ""
        if query:
            query_quoted = urllib.parse.quote(query)
            query_string = self.query_template.format(query_quoted)
        url = self.url_template.format(self.url, "hits", query_string, "")
        response = self.get_request(url)
        search_result = self.get_search_result(response.content)
        nr_records = self.get_number_records(search_result, 'numberOfRecordsMatched')
        result = {}
        result["numberOfRecordsMatched"] = nr_records
        return result

    def get_search_result(self, xml):
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        root = etree.fromstring(xml, parser=parser)
        search_result = root.xpath('.//csw:SearchResults', namespaces=self.ns)
        if search_result:
            return search_result[0]
        else:
            return search_result

    def get_number_records(self, search_result, attribute):
        number_records = search_result.attrib[attribute]
        if number_records:
            return int(number_records)
        else:
            raise Exception("Could not find SearchResults@{0} in CSW GetRecords response".\
                format(attribute))

    def get_record_identifiers(self, xml):
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        root = etree.fromstring(xml, parser=parser)
        records = root.xpath('.//dc:identifier', namespaces=self.ns)
        result = [record.text for record in records]
        return result

    def get_md_identifiers(self, xml):
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        root = etree.fromstring(xml, parser=parser)
        search_result = root.xpath('.//csw:SummaryRecord', namespaces=self.ns)
        results = []
        for item in search_result:
            uuid = item.xpath('.//dc:identifier', namespaces=self.ns)
            uuid_string = uuid[0].text
            results.append(uuid_string)
        return results

    def get_md_fields(self, xml):
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        root = etree.fromstring(xml, parser=parser)
        search_result = root.xpath('.//csw:SummaryRecord', namespaces=self.ns)
        results = []
        for item in search_result:
            uuid = item.xpath('.//dc:identifier', namespaces=self.ns)
            uuid_string = uuid[0].text
            record = {}
            titel = item.xpath('.//dc:title', namespaces=self.ns)
            title_string = titel[0].text
            abstract = item.xpath('.//dct:abstract', namespaces=self.ns)
            abstract_string = abstract[0].text
            modified = item.xpath('.//dct:modified', namespaces=self.ns)
            # some records have unset modified field, WHY?!!!
            if modified: 
                modified_string = modified[0].text
                record["modified"] = modified_string
            md_type = item.xpath('.//dc:type', namespaces=self.ns)
            md_type_string = md_type[0].text
            keywords_xpath = item.xpath('.//dc:subject', namespaces=self.ns)
            keywords = []
            for keyword in keywords_xpath:
                keywords.append(keyword.text)
            record["identifier"] = uuid_string
            record["titel"] = title_string
            record["abstract"] = abstract_string
            record["md_type"] = md_type_string
            record["keywords"] = keywords
            results.append(record)
        return results
