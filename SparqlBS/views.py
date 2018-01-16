from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from SparqlBS.utilities import *
# Create your views here.

ebi_endpoint = "https://www.ebi.ac.uk/rdf/services/sparql"


def index(request):

	return render(request, 'index.html')

def search_pathways(request):
	sparql = SPARQLWrapper(ebi_endpoint)

	print("Insert a pathway name: ")
	pathway_search = request.GET.get('input')
	print(pathway_search)

	pathway_results = select_pathway(sparql, pathway_search)
	pathway_list = convert_json_format_into_list(pathway_results)

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
	#return HttpResponse('OK', content_type=pathway_results)
	response = JsonResponse(pathway_results)

	return HttpResponse(response, content_type="application/json")
