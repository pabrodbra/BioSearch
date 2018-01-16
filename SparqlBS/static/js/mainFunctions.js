/*
@author Pablo Rodriguez Brazzarola
BioSearch
Universidad de Málaga
*/

var object;

// -- HELPERS
var list_item_class = "list-group-item"
var list_item_button_class = "btn btn-lg btn-block btn-default"

var pathway_uri = "";
var reaction_uri = "";
var protein_uri = "";

function parseJSONresult(json_response){
	/*
	var variables = results["head"]["vars"]
    query_rows = [[row[v]["value"] for v in variables] for row in results["results"]["bindings"]]
    query_rows.insert(0, variables)

    return query_rows*/
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
			//PARSE
			/*
			console.log("--- RESPONSE ---");
			console.log(response);
			console.log("--- PARSED RESPONSE ---");
			*/
			object = response;
			parsed_pathway = parseResponse(response);
			//var test = JSON.parse(response);
		},
		complete:function(){
			appendPathways(parsed_pathway);
		},
		error:function(e){
			console.log("***ERROR*** :: " + e)
		}
	});

}

// -- CREATING
/*
 <div id="div1">
<p id="p1">This is a paragraph.</p>
<p id="p2">This is another paragraph.</p>
</div>

<script>
var para = document.createElement("p");
var node = document.createTextNode("This is new.");
para.appendChild(node);

var element = document.getElementById("div1");
element.appendChild(para);
</script> 
*/
var test;
function appendPathways(parsed_response){
	// Get List to Append
	var pathway_list = document.getElementById("pathway_list");

	variables = parsed_response.vars;
	results = parsed_response.results;
	console.log("DEBUG 1");
	console.log(variables);
	console.log(results);
	test = variables;

	for (var result in results){
		console.log("------------------- NEW RESULT ------------------------")
		var current_result = results[result]
		// Create Elements
		var new_li = document.createElement('li');
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
				new_string += current_value +  /n  ;
			}
		}
		console.log(new_string);
		// Add text to element
		var new_text = document.createTextNode(new_string);

		new_button.appendChild(new_text);

		pathway_list.appendChild(new_button);
	}
}

function parseResponse(response){
	var variables = response.head.vars
	var object_arrays = response.results.bindings
	console.log("TESTING PARSERESPONSE");
	return {vars:variables, results:object_arrays}
}


// -- ONCLICK

$("#pathway_submit").click(function() {
	searchPathways();
});