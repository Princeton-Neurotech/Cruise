import React, { useState } from 'react';
import Collapse from 'react-bootstrap/Collapse';
import Button from 'react-bootstrap/Button';
import WordCount from './WordCount';
import PageCount from './PageCount';
import axios from 'axios';
import reportValidity from 'report-validity'

let wordCount = 0
let pageCount = 0

const Thresholds = () => {

    const sendThr = (() => {
        let form = document.getElementById('fontSettingsList');
        let res = reportValidity(form);
        if (res) {
            axios.post("http://127.0.0.1:8080/api/thr/", { wordCount: wordCount,
                                                            pageCount: pageCount })
                .then(res => {
                    console.log(res);
                    console.log(res.data);
                })
        }
    }
    )
    const handleCallbackOne = (childData) =>{
        console.log(childData);
        // this.setState({LineSpace: childData})
        wordCount = childData;
    }

    const handleCallbackTwo = (childData) =>{
        console.log(childData);
        // this.setState({LineSpace: childData})
        pageCount = childData;
    }
    
    const [open, setOpen] = useState(false);
    return (
        <div className='thresholds'>
            <Button
                id='thresholdsBtn'
                onClick={() => setOpen(!open)}
                aria-controls="threshholdsList"
                aria-expanded={open}
            >
                Word and Page Count
            </Button>
            <Collapse in={open}>
                <div id="threshholdsList">
                    <WordCount parentCallback = {handleCallbackOne} />
                    <PageCount parentCallback = {handleCallbackTwo}/>
                    <button className="btn btn-success" onClick={sendThr}>submit</button>
                </div>
            </Collapse>
        </div>
    )
}

export default Thresholds