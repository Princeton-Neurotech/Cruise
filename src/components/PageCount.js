import React, { useState } from 'react'
import NumericInput from 'react-numeric-input'

class PageCount extends React.Component {
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
            <div className="form-group pageCountSection">
                <label htmlFor="" className='pageCountTitle'>Page Count Threshold</label>
                <br/>
                <label htmlFor="" className='pageCount'>How many total pages you want to write</label>
                <input type="number"
                    title="Rate"
                    id="pageCount"
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
export default PageCount