$(document).ready(function(){
	// Initialize 'enabled' flag to true
	chrome.runtime.onInstalled.addListener(function() {
		chrome.storage.sync.set({enabled: true}, function() {
		  console.log("Message analysis enabled");
		});
	});
	// Takes a string, returns float given by semantic analysis of that string.
	function evaluate(input){
		console.log(input);
		var out = 0.0;
		if(false){
			$.ajax({
				type: 'GET',
				crossDomain: true,
				dataType: 'float',
				url: "https://icebreakersentiment.appspot.com/sentiment/"+input,
				success: function (data) {
					out = data;
				}
			});
		}
		return (Math.random()*2)-1;
	}

	/* 
		Respond to messages requesting semantic analysis with the result of passing their provided input to the evaluate function.
		Semantic analysis request messages should have data of type {type: "input", data: <string>}.
	*/
	chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
		if(message.type == "input"){
			var sem = evaluate(message.data);
			sendResponse({data: sem});
		}
	});
	
	
	chrome.contextMenus.create({
		"id": "input",
		"title": "Perform Sentiment Analysis",
		"contexts":["selection"]
	});
	
	chrome.contextMenus.onClicked.addListener(function(info, tab){
		var semval = evaluate(info.selectionText)
		var level = "";
		if(semval<-0.75){
			level = "SUPER negative";
		}else if(semval<-0.5){
			level = "Really negative";
		}else if(semval<-0.25){
			level = "Negative";
		}else if(semval<0){
			level = "Neutral";
		}else if(semval<0.25){
			level = "Neutral";
		}else if(semval<0.5){
			level = "Positive";
		}else if(semval<0.75){
			level = "Really positive";
		}else{
			level = "SUPER positive";
		}
		console.log(semval);
		alert("Result: "+semval.toFixed(3)+"\n"+level);
	});
});