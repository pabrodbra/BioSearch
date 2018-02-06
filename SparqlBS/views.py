from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from SparqlBS.utilities import *
# Create your views here.

ebi_endpoint = "https://www.ebi.ac.uk/rdf/services/sparql"
sparql_ebi = SPARQLWrapper(ebi_endpoint)

uniprot_endpoint = "http://sparql.uniprot.org/sparql"
sparql_uniprot = SPARQLWrapper(uniprot_endpoint)


def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    return render(request, 'contact.html')

# -- SPARQL

def search_pathways(request):
    pathway_search = request.GET.get('input')
    print(pathway_search)

    pathway_result = select_pathway(sparql_ebi, pathway_search)
    pathway_list = convert_json_format_into_list(pathway_result)

    if len(pathway_list) > 1:
        print()
        print("The found pathways are:")
        i = 1
        for l in pathway_list[1:]:
            # Se muestra: Index | Pathway_name (Organism_name)
            print(str(i) + ' | ' + l[1] + ' (' + l[2] + ')')
            i += 1

    else:
        print("None found")
    # return HttpResponse('OK', content_type=pathway_results)
    response = JsonResponse(pathway_result)

    return HttpResponse(response, content_type="application/json")


def search_reactions(request):
    pathway_uri = request.GET.get('input')

    reaction_result = select_reaction(sparql_ebi, pathway_uri)
    reaction_list = convert_json_format_into_list(reaction_result)

    if len(reaction_list) > 1:
        print()
        print("The found reactions are:")
        i = 1
        for l in reaction_list[1:]:
            # Se muestra: Index | Reaction_name (Reaction_direction)
            print(str(i) + ' | ' + l[1] + ' (' + l[2] + ')')
            i += 1

    else:
        print("Reactions not found in that pathway!")

    response = JsonResponse(reaction_result)
    return HttpResponse(response, content_type="application/json")


def search_controllers(request):
    reaction_uri = request.GET.get('input')

    controller_result = select_all_controller(sparql_ebi, reaction_uri)
    controller_list = convert_json_format_into_list(controller_result)

    if len(controller_list) > 1:
        print()
        print("The found controllers are:")
        for l in controller_list[1:]:
            # Se muestra: Control_entity_type (Control_type): Controller_name (Controller_type)
            print(extract_fragment_from_uri(l[3]) + ' (' + l[4] + '): ' + l[1] +
                  ' (' + extract_fragment_from_uri(l[2]) + ')')

    else:
        print("Controllers not found in that reaction!")

    response = JsonResponse(controller_result)
    return HttpResponse(response, content_type="application/json")


def search_reactant_product(request):
    reaction_uri = request.GET.get('input')

    react_prod_result = select_reactant_product(sparql_ebi, reaction_uri)
    react_prod_list = convert_json_format_into_list(react_prod_result)

    if len(react_prod_list) > 1:
        print()
        print("The found reactants or products are:")
        for l in react_prod_list[1:]:
            # Se muestra: Composition_type: Component_name (Component_type)
            print(l[3] + ': ' + l[1] + ' (' + extract_fragment_from_uri(l[2]) + ')')

    else:
        print("Not reactants nor products found in that reaction!")

    response = JsonResponse(react_prod_result)
    return HttpResponse(response, content_type="application/json")


def search_component_info(request):
    # Federated query
    controller_id = request.GET.get('input')

    controller_info_result = select_full_info(sparql_ebi, uniprot_endpoint, controller_id)
    controller_info_list = convert_json_format_into_list(controller_info_result)

    if len(controller_info_list) > 1:
        print()
        print("The found information for the controller is:")
        for l in controller_info_list[1:]:
            # Se muestra: Controller_name (Cellular_location or Gene_name)
            print(l[0] + ' (' + l[1] + ')')

    else:
        print("Information not found for that controller!")

    response = JsonResponse(controller_info_result)
    return HttpResponse(response, content_type="application/json")
