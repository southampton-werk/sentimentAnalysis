console.log("script loaded");
function walk(node, func) {
    func(node);
    node = node.firstChild;
    while (node) {
        walk(node, func);
        node = node.nextSibling;
    }
}
function appEnabled(){
	var enabled = true;
	chrome.storage.local.get(['enabled'], function(result){
		if(result!=null){
			enabled = result.key;
		}
	});
	return enabled;
}
var source = null;
document.addEventListener('click', function(e){
	if(appEnabled()){
		e = e || window.event;
		var target = e.target || e.srcElement;
		console.log("Focused element: "+target.tagName);
		walk(target, function(node){
			if(node.nodeType==Node.ELEMENT_NODE){
				if(node.hasAttributes()){
					var attrs = node.attributes;
					if(attrs[0].name=='data-text' && attrs[0].value=="true"){
						source = node;
					}
				}
			}
		});
	}
});
document.addEventListener('keyup', function(){
	if(appEnabled()){
		source.focus();
		var input = source.innerHTML;
		var semval = null;
		chrome.runtime.sendMessage({type: "input", data: input}, function(response){
			semval = response.data;
		});
		console.log(input+":"+semval);
	}
});