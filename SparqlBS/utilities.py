from SPARQLWrapper import *


def convert_json_format_into_list(results):
    """
    Given a dictionary containing the results of a SPARQL query in JSON format, it creates a list of lists in which
    the first element is a list containing the variables used in the query, and the rest of the elements
    are lists representing each "row" of the query results.

    :param results: A dictionary representing a JSON object.
    :return: A list of lists containing the variables and the query results.
    """
    variables = results["head"]["vars"]
    query_rows = [[row[v]["value"] for v in variables] for row in results["results"]["bindings"]]
    query_rows.insert(0, variables)
    return query_rows


def extract_fragment_from_uri(uri):
    """
    Given an URI, this function extracts its fragment, considering the fragment as the part of the URI
    which goes after the '#' symbol.

    :param uri: A string containing the URI.
    :return: A sting containing the fragment of the given URI.
    """
    return uri.split('#')[-1]


def select_pathway(sparql, pathway_search):
    """
    It retrieves all the pathways which names contain a given keyword (search word).

    :param sparql: SPARQLWrapper object using the ebi endpoint.
    :param pathway_search: The keyword or search word.
    :return: The query results in JSON format.
    """

    query_pathways = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        PREFIX biopax3: <http://www.biopax.org/release/biopax-level3.owl#>
        SELECT DISTINCT ?pathway ?pathway_name ?org_name
        FROM <http://rdf.ebi.ac.uk/dataset/reactome>
        WHERE
        {
           ?pathway rdf:type biopax3:Pathway .
           ?pathway biopax3:displayName ?pathway_name
           FILTER regex(?pathway_name, '""" + pathway_search + """', "i")
           ?pathway biopax3:organism ?org .
           ?org biopax3:name ?org_name
        }
        ORDER BY ?pathway_name ?org_name
        LIMIT 100
        """

    sparql.setQuery(query_pathways)
    sparql.setReturnFormat(JSON)
    return sparql.queryAndConvert()


def select_reaction(sparql, pathway_uri):
    """
    It retrieves all types of reactions (biochemical, degradation and template)
    of a given pathway.

    :param sparql: SPARQLWrapper object using the ebi endpoint.
    :param pathway_uri: The pathway identifier (URI)
    :return: The query result in JSON format.
    """

    query_reactions = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        PREFIX biopax3: <http://www.biopax.org/release/biopax-level3.owl#>
        SELECT DISTINCT *
        WHERE
        {<""" + pathway_uri + """> biopax3:pathwayComponent ?reaction .
        ?reaction biopax3:displayName ?reaction_name ;
                  rdf:type ?reaction_type
        VALUES ?reaction_type{biopax3:BiochemicalReaction biopax3:Degradation
                                    biopax3:TemplateReaction}
        OPTIONAL { ?reaction biopax3:conversionDirection ?direction }
        OPTIONAL { VALUES ?direction{"LEFT_TO_RIGHT"} }}
        """

    sparql.setQuery(query_reactions)
    sparql.setReturnFormat(JSON)
    return sparql.queryAndConvert()


def select_controller(sparql, reaction_uri):
    """
    It retrieves all non-protein type controllers of a given reaction.

    :param sparql: SPARQLWrapper object using the ebi endpoint.
    :param reaction_uri: The reaction URI identifier.
    :return: The query result in JSON format.
    """

    query_controllers = """
        PREFIX biopax3: <http://www.biopax.org/release/biopax-level3.owl#>

        SELECT DISTINCT ?controller ?controller_name ?controller_type ?control_type
        WHERE
          {
            ?control biopax3:controlled <""" + reaction_uri + """> ;
                     biopax3:controller ?controller ;
                     a ?control_type
            VALUES ?controller_type{biopax3:PhysicalEntity biopax3:Complex biopax3:Rna
                                    biopax3:SmallMolecule biopax3:Dna}
            ?controller a ?controller_type ;
                     biopax3:displayName ?controller_name
          }

          ORDER BY ?control_type
        """

    sparql.setQuery(query_controllers)
    sparql.setReturnFormat(JSON)
    return sparql.queryAndConvert()


def select_protein(sparql, reaction_uri):
    """
    It retrieves all protein type controllers of a given reaction.

    :param sparql: SPARQLWrapper object using the ebi endpoint.
    :param reaction_uri: The reaction URI identifier.
    :return: The query result in JSON format.
    """

    query_proteins = """
        PREFIX biopax3: <http://www.biopax.org/release/biopax-level3.owl#>

        SELECT DISTINCT ?protein_id ?protein_name ?controller_type ?control_type
        WHERE
          {
            VALUES ?controller_type{"Protein"}
            ?protein a biopax3:Protein .
            ?control biopax3:controlled <""" + reaction_uri + """> ;
                     biopax3:controller ?protein ;
                     a ?control_type .
            ?protein biopax3:displayName ?protein_name
            OPTIONAL {
              ?protein biopax3:entityReference ?protein_ref .
              ?protein_ref biopax3:xref ?protein_xref .
              ?protein_xref biopax3:id ?protein_id ;
                            biopax3:db ?protein_db .
              FILTER regex(?protein_db, "uniprot", "i")
            }
          }

          ORDER BY ?control_type
        """

    sparql.setQuery(query_proteins)
    sparql.setReturnFormat(JSON)
    return sparql.queryAndConvert()


def select_all_controller(sparql, reaction_uri):
    """
    It retrieves all types of controllers of a given reaction, both protein and non-protein types.
    If the controller is a Protein, controller_id contains either its Uniprot AC or its Reactome URI.
    If it is a non-Protein type, controller_id contains its Reactome URI.

    :param sparql: SPARQLWrapper object using the ebi endpoint.
    :param reaction_uri: The reaction URI identifier.
    :return: The query result in JSON format.
    """

    query_all_controllers = """
        PREFIX biopax3: <http://www.biopax.org/release/biopax-level3.owl#>

        SELECT DISTINCT ?controller_id ?controller_name ?controller_type ?control_type ?c_type
        WHERE
          {
            ?control biopax3:controlled <""" + reaction_uri + """> ;
                     a ?control_type ;
                     biopax3:controlType ?c_type ;
                     biopax3:controller ?controller .
            ?controller biopax3:displayName ?controller_name ;
                           a ?controller_type
            OPTIONAL {
              ?controller biopax3:entityReference ?protein_ref .
              ?protein_ref biopax3:xref ?protein_xref .
              ?protein_xref biopax3:id ?protein_ac ;
                            biopax3:db ?protein_db .
              FILTER regex(?protein_db, "uniprot", "i")
            }
            BIND (IF(BOUND(?protein_ac), ?protein_ac, ?controller) AS ?controller_id)
          }

        ORDER BY ?control_type ?controller_type
        """

    sparql.setQuery(query_all_controllers)
    sparql.setReturnFormat(JSON)
    return sparql.queryAndConvert()


def select_reactant_product(sparql, reaction_uri):
    """
    It retrieves all reactants and products of a given reaction. If the component is a Protein,
    component_id contains either its Uniprot AC or its Reactome URI. If it is a non-protein
    type, component_id contains its Reactome URI.

    :param sparql: SPARQLWrapper object using the ebi endpoint.
    :param reaction_uri: The reaction URI identifier.
    :return: The query result in JSON format.
    """

    query_react_prod = """
    PREFIX biopax3: <http://www.biopax.org/release/biopax-level3.owl#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT DISTINCT ?component_id ?component_name ?component_type ?composition_type
    WHERE
      {
        VALUES ?reaction{<""" + reaction_uri + """>}
        ?reaction ?c ?component .
        ?component a ?component_type ;
                   biopax3:displayName ?component_name
        {VALUES ?c{biopax3:left}
          VALUES ?composition_type{"Reactant"}}
        UNION { VALUES ?c{biopax3:right}
                VALUES ?composition_type{"Product"}}
        OPTIONAL {
          ?component biopax3:entityReference ?protein_ref .
          ?protein_ref biopax3:xref ?protein_xref .
          ?protein_xref biopax3:id ?protein_ac ;
                        biopax3:db ?protein_db .
          FILTER regex(?protein_db, "uniprot", "i")
        }
        BIND (IF(BOUND(?protein_ac), ?protein_ac, ?component) AS ?component_id)
      }
    """

    sparql.setQuery(query_react_prod)
    sparql.setReturnFormat(JSON)
    return sparql.queryAndConvert()


def select_controller_info(sparql, controller_uri):
    """
    It retrieves some information about a controller given its URI.

    :param sparql: SPARQLWrapper object using the ebi endpoint.
    :param controller_uri: The controller URI.
    :return: The query result in JSON format.
    """

    query_controller_info = """
        PREFIX biopax3: <http://www.biopax.org/release/biopax-level3.owl#>

        SELECT DISTINCT ?controller_name ?cell_term
        WHERE
          {
            <""" + controller_uri + """> biopax3:displayName ?controller_name ;
                     biopax3:cellularLocation ?cell_vocabulary .
            ?cell_vocabulary biopax3:term ?cell_term
          }
        """

    sparql.setQuery(query_controller_info)
    sparql.setReturnFormat(JSON)
    return sparql.queryAndConvert()


def select_uniprot(sparql, uniprot_id):
    """
    It retrieves some information about a protein stored in Uniprot given its accession number.

    :param sparql: SPARQLWrapper object using the Uniprot endpoint.
    :param uniprot_id: The Uniprot AC of the protein.
    :return: The query result in JSON format.
    """

    query_uniprot = """
        PREFIX up_core:<http://purl.uniprot.org/core/>
        PREFIX uniprot:<http://purl.uniprot.org/uniprot/>
        PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
        PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>

        SELECT DISTINCT ?protein_name ?gene_name
        WHERE
          {
            VALUES ?protein{uniprot:""" + uniprot_id + """}
            ?protein rdfs:label ?protein_name ;
                     up_core:encodedBy ?gene .
            ?gene skos:prefLabel ?gene_name
          }
        """

    sparql.setQuery(query_uniprot)
    sparql.setReturnFormat(JSON)
    return sparql.queryAndConvert()


def select_full_info(sparql, end_unip, component_id):
    """
    Using a federated query, it retrieves some information about a given component. If controller_id is an URI
    the information is retrieved form Reactome, and if it is an Uniprot accesion number the information is retrieved
    from Uniprot.

    :param sparql: SPARQLWrapper object using the ebi endpoint.
    :param end_unip: The URL of the Uniprot endpoint.
    :param component_id: The component identifier, either an URI or an Uniprot AC.
    :return: The query result in JSON format.
    """

    uniprot_id = extract_fragment_from_uri(component_id)

    query_full_info = """
        PREFIX biopax3: <http://www.biopax.org/release/biopax-level3.owl#>
        PREFIX up:<http://purl.uniprot.org/core/>
        PREFIX uniprot:<http://purl.uniprot.org/uniprot/>
        PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
        PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>

        SELECT DISTINCT ?data
        WHERE
          {
             {VALUES ?comp_id{<""" + component_id + """>}
             {?comp_id biopax3:displayName ?data}
             UNION {?comp_id biopax3:cellularLocation ?cell_vocabulary .
             ?cell_vocabulary biopax3:term ?data}}

             UNION { SERVICE <""" + end_unip + """> {
                VALUES ?prot{uniprot:""" + uniprot_id + """}
                {?prot rdfs:label ?data }
                UNION {?prot up:encodedBy ?gene .
                ?gene skos:prefLabel ?data}
                UNION {?prot up:sequence ?s
                FILTER regex(str(?s), "-1$", "i")
                ?s rdf:value ?data}
                UNION {?prot up:classifiedWith ?c .
                FILTER regex(?c, "GO_")
                ?c rdfs:label ?data}}}
          }
        """

    sparql.setQuery(query_full_info)
    sparql.setReturnFormat(JSON)
    return sparql.queryAndConvert()


def select_more_info(sparql, uri):
    """
    It retrieves all the comments, publications references and pathways either a pathway
    or reaction is a component of.

    :param sparql: SPARQLWrapper object using the ebi endpoint.
    :param uri: A pathway or a reaction URI.
    :return: The query result in JSON format.
    """

    query_more_info = """
    PREFIX biopax3: <http://www.biopax.org/release/biopax-level3.owl#>
    SELECT DISTINCT ?comment ?pathway_name ?org_name ?title ?source ?year
    WHERE
      {
        VALUES ?entity{<""" + uri + """>}
        { ?entity biopax3:comment ?comment }
        UNION { ?pathway biopax3:pathwayComponent ?entity ;
                         a biopax3:Pathway ;
                         biopax3:displayName ?pathway_name ;
                         biopax3:organism ?org .
               ?org biopax3:name ?org_name }
        UNION { ?entity biopax3:xref ?publi .
        ?publi a biopax3:PublicationXref ;
               biopax3:title ?title ;
               biopax3:source ?source ;
               biopax3:year ?year }
      }

    ORDER BY ?year
    """

    sparql.setQuery(query_more_info)
    sparql.setReturnFormat(JSON)
    return sparql.queryAndConvert()
