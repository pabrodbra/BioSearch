/*
@author Pablo Rodriguez Brazzarola
BioSearch
Universidad de Málaga
*/

// DEBUGGIN
var object;
var test;

// -- HELPERS
var list_item_class = "list-group-item"
var list_item_button_class = "btn btn-md btn-default"

var pathway_uri = "";
var reaction_uri = "";
var controller_uri = "";


function parseResponse(response){
	var variables = response.head.vars
	var object_arrays = response.results.bindings
	return {vars:variables, results:object_arrays}
}

// -- SEARCHING

function searchSPARQL(url, result_list, result_item, input_id){
	var parsed_results = {}
	console.log("--- Search SPARQL");
	console.log(input_id);
	console.log(url);

	$.ajax({
		url: url,
		type: "GET",
		data: {'input': input_id},
		success:function(response){
			parsed_results = parseResponse(response);
		},
		complete:function(){
			if(url != "component_info")
				appendResults(parsed_results, result_list, result_item)
			else
				appendInfo(parsed_results, result_list, result_item); console.log(url)
		},
		error:function(e){
			console.log("***ERROR*** :: " + e)
		}
	});

}

// -- CREATING

function appendResults(parsed_response, list_id, child_class){
	// Get List to Append
	var results_list = document.getElementById(list_id);//clearList(list_id);

	variables = parsed_response.vars;
	results = parsed_response.results;

	console.log(results);

	for (var result in results){
		var current_result = results[result]
		// Create Elements
		var new_li = document.createElement('li');
		new_li.className = list_item_class;
		var new_button = document.createElement('button');
		new_button.className = list_item_button_class + " " + child_class;

		var new_string = "";

		//new_button.setAttribute("id", uri)
		// Create text from variables of results
		for (var var_name in variables){
			current_value = current_result[variables[var_name]]['value'];
			if (var_name == 0){
				new_button.setAttribute("id", current_result[variables[var_name]]['value']);
			}
			else{
				current_value = current_value.split('#').pop();
				if (var_name == variables.length-1){
					new_string += current_value;
				} else {
					new_string += current_value + " | " ;
				}
			}
		}

		// Add text to element
		var new_text = document.createTextNode(new_string);
		new_button.appendChild(new_text);
		results_list.appendChild(new_button);
	}
}

function appendInfo(parsed_response, list_id, child_class){
	var results_list = document.getElementById(list_id);//clearList(list_id);

	variables = parsed_response.vars;
	results = parsed_response.results;

	for (var result in results){
		var current_result = results[result]
		// Create Elements

		for (var var_name in variables){
			var new_li = document.createElement('li');
			new_li.className = list_item_class;
			var new_button = document.createElement('button');
			new_button.className = list_item_button_class + " " + child_class;

			var new_string = "";

			//new_button.setAttribute("id", uri)
			// Create text from variables of results
			current_value = current_result[variables[var_name]]['value'];
			// Only for sequences
			if (current_value.length > 50 && current_value.match(" ") == null)
			    current_value = current_value.match(/.{37}/g).join(' ');
			console.log("***DEBUG*** current_value = " + current_value)
			current_value = current_value.split('#').pop();
			new_string += current_value;
			
			// Add text to element
			var new_text = document.createTextNode(new_string);
			new_button.appendChild(new_text);
			results_list.appendChild(new_button);
		}

	}
}

// -- ONCLICK
var last_path = null, last_reaction = null, last_controller = null;

function activateButton(last_button, current_button){
	if(last_button != null){
		last_button.removeClass("btn-primary");
		last_button.addClass("btn-default");
	}
	current_button.removeClass("btn-default");
	current_button.addClass("btn-primary");
}

function clearList(list_id){
	var selected_list = document.getElementById(list_id);
	while (selected_list.firstChild) {
		selected_list.removeChild(selected_list.firstChild);
	}
	return selected_list;
}
// - Pathways

$("#pathway_input").keypress(function(e){
    if(e.which == 13){//Enter key pressed
        $('#pathway_submit').click();//Trigger search button click event
    }
});

$("#pathway_submit").click(function() {
	clearList("pathway_list");
	clearList("reaction_list");
	clearList("component_list");
	clearList("component_info");

	var input_pathway = document.getElementById("pathway_input").value;
	searchSPARQL("pathway", "pathway_list", "pathway_item", input_pathway);
});

// - Reactions

$(document).on('click', ".pathway_item", function() {
	clearList("reaction_list");
	clearList("component_list");
	clearList("component_info");

	activateButton(last_path, $(this));
	last_path = $(this);

	pathway_uri = $(this).attr('id');
	reaction_uri = "";
	controller_uri = "";

	searchSPARQL("reaction", "reaction_list", "reaction_item", pathway_uri);
});

// - Components

$(document).on('click', ".reaction_item", function() {
	clearList("component_list");
	clearList("component_info");

	activateButton(last_reaction, $(this));
	last_reaction = $(this);

	reaction_uri = $(this).attr('id');
	controller_uri = "";

	searchSPARQL("controller", "component_list", "component_item", reaction_uri);
	searchSPARQL("reactant_product", "component_list", "component_item", reaction_uri);
});

// - Component Info

$(document).on('click', ".component_item", function() {
	clearList("component_info");
	activateButton(last_controller, $(this));
	last_controller = $(this);

	controller_uri = $(this).attr('id')

	searchSPARQL("component_info", "component_info", "info_item", controller_uri);
});