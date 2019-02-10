$(document).ready(function(){
	// Initialize 'enabled' flag to true
	chrome.runtime.onInstalled.addListener(function() {
		chrome.storage.sync.set({enabled: true}, function() {
		  console.log("Message analysis enabled");
		});
	});
	// Takes a string, returns float given by sentiment analysis of that string.
	function evaluate(input, func){
		$.get("https://icebreakersentiment.appspot.com/sentiment/"+input, func(data));
	}

	/* 
		Respond to messages requesting sentiment analysis with the result of passing their provided input to the evaluate function.
		Sentiment analysis request messages should have data of type {type: "input", data: <string>}.
	*/
	chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
		if(message.type == "input"){
			evaluate(message.data, sendResponse);
		}
	});
	
	
	chrome.contextMenus.create({
		"id": "input",
		"title": "Perform Sentiment Analysis",
		"contexts":["selection"]
	});
	
	chrome.contextMenus.onClicked.addListener(function(info, tab){
		$.get("https://icebreakersentiment.appspot.com/sentiment/"+info.selectionText, function(data){
			var level = "";
			if(data<-0.75)     { level = "SUPER negative";  }
			else if(data<-0.5) { level = "Really negative"; }
			else if(data<-0.25){ level = "Negative";        }
			else if(data<0)    { level = "Neutral";         }
			else if(data<0.25) { level = "Neutral";         }
			else if(data<0.5)  { level = "Positive";        }
			else if(data<0.75) { level = "Really positive"; }
			else               { level = "SUPER positive";  }
			
			console.log(data);
			alert("Result: "+data.substring(0, 5)+"\n"+level);
		});
	});
});