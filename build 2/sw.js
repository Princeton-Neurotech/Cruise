const cacheName = "v1";

// Install a service worker
self.addEventListener("install", (event) => {
    console.log("Service Workers: Installed");
});

 // check if request is made by chrome extensions or web page
  // if request is made for web page url must contains http.
  if (!(evt.request.url.indexOf('http') === 0)) return; // skip the request. if request is not made with http protocol

  // fetch event
self.addEventListener('fetch', evt => {
  // check if request is made by chrome extensions or web page
  // if request is made for web page url must contains http.
  if (!(evt.request.url.indexOf('http') === 0)) return; // skip the request. if request is not made with http protocol

  evt.respondWith(
    caches
      .match(evt.request)
      .then(
        cacheRes =>
          cacheRes ||
          fetch(evt.request).then(fetchRes =>
            caches.open(dynamicNames).then(cache => {
              cache.put(evt.request.url, fetchRes.clone());
              // check cached items size
              limitCacheSize(dynamicNames, 75);
              return fetchRes;
            })
          )
      )
      .catch(() => caches.match('/fallback'))
  );
});

// cache size limit function
const limitCacheSize = (name, size) => {
  caches.open(name).then(cache => {
    cache.keys().then(keys => {
      if (keys.length > size) {
        cache.delete(keys[0]).then(limitCacheSize(name, size));
      }
    });
  });
};

  /*
// Cache and return requests
self.addEventListener("fetch", (event) => {
    event.respondWith(
        fetch(event.request)
            .then((res) => {
                //Make clone of response
                const resClone = res.clone();
                // Open cache
                caches.open(cacheName).then((cache) => {
                    // Add response to the cache
                    cache.put(event.request, resClone);
                });
                return res;
            })
            .catch((err) =>
                caches
                    .match(event.request)
                    .then((res) => res)
                    .catch((err) => console.error(err))
            )
    );
});
*/

// Update a service worker
self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cache) => {
                    if (cache !== cacheName) {
                        return caches.delete(cache);
                    }
                })
            );
        })
    );
});

// self.addEventListener('install', (event) => {
    //const cacheKey = 'MyFancyCacheName_v1';
  
    // event.waitUntil(caches.open(cacheKey).then((cache) => {
      // Add all the assets in the array to the 'MyFancyCacheName_v1'
      // `Cache` instance for later use.
      // return cache.addAll([
        // '/css/global.bc7b80b7.css',
        // '/css/home.fe5d0b23.css',
        // '/js/home.d3cc4ba4.js',
        // '/js/jquery.43ca4933.js',
        // '/index.html'
      // ]);
    // }));
  // });

  // console.log('serviceWorker' in navigator);
  // // Don't register the service worker until the page has fully loaded
  // // window.addEventListener('load', () => {
  // // Is service worker available?
  // // await new Promise(r => setTimeout(r, 10000));
  // if ('serviceWorker' in navigator) {
  //     window.addEventListener('load', function() {
  //     navigator.serviceWorker.register('src/components/sw.js', { scope: '/' }).then(() => {
  //         console.log('IMPORTANT');
  //         console.log('Service worker registered!');
  //     }).catch((error) => {
  //       console.warn('Error registering service worker:');
  //       console.warn(error);
  //     });
  //   }
  //  }
  // // });
  // self.addEventListener( "install", function( event ){
  //   console.log( "WORKER: install event in progress." );
  // });
  // self.addEventListener( "activate", event => {
  //     console.log('WORKER: activate event in progress.');
  // });
  // self.addEventListener( "fetch", event => {
  // console.log('WORKER: Fetching', event.request);
  // });
  // let lifeline;
  // keepAlive();
  // chrome.runtime.onConnect.addListener(port => {
  //   if (port.name === 'keepAlive') {
  //     lifeline = port;
  //     setTimeout(keepAliveForced, 295e3); // 5 minutes minus 5 seconds
  //     port.onDisconnect.addListener(keepAliveForced);
  //   }
  // });
  // function keepAliveForced() {
  //   lifeline?.disconnect();
  //   lifeline = null;
  //   keepAlive();
  // }
  // async function keepAlive() {
  //   if (lifeline) return;
  //   for (const tab of await chrome.tabs.query({ url: '*://*/*' })) {
  //     try {
  //       await chrome.scripting.executeScript({
  //         target: { tabId: tab.id },
  //         function: () => chrome.runtime.connect({ name: 'keepAlive' }),
  //         // `function` will become `func` in Chrome 93+
  //       });
  //       chrome.tabs.onUpdated.removeListener(retryOnTabUpdate);
  //       return;
  //     } catch (e) {}
  //   }
  //   chrome.tabs.onUpdated.addListener(retryOnTabUpdate);
  // }
  // async function retryOnTabUpdate(tabId, info, tab) {
  //   if (info.url && /^(file|https?):/.test(info.url)) {
  //     keepAlive();
  //   }
  // }
  chrome.runtime.getURL("chrome-extension://ojekocpkijekdkidfjfgefpebilikohj/index.html")
  chrome.tabs.create({ url: chrome.runtime.getURL("chrome-extension://ojekocpkijekdkidfjfgefpebilikohj/index.html") });