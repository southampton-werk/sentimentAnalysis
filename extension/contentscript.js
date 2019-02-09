function isTextBox(element) {
    var tagName = element.tagName.toLowerCase();
    if (tagName === 'textarea') return true;
    if (tagName !== 'input') return false;
    var type = element.getAttribute('type').toLowerCase();
    return type == 'text';
}

document.addEventListener("keypress", function(){
	if( 
	var active = document.activeElement;
	if(isTextBox(active){
		chrome.runtime.sendMessage({type:"message_typed",data:active.text}, function(response){
			var out = response.data
			if(out<0){
				active.style.color = "#ff0000"
			}else{
				active.style.color = "#00ff00"
			}
		});
	}
});