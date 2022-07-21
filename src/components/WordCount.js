import React, { useState } from 'react'
import NumericInput from 'react-numeric-input'

class WordCount extends React.Component {
    constructor(props) {
        super(props);
    }
    // onChange(e) {
    //     this.setState({
    //         value: e.target.value
    //     })
    // }
    getInputValue = (e) =>{
        this.props.parentCallback(e.target.value);
    };
    render() {
        return (
            <div className="form-group wordCountSection">
                <label htmlFor="" className='wordCountTitle'>Word Count Threshold</label>
                <br/>
                <label htmlFor="" className='wordCount'>How many total words you want to write</label>
                <input type="number"
                    title="Rate"
                    id="wordCount"
                    className="form-control"
                    min="0"
                    step="1"
                    onChange={this.getInputValue}
                />
                {/* <NumericInput className="form-control"
                    value={0}
                    min={0}
                    step={1}
                    precision={0} /> */}
            </div>

        )
    }
}
export default WordCount