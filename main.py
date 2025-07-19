import os
import extractFeatures as ef
import openai
from py2neo import Graph, Node, Relationship
from dotenv import dotenv_values
import configparser
import pdfExtractor as pdf

config = configparser.ConfigParser()
config.read('config.ini')
secrets = dotenv_values(".env")

openai.api_key = secrets["OPENAI_API_KEY"]
GPTModel = config.get('OpenAI', 'gpt_model')

graph = Graph(secrets["NEO4J_SERVER"], 
              auth=(secrets["NEO4J_USERNAME"], 
                    secrets["NEO4J_PASSWORD"]))

source_file = "coady_fake_news"

source = pdf.extract_text_from_pdf("coady_fake_news.pdf")

print(len(source))

response = ef.extractConcepts(source, GPTModel)
graph.delete_all()

print("writing nodes to graph")

KnowledgeNodes = []

for index in response["knowledge"]:

    node = Node("Ideas", idea = index["idea"], description = index["description"], node_id = index["node_id"], source=source_file) 
    KnowledgeNodes.append(node)

for i in KnowledgeNodes:
    graph.create(i)

print("writing connections to graph")
ConnectionNodes = []

for index in response["connections"]:
    KnowledgeNodeSourceIndex = int(index["source_node"])-1
    KnowledgeNodeDestinationIndex = int(index["destination_node"])-1
    graph.create(Relationship(KnowledgeNodes[KnowledgeNodeSourceIndex], 
                              index["connection_type"],
                              KnowledgeNodes[KnowledgeNodeDestinationIndex],
                              source=source_file))
    
glossary = ef.extractGlossary(source, GPTModel)

print("writing glossary to graph")
glossaryNodes = []
for index in glossary["glossary"]:
    node = Node("Definition", term = index["term"], definition = index["definition"], source=source_file) 
    glossaryNodes.append(node)

for i in glossaryNodes:
    graph.create(i)  

print("Done ;)")