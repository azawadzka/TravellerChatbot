DESTINATION_PROMPT = """
Return JSON having one field "destination" containing name of the last travel destination that the user asked about in the context. If you don't know, fill the field with the word "unknown".
Context: {context}
"""