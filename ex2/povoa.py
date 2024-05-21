from rdflib import Namespace,URIRef,Graph,Literal
from rdflib.namespace import RDF,OWL,XSD
import json
import csv

g = Graph()
g.parse("medical.ttl")

ns = Namespace("http://www.example.org/disease-ontology#")

def processSyntoms():
    f = open("Disease_Syntoms.csv",'r')
    csvreader = csv.reader(f)

    next(csvreader)
    dicDisease = {}
    diseaseSet = set()
    symptomsSet = set()
    i = 0

    for row in csvreader:

        disease = row[0].strip()
        symptoms = [symptom.strip() for symptom in row[1:] if symptom.strip()]

        diseaseUri = URIRef(f'{ns}{disease.replace(" ","_")}')
        if disease not in diseaseSet:
            g.add((diseaseUri, RDF.type, OWL.NamedIndividual))
            g.add((diseaseUri, RDF.type, ns.Disease))
            diseaseSet.add(disease)

        for symp in symptoms:

            sympUri = URIRef(f'{ns}{symp.replace(" ","_")}')
            if symp not in symptomsSet:
                g.add((sympUri, RDF.type, OWL.NamedIndividual))
                g.add((sympUri, RDF.type, ns.Symptom))
                symptomsSet.add(symp)

            if disease in dicDisease:
                if symp not in dicDisease[disease]:
                    g.add((diseaseUri,ns.hasSymptom,sympUri))
                dicDisease[disease].add(symp)
            else:
                g.add((diseaseUri,ns.hasSymptom,sympUri))
                dicDisease[disease] = set([symp])

        i+=1

    f.close()

def processDescriptions():
    f = open("Disease_Description.csv",'r')
    csvreader = csv.reader(f)

    next(csvreader)

    for row in csvreader:

        disease = row[0]
        description = row[1]
        diseaseUri = URIRef(f'{ns}{disease.replace(" ","_")}')

        g.add((diseaseUri,ns.description,Literal(description)))


    f.close()


def processTreatment():

    f = open("Disease_Treatment.csv",'r')
    csvreader = csv.reader(f)

    next(csvreader)

    treatmentSet = set()
    dicDisease = {}

    for row in csvreader:

        disease = row[0]
        treatments = row[1:]
        diseaseUri = URIRef(f'{ns}{disease.replace(" ","_")}')
        
        for treat in treatments:
            
            treatUri = URIRef(f'{ns}{treat.replace(" ","_")}')
            if treat not in treatmentSet:
                treatmentSet.add(treat)
                g.add((treatUri, RDF.type, OWL.NamedIndividual))
                g.add((treatUri, RDF.type, ns.Treatment))

            if disease in dicDisease:
                if treat not in dicDisease[disease]:
                    g.add((diseaseUri,ns.hasTreatment,treatUri))
                dicDisease[disease].add(treat)
            else:
                g.add((diseaseUri,ns.hasTreatment,treatUri))
                dicDisease[disease] = set([treat])


    f.close()


def processDoentes():
    
    with open("pg50326.json",'r') as f:
            data = json.load(f)

    doentes = data

    i=0
    for doente in doentes:
        nome = doente["nome"]
        sintomas = doente["sintomas"]

        doenteUri = URIRef(f"{ns}doente_{i}")
        g.add((doenteUri, RDF.type, OWL.NamedIndividual))
        g.add((doenteUri, RDF.type, ns.Patient))
        g.add((doenteUri, ns.name, Literal(nome)))
        for sintoma in sintomas:
            sympUri = URIRef(f'{ns}{sintoma.replace(" ","_")}')
            g.add((doenteUri, ns.exhibitsSymptom, sympUri))
            
        i+=1



# def processAlunos():

#     with open("aval-alunos.json",'r') as f:
#         data = json.load(f)
    
#     alunosList = data["alunos"]
#     alunosSet = set()

#     for aluno in alunosList:

#         id = aluno.get("idAluno")
#         if id not in alunosSet:    
#             nome = aluno.get("nome")
#             curso = aluno.get("curso")
#             notaProjeto = aluno.get("projeto")
#             tpcs = aluno.get("tpc") #lista
#             exames = aluno.get("exames")

#             # Alunos
#             alunoUri = URIRef(f"{ns}{id}")
#             g.add((alunoUri, RDF.type, OWL.NamedIndividual))
#             g.add((alunoUri, RDF.type, ns.Aluno))
#             g.add((alunoUri, ns.idAluno, Literal(id)))

#             if nome:
#                 g.add((alunoUri, ns.nome, Literal(nome)))
#             if curso:
#                 g.add((alunoUri, ns.curso, Literal(curso)))
#             if notaProjeto:
#                 project_id = URIRef(f"projeto_{id}")
#                 g.add((project_id, RDF.type, OWL.NamedIndividual))
#                 g.add((project_id, RDF.type, ns.Projeto))
#                 g.add((project_id, ns.notaProjeto, Literal(notaProjeto,datatype=XSD.int)))

#                 g.add((alunoUri,ns.tem_projeto,project_id))
#             if tpcs:
                
#                 for tpc in tpcs:
#                     tp = tpc["tp"]
#                     nota = tpc["nota"]
#                     tpc_id = URIRef(f"tpc_{id}_{tp}")
#                     g.add((tpc_id, RDF.type, OWL.NamedIndividual))
#                     g.add((tpc_id, RDF.type, ns.TPC))

#                     g.add((tpc_id, ns.tp,Literal(tp)))
#                     g.add((tpc_id, ns.notaTPC,Literal(nota,datatype=XSD.float)))

#                     g.add ((alunoUri,ns.tem_tpc,tpc_id))
                
#             if exames:

#                 examesList = exames.items() # list((epoca,nota))

#                 for epoca,nota in examesList:
#                     exameId = URIRef(f"exame_{id}_{epoca}")
#                     g.add((exameId, RDF.type, OWL.NamedIndividual))
#                     g.add((exameId, RDF.type, ns.Exame))

#                     g.add((exameId, ns.epoca, Literal(epoca)))
#                     g.add((exameId, ns.notaExame,Literal(nota,datatype=XSD.int)))

#                     g.add((alunoUri,ns.tem_exame,exameId))
#             alunosSet.add(id)

#         else:
#             print(id)

#     print(len(alunosSet))



processSyntoms()
processDescriptions()
g.serialize(format="ttl",destination="med_doencas.ttl")
processTreatment()
g.serialize(format="ttl",destination="med_tratamentos.ttl")
processDoentes()
g.serialize(format="ttl",destination="med_doentes.ttl")
