import React, { useEffect, useRef } from 'react'
import reportValidity from 'report-validity'
import axios from 'axios';
// module.exports = {myURL};
let url = ''
let myURL = {
    url: url
}

const DocURL = () => {

    const getInputValue = (event) => {
        // show the user input value to console
        const userValue = event.target.value;
        url = userValue;

        // console.log(userValue);
    };
    let URLform = useRef()
    const sendURL = (() => {
        let form = document.getElementById('urlForm');
        let res = reportValidity(form);
        // console.log(url);
        if (res) {
            console.log(url)
            axios.post("http://127.0.0.1:8080/api/url/", { URL: url })
                .then(res => {
                    console.log(res);
                    console.log(res.data);
                })
        }
    }
    )
    return (
        <div>
            <form ref={URLform} id='urlForm'>
                <label>
                    Document URL:
                    <input type="text" name="docURL" onChange={getInputValue} />
                </label>
            </form>
            <button className="btn btn-success" onClick={sendURL}>Submit</button>
        </div>
    )
}

export default DocURL
