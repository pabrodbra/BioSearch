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


def print_list_results(results):
    """
    Given a list containing the results of a SPARQL query,
    it prints the variables used in the query and the query results.
    :param results: A list of lists containing the "rows" of a SPARQL query results.
    """
    print("Variables:", ', '.join(results[0]))
    for l in results[1:]:
        print('\t'.join(l))


def print_json_format(results):
    """
    Given a dictionary containing the results of a SPARQL query in JSON format,
    it prints the variables used in the query and the query results.
    :param results: A dictionary representing a JSON object.
    """
    variables = results["head"]["vars"]
    print("Variables:", ', '.join(variables))
    for result in results["results"]["bindings"]:
        for v in variables:
            print(result[v]["value"], end='\t')
        print()


def extract_uniprot_ac(results):
    """
    Given a list containing the results of a SPARQL query, it extracts the protein accession
    number (Uniprot database identifier) from the URIs in the results list that contain
    the Uniprot AC of a protein.

    :param results: A list of lists containing the "rows" of a SPARQL query results.
    :return: A list containing the extracted Uniprot ACs.
    """
    return [uri.split('/')[-1] for row in results[1:] for uri in row if 'uniprot' in uri]


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
    It retrieves all the pathways which names contain a given keyword (search word)

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
    It retrieves all biochemical reactions of a given pathway.

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
        ?reaction rdf:type biopax3:BiochemicalReaction ;
                  biopax3:displayName ?reaction_name ;
                  biopax3:conversionDirection ?direction}
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
                     a ?control_type
            OPTIONAL {?control biopax3:controlType ?c_type}

            {VALUES ?controller_type{biopax3:PhysicalEntity biopax3:Complex biopax3:Rna
                                    biopax3:SmallMolecule biopax3:Dna}
            ?control biopax3:controller ?controller_id .
            ?controller_id biopax3:displayName ?controller_name ;
                           a ?controller_type}

            UNION {VALUES ?controller_type{biopax3:Protein}
            ?control biopax3:controller ?protein .
            ?protein biopax3:displayName ?controller_name ;
                 a ?controller_type
            OPTIONAL {
              ?protein biopax3:entityReference ?protein_ref .
              ?protein_ref biopax3:xref ?protein_xref .
              ?protein_xref biopax3:id ?protein_ac ;
                            biopax3:db ?protein_db .
              FILTER regex(?protein_db, "uniprot", "i")
            }
            BIND (IF(BOUND(?protein_ac), ?protein_ac, ?protein) AS ?controller_id)}
          }

        ORDER BY ?control_type
        """

    sparql.setQuery(query_all_controllers)
    sparql.setReturnFormat(JSON)
    return sparql.queryAndConvert()


def select_reactant_product(sparql, reaction_uri):
    """
    It retrieves all reactants and products of a given reaction.

    :param sparql: SPARQLWrapper object using the ebi endpoint.
    :param reaction_uri: The reaction URI identifier.
    :return: The query result in JSON format.
    """

    query_react_prod = """
    PREFIX biopax3: <http://www.biopax.org/release/biopax-level3.owl#>
    SELECT DISTINCT ?component_id ?component_name ?component_type ?composition_type
    WHERE
      {
        VALUES ?reaction{<""" + reaction_uri + """>}
        { ?reaction biopax3:left ?component_id .
          VALUES ?composition_type{"Reactant"}}
        UNION { ?reaction biopax3:right ?component_id .
                VALUES ?composition_type{"Product"}}
        ?component_id a ?component_type ;
                        biopax3:displayName ?component_name
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


def select_full_info(sparql, end_unip, controller_id):
    """
    Using a federated query, it retrieves some information about a given controller. If controller_id is an URI
    the information is retrieved form Reactome, and if it is an Uniprot accesion number the information is retrieved
    from Uniprot.

    :param sparql: SPARQLWrapper object using the ebi endpoint.
    :param end_unip: The URL of the Uniprot endpoint.
    :param controller_id: The controller identifier, either an URI or a Uniprot AC.
    :return: The query result in JSON format.
    """

    query_full_info = """
        PREFIX biopax3: <http://www.biopax.org/release/biopax-level3.owl#>
        PREFIX up_core:<http://purl.uniprot.org/core/>
        PREFIX uniprot:<http://purl.uniprot.org/uniprot/>
        PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
        PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>

        SELECT DISTINCT ?controller_name ?data_1
        WHERE
          {
             {<""" + controller_id + """> biopax3:displayName ?controller_name ;
                            biopax3:cellularLocation ?cell_vocabulary .
             ?cell_vocabulary biopax3:term ?data_1}
             UNION {SERVICE <""" + end_unip + """> {
                uniprot:""" + extract_fragment_from_uri(controller_id) + """ rdfs:label ?controller_name ;
                         up_core:encodedBy ?gene .
                ?gene skos:prefLabel ?data_1}}
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
