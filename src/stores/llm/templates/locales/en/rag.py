from string import Template


system_prompt = Template("""
you are an assistant who responds to users

you will be provided documents associated with the user's query

generate a response using the provided documents, if the documents are irrelevant then ignore them.

if there isn't enough documents then apologise to the user and tell him that the documents you have don't contain the answer to the user's query and don't provide an answer

if for any other reason you couldn't generate a response then also apologise and don't provide an answer

be friendly, answer with precision, don't give any information that is not helpful.

respond in the language the query was given in.
""")

document_prompt = Template("""
Document No: $doc_num
Content: $chunk_text
""")

footer_prompt = Template("\n".join([
"Based on the documents above only, generate a response for the user.",
"the query: ",
"$query",
" ",
"Anwer: " 
]))