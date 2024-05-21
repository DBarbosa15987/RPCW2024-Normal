# Ex11

Quantas doenças estão presentes na ontologia?

PREFIX : <http://www.example.org/disease-ontology#>

select (count (?d) as ?count) where {
    ?d a :Disease .
}


Que doenças estão associadas ao sintoma "yellowish_skin"?

PREFIX : <http://www.example.org/disease-ontology#>

select ?d where {
    ?d a :Disease .
    ?d :hasSymptom :yellowish_skin.
}

Que doenças estão associadas ao tratamento "exercise"?

PREFIX : <http://www.example.org/disease-ontology#>

select ?d where {
    ?d a :Disease .
    ?d :hasTreatment :exercise.
}

Produz uma lista ordenada alfabeticamente com o nome dos doentes.


PREFIX : <http://www.example.org/disease-ontology#>

select ?name where {
    ?p a :Patient .
    ?p :name ?name.
}order by ?name


# Ex12

PREFIX : <http://www.example.org/disease-ontology#>

construct {
    ?patientX :hasDisease ?diseaseY.
}
where {
    ?diseaseY :hasSymptom ?symp.
    ?patientX :exhibitsSymptom ?symp.

    {
        select ?patientX ?diseaseY (count(?symp) as ?count1)
        where {
            ?diseaseY :hasSymptom ?symp.
        }
        group by ?patientX ?diseaseY
    }
    {
        select ?patientX ?diseaseY (count(?symp) as ?count2)
        where {
            ?diseaseY :hasSymptom ?symp.
            ?patientX :exhibitsSymptom ?symp.
        }
        group by ?patientX ?diseaseY
    }
    FILTER(?count1 = ?count2)
}


# Ex13

PREFIX : <http://www.example.org/disease-ontology#>

select ?doenca (count(?p) as ?nDoentes) where {
    ?p a :Patient .
    ?p :hasDisease ?doenca.
}group by ?doenca

# Ex14

PREFIX : <http://www.example.org/disease-ontology#>

select ?sintoma  (count(?d) as ?nDoencas) where {
    ?sintoma a :Symptom .
    ?d :hasSymptom ?sintoma.
    
}group by ?sintoma

# Ex15

PREFIX : <http://www.example.org/disease-ontology#>

select ?tratamento  (count(?d) as ?nDoencas) where {
    ?tratamento a :Treatment .
    ?d :hasTreatment ?tratamento.
    
}group by ?tratamento