import React, { useState } from 'react'
import NumericInput from 'react-numeric-input'
import reportValidity from 'report-validity'
import axios from 'axios';

class TotalTime extends React.Component {
    constructor(props) {
        super(props);
        this.state = { Time: 0 };
    }
    // onChange(e) {
    //     this.setState({
    //         value: e.target.value
    //     })
    // }
    // getInputValue = (e) =>{
    //     this.props.parentCallback(e.target.value);
    // };
    getInputValue = (event) => {
        // show the user input value to console
        this.setState({ Time: event.target.value });
        // console.log(userValue);
    }
    sendTime = (() => {
        let form = document.getElementById('totalTimeSection');
        let res = reportValidity(form);
        if (res) {
            axios.post("http://127.0.0.1:8080/api/time/", { totalTime: this.state.Time })
                .then(res => {
                    console.log(res);
                    console.log(res.data);
                })
        }
    }
    )
    render() {
        return (
            <div>
                <form id='totalTimeSection'>
                    <label htmlFor="" className='totalTimeTitle'>Total Estimated Time (in minutes)</label>
                    <br />
                    <label htmlFor="" className='totalTime'>Time estimated to complete assignment</label>
                    <input type="number"
                        title="Rate"
                        id="totalTime"
                        className="form-control"
                        min="0"
                        max="6000"
                        step="1"
                        onChange={this.getInputValue}
                    />
                    <button className="btn btn-success" onClick={this.sendTime}>Submit</button>
                    {/* <NumericInput className="form-control"
                    value={0}
                    min={0}
                    step={1}
                    precision={0} /> */}
                </form>
            </div>

        )
    }
}
export default TotalTime