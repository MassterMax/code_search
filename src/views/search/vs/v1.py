def transform(user_request):
    if user_request == "__all":
        return '''
            {
                "query": {
                    "match_all": { }
                }
            }
        '''
    return f'''
    {{
        "query": {{
            "match": {{
                "email": {{
                    "query": "{user_request}",
                    "fuzziness": 10
                }}
            }}
        }}
    }}
    '''