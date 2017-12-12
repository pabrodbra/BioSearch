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
var list_item_button_class = "btn btn-md btn-block btn-default"

var pathway_uri = "";
var reaction_uri = "";
var protein_uri = "";


function parseResponse(response){
	var variables = response.head.vars
	var object_arrays = response.results.bindings
	return {vars:variables, results:object_arrays}
}

// -- SEARCHING

function searchPathways(){
	var input_pathway = document.getElementById("pathway_input").value;
	var parsed_pathway = {}
	console.log(input_pathway);

	$.ajax({
		url: 'pathway',
		type: "GET",
		data: {'input':input_pathway},
		success:function(response){
			parsed_pathway = parseResponse(response);
			//var test = JSON.parse(response);
		},
		complete:function(){
			//appendPathways(parsed_pathway);
			appendResults(parsed_pathway, "pathway_list")
		},
		error:function(e){
			console.log("***ERROR*** :: " + e)
		}
	});

}

// -- CREATING

function appendResults(parsed_response, box_id){
	// Get List to Append
	var pathway_list = document.getElementById(box_id);
	while (pathway_list.firstChild) {
		pathway_list.removeChild(pathway_list.firstChild);
	}
	variables = parsed_response.vars;
	results = parsed_response.results;
	console.log("DEBUG 1");
	console.log(variables);
	console.log(results);
	test = variables;

	for (var result in results){
		var current_result = results[result]
		// Create Elements
		var new_li = document.createElement('li');
		new_li.
		new_li.className = list_item_class;
		var new_button = document.createElement('button');
		new_button.className = list_item_button_class;
		console.log("DEBUG 2");
		console.log(current_result)

		var new_string = "";

		//new_button.setAttribute("id", uri)
		console.log("DEBUG 3");
		// Create text from variables of results
		for (var var_name in variables){
			current_value = current_result[variables[var_name]]['value']
			if (var_name == 0){
				new_button.setAttribute("id", current_result[variables[var_name]]['value'])
			}
			else if (var_name == variables.length-1){
				new_string += current_value
			} else {
				new_string += current_value + " | " ;
			}
		}
		console.log(new_string);

		// Add text to element
		var new_text = document.createTextNode(new_string);
		new_button.appendChild(new_text);
		pathway_list.appendChild(new_button);
	}
}

// -- ONCLICK

$("#pathway_submit").click(function() {
	searchPathways();
});

$("#pathway_input").keypress(function(e){
    if(e.which == 13){//Enter key pressed
        $('#pathway_submit').click();//Trigger search button click event
    }
});