/*
@author Pablo Rodriguez Brazzarola
BioSearch
Universidad de Málaga
*/

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

	console.log(input_pathway);

	$.ajax({
		url: 'pathway',
		type: "GET",
		data: {'input':input_pathway},
		success:function(response){
			//PARSE
			console.log("--- RESPONSE ---");
			console.log(response);
			console.log("--- PARSED RESPONSE ---");
			var test = JSON.parse(response);
			console.log(test["head"]["vars"]);
		},
		complete:function(){
			appendPathways();
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

function appendPathways(pathway_results){
	var pathway_list = document.getElementById("pathway_list");
	for (i=0; i<10; i++){
	//for (var path in pathway_results){
		var temp_li = document.createElement('li');
		temp_li.className = list_item_class;
		var temp_button = document.createElement('button');
		temp_button.className = list_item_button_class;
		var temp_text = document.createTextNode(i);

		temp_button.appendChild(temp_text);

		pathway_list.appendChild(temp_button);
	}
}


// -- ONCLICK

$("#pathway_submit").click(function() {
	console.log("TEST")
	searchPathways();
});