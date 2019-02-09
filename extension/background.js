chrome.runtime.onInstalled.addListener(function() {
    chrome.storage.sync.set({enabled: true}, function() {
      console.log("Message analysis enabled");
    });
  });