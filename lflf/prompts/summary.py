summary_prompt = """
                Now based on the previous response, summarize what is the final action choice. 
                Return the answer as a JSON object, with a single key 'action', and a single value which is a number. 
                Do not return any other string besides the json object. For example, if the action is 7, return {'action': 7}
                If the text have multiple results for the correct action, you must only return one of them. Do not return multiple answers!
                """

summary_correction = """
                    This is incorrect format. You should return the answer as single JSON object, with a single key 'action', and the value should be a single number! 
                    If the text have multiple results for the correct action, you must only return one of them. Do not return multiple answers! Please try again.
                    """

summary_prompt_return_action = """
                Now based on the previous response, summarize what is the final action choice. 
                Return the answer as a JSON object, with a single key 'action', and a single list. The value of JSON object must be a list of 7 numbers.
                Do not return any other string besides the json object. 
                For example, if the action is [0,0,20,0,0,-30,100], return {'action': [0, 0, 20, 0, 0, -30, 100]}.
                If the action is [0,0,20,0,0,-30,100], return {'action': [0, 0, 20, 0, 0, -30, 100]}.
                If the action is [0,20,20,0,0,0,-100], return {'action': [0, 20, 20, 0, 0, 0, -100]}.
                If the action is [-20 20 0 0 0 20 100], return {'action': [-20, 20, 0, 0, 0, 20, 100]}.
                If the action is [0,-20,0,0,0,0,100], return {'action': [0, -20, 0, 0, 0, 0, 100]}.
                If the action is [20,0,0,0,0,0,-100], return {'action': [20, 0, 0, 0, 0, 0, -100]}.
                If the action is 0 0 0 0 0 -20 -100, return {'action': [0, 0, 0, 0, 0, -20, -100]}.
                If the action is [14 20 0 0 5 0 -100], return {'action': [14, 20, 0, 0, 5, 0, -100]}.
                If the action is -1 0 2 -40 30 1 100, return {'action': [-1, 0, 2, -40, 30, 1, 100]}
                """

summary_correction_return_action = """
                    This is incorrect format. You should return the answer as single JSON object, with a single key 'action', and the value should be a single list! Please try again.
                    """
