/*
@author Pablo Rodriguez Brazzarola
BioSearch
Universidad de Málaga
*/


function searchPathways(){
	var input_pathway = document.getElementById("pathway_input").value;

	console.log(input_pathway)

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
			console.log(test);
		},
		complete:function(){

		}
	});

}

$("#pathway_submit").click(function() {
	console.log("TEST")
	searchPathways();
});