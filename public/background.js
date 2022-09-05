/*
// background.js
chrome.storage.local.get(["badgeText"], ({ badgeText }) => {
    chrome.action.setBadgeText({ text: badgeText });
  });
  
  // Listener is registered on startup
  chrome.action.onClicked.addListener(handleActionClick);

  chrome.runtime.onMessage.addListener(({ type, name }) => {
    if (type === "set-name") {
      chrome.storage.local.set({ name });
    }
  });
  
  chrome.action.onClicked.addListener((tab) => {
    chrome.storage.local.get(["name"], ({ name }) => {
      chrome.tabs.sendMessage(tab.id, { name });
    });
  });

  /*
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
    navigator.serviceWorker.register('/service-worker.js');
    });
}
*/

console.log('registering service worker')
console.log('serviceWorker' in navigator);
// Don't register the service worker until the page has fully loaded
/// window.addEventListener('load', () => {
// Is service worker available?

// await new Promise(r => setTimeout(r, 10000));
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js', {scope: 'chrome-extension://ojekocpkijekdkidfjfgefpebilikohj/'}).then(() => {
      console.log('IMPORTANT');
      console.log('Service worker registered!');
  }).catch((error) => {
    console.warn('Error registering service worker:');
    console.warn(error);
  });
}
// });
self.addEventListener( "install", function( event ){
  console.log( "WORKER: install event in progress." );
});
self.addEventListener( "activate", event => {
    console.log('WORKER: activate event in progress.');
});
self.addEventListener( "fetch", event => {
console.log('WORKER: Fetching', event.request);
});

let lifeline;

keepAlive();

chrome.runtime.onConnect.addListener(port => {
  if (port.name === 'keepAlive') {
    lifeline = port;
    setTimeout(keepAliveForced, 295e3); // 5 minutes minus 5 seconds
    port.onDisconnect.addListener(keepAliveForced);
  }
});

function keepAliveForced() {
  lifeline?.disconnect();
  lifeline = null;
  keepAlive();
}

async function keepAlive() {
  if (lifeline) return;
  for (const tab of await chrome.tabs.query({ url: '*://*/*' })) {
    try {
      await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: () => chrome.runtime.connect({ name: 'keepAlive' }),
        // `function` will become `func` in Chrome 93+
      });
      chrome.tabs.onUpdated.removeListener(retryOnTabUpdate);
      return;
    } catch (e) {}
  }
  chrome.tabs.onUpdated.addListener(retryOnTabUpdate);
}

async function retryOnTabUpdate(tabId, info, tab) {
  if (info.url && /^(file|https?):/.test(info.url)) {
    keepAlive();
  }
}

chrome.runtime.getURL("index.html")
chrome.tabs.create({ url: chrome.runtime.getURL("index.html") });