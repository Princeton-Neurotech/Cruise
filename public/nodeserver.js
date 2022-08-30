// const express = require('express')
// const app = express()
// const port = 3000

// app.get('/', (req, res) => {
//     res.sendFile(path.join(__dirname, 'index.html'));
// })

// app.listen(port, () => {
//   console.log(`Example app listening on port ${port}`)
// })
const {myURL} = require('/Users/amirtouil/cruise_extension/src/components/DocURL.js');

var request = require('request-promise');
  
async function arraysum() {
  
    // This variable contains the data
    // you want to send 
    var data = {
        array: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    }
  
    var options = {
        method: 'POST',
  
        // http:flaskserverurl:port/route
        uri: 'http://localhost:5000/url',
        body: data,
  
        // Automatically stringifies
        // the body to JSON 
        json: true
    };
  
    var sendrequest = await request(options)
  
        // The parsedBody contains the data
        // sent back from the Flask server 
        .then(function (parsedBody) {
            console.log(parsedBody);
              
            // You can do something with
            // returned data
            let result;
            result = parsedBody['result'];
            console.log("Sum of Array from Python: ", result);
            console.log(myURL.url)
        })
        .catch(function (err) {
            console.log(err);
        });
}

var command = require("shebang!../bin/command");
  
arraysum();