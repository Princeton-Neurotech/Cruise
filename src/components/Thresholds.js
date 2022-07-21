import React, { useState } from 'react';
import Collapse from 'react-bootstrap/Collapse';
import Button from 'react-bootstrap/Button';
import WordCount from './WordCount';
import PageCount from './PageCount';
import axios from 'axios';
import reportValidity from 'report-validity'
import ReactNotifications from 'react-browser-notifications';

class Thresholds extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isRoadblock: false,
            isCompletion: false,
            wordCount: 0,
            pageCount: 0,
            open: false,
        };
    }

    setRoadblock = () => {
        setInterval(this.checkRoadblock()
            , 1000)
    }

    setCompletion = () => {
        setInterval(this.checkCompletion()
            , 5000)
    }

    showRoadblockNotifications() {
        console.log(this.n.supported())
        if (this.n.supported()) this.n.show();
    }

    showCompNotifications() {
        console.log(this.a.supported())
        if (this.a.supported()) this.a.show();
    }

    handleRoadClick(event) {
        this.n.close(event.target.tag);
    }
    handleCompClick(event) {
        this.a.close(event.target.tag);
    }

    sendThr = (() => {
        setInterval(() => {
            this.checkRoadblock()
        }, 1000);
        let form = document.getElementById('fontSettingsList');
        let res = reportValidity(form);
        if (res) {
            axios.post("http://127.0.0.1:3000/api/thr/", { wordCount: this.state.wordCount,
                                                            pageCount: this.state.pageCount })
                .then(res => {
                    console.log(res);
                    console.log(res.data);
                })
        }

        setInterval(() => {
            this.checkCompletion()
        }, 5000);
    })

    checkRoadblock() {
            axios.get("http://127.0.0.1:3000/api/roadblock/")
                .then(res => {
                    if (res.data[0] == 'True') {
                        this.showRoadblockNotifications();
                        this.state.isRoadblock = true;
                    }
                    // need to then set back to false!
                    // console.log(res);
                    // console.log(res.data);
                })
        }

    checkCompletion() {
        axios.get("http://127.0.0.1:3000/api/completion/")
            .then(res => {
                if (res.data[0] == 'True') {
                    this.showCompNotifications();
                    this.state.isCompletion = true;
                }
                // console.log(res);
                // console.log(res.data);
            })
    }

    handleCallbackOne = (childData) =>{
        console.log(childData);
        // this.setState({LineSpace: childData})
        this.state.wordCount = childData;
    }

    handleCallbackTwo = (childData) =>{
        console.log(childData);
        // this.setState({LineSpace: childData})
        this.state.pageCount = childData;
    }
    
    // const [open, setOpen] = useState(false);
    render(){
        return (
            <div className='thresholds'>
                <ReactNotifications
                    onRef={ref => (this.n = ref)} 
                        title="You have approached a roadblock!"
                        body="You have approached a roadblock!"
                        // tag="abcdef"
                        // timeout="2000"
                    onClick={event => this.handleRoadClick(event)}
                />
                <ReactNotifications
                    onRef={ref => (this.a = ref)} 
                        title="You have completed your goal!"
                        body="You have completed your goal!"
                        // tag="abcdef"
                        // timeout="2000"
                    onClick={event => this.handleCompClick(event)}
                />
                <Button
                    id='thresholdsBtn'
                    onClick={() => {this.setState({open: !this.state.open})}}
                    aria-controls="threshholdsList"
                    aria-expanded={this.state.open}
                >
                    Word and Page Count
                </Button>
                <Collapse in={this.state.open}>
                    <div id="threshholdsList">
                        <WordCount parentCallback = {this.handleCallbackOne} />
                        <PageCount parentCallback = {this.handleCallbackTwo}/>
                        <button className="btn btn-success" onClick={this.sendThr}>submit</button>
                    </div>
                </Collapse>
            </div>)
        }
}

export default Thresholds