import json
import os
import time

from typing import Dict

class SearchResponseAnalyzer:
    """
    Class to process debugging info from elastic response into a more readable format
    """  
    @classmethod
    def extract_explain_info(cls, explain_section: Dict):
        """
        Recursively get upper levels of elasticsearch explaination result
        Skips formulas how engine calculates weight of each token in some field
        Args:
            explain_section: response['hits']['hits'][ind]['_explanation'] - elastic explain of a doc
        Returns: result as dict
        """
        result = {'description': explain_section['description'],
                    'value': explain_section['value']}
        if 'computed as' in explain_section['description']:
            return result
        result['details'] = []
        for detail in explain_section['details']:
            result['details'].append(cls.extract_explain_info(detail))
        return result

    @classmethod
    def pretty_explain(cls, fout, explain_json: Dict):
        """
        Make a text from json explanation
        Args:
            fout: opened file with write mode
            explain_json: result of extract_explain_info(...)
        Returns: -
        """
        def print_plan(explain_json: Dict, format_prefix: str):
            """
            Recursively print nodes information
            Args:
                format_prefix: indent at the beginning of a line
            """
            decription = explain_json['description']
            if len(decription) >= len('weight') and \
                 'weight' == decription[0: len('weight')]:
                field_name = decription[len('weight('): decription.find(':')]
                token = decription[decription.find(':') + 1: decription.find(' ')]
                fout.write(f'{format_prefix}{field_name}: "{token}"\twith score {explain_json["value"]}\n')
                return
            fout.write(f'{format_prefix}{explain_json["description"]}\twith value {explain_json["value"]}\n')
            format_prefix += '  '
            for detail in explain_json['details']:
                print_plan(detail, format_prefix)

        for doc in explain_json:
            fout.write(f'id: {doc["doc_id"]}, score: {doc["score"]}\n')
            print_plan(doc['explain'], '  ')


    @classmethod
    def explain_score(cls, es_result: Dict, user_request: str):
        """
        Print readable explanation from elastic about each chosen documents
        Args:
            es_result: response from elastic as dict
            user_request: initial user request
        Returns: -
        Files: create a new one in codesearch/es/explain_plans/ directory
               and write results of extract_explain_info(...) and pretty_explain(...) in it
        """
        explain_json = []
        for doc in es_result['hits']['hits']:
            doc_json = dict()
            doc_json['doc_id'] = doc['_id']
            doc_json['score'] = doc['_score']
            doc_json['explain'] = cls.extract_explain_info(doc['_explanation'])
            explain_json.append(doc_json)
        output_filename = f'{os.path.dirname(__file__)}/explain_plans/{time.strftime("%Y-%m-%d_%H-%M-%S")}.log'
        with open(output_filename, 'w', encoding='utf-8') as fout:
            fout.write(user_request + '\n')
            cls.pretty_explain(fout, explain_json)
            json.dump(explain_json, fout)


    @classmethod
    def explain_time(cls, es_result: Dict):
        pass
