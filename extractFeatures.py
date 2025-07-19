import openai
import os
import json

def extractConcepts(transcript, model):    
    print("Extracting document concepts")
    response = openai.ChatCompletion.create(
        model=model,
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": """You are a literary genius who is well versed at identifying the themes and ideas in any piece of text. 
                                            You are very professional and will only respond in JSON format. 
                                            Your job is to identify the ideas in the text presented to you and provide a representitive name and high level description of the idea
                                            If there is more than one idea, then return all the ideas in seperate JSON segments.
                                            The return format is {"scanned_text_name" : $TEXT_NAME, 
                                                                  "knowledge" = [
                                                                    {"idea": $INSERT_IDEA, "description": $INSERT_DESCRIPTION, "node_id": $NODE_ID},
                                                                    {"idea": $INSERT_IDEA, "description": $INSERT_DESCRIPTION, "node_id": $NODE_ID},
                                                                    {"idea": $INSERT_IDEA, "description": $INSERT_DESCRIPTION, "node_id": $NODE_ID},
                                                                    ...
                                                                    ],
                                                                  "connections" = [
                                                                    {"source_node" = $NODE_ID_SOURCE, "destination_node" = $NODE_ID_DESTINATION, "connection_type" = $CONNECTION_TYPE}
                                                                  ]
                                                                }
                                            Your task is to populate $TEXT_NAME and as many instances of $INSERT_IDEA and $INSERT_DESCRIPTION as you find in the text.
                                            You then need to map the connections between the nodes by filling out the $NODE_ID_SOURCE and NODE_ID_DESTINATION and assigning the kind of relationship in $CONNECTION_TYPE
                                            The NODE_ID_SOURCE and NODE_ID_DESTINATION should strictly be integers
                                            I want you to focus on having as many connection as possible, and make them descriptive e.g., "supports the argument", "was argued by", "is a form of" etc.
                                            """},
            {"role": "user", "content": transcript}
        ]
    )
    content = response['choices'][0]['message']['content']
    content_dict = json.loads(content)
    return(content_dict)


def extractGlossary(text, model):    
    print("Extracting document glossary")
    response = openai.ChatCompletion.create(
        model=model,
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": """You are a literary genius who is well versed at identifying the themes and ideas in any piece of text. 
                                            You are very professional and will only respond in JSON format. 
                                            Your job is to identify all the key words and build a glossary of them
                                            The return format is {"scanned_text_name" : $TEXT_NAME, 
                                                                  "glossary" = [
                                                                    {"term": $INSERT_TERM, "definition": $INSERT_DEFINITION},
                                                                    {"term": $INSERT_TERM, "definition": $INSERT_DEFINITION},
                                                                    {"term": $INSERT_TERM, "definition": $INSERT_DEFINITION},
                                                                    ...
                                                                    ]}
                                                                 
              
                                            Your task is to populate $INSERT_TERM with the terms you find in the text and $INSERT_DEFINITION based on your understanding of their use
                                            I want you to insert any term that is not in common usage and may confuse the reader.
                                            """},
            {"role": "user", "content": text}
        ]
    )
    content = response['choices'][0]['message']['content']
    content_dict = json.loads(content)
    return(content_dict)