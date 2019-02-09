chrome.runtime.onInstalled.addListener(function() {
    chrome.storage.sync.set({enabled: true}, function() {
      console.log("Message analysis enabled");
    });
});
function evaluate(text){
	var out = 0;
	$.get("https://icebreakersentiment.appspot.com/sentiment/".concat(text), function (data) {
		out = data;
	});
	return out;
}
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
	if(message.type == "message_typed"){
		var sem = evaluate(message.data);
		sendResponse({data: sem});
	}
});