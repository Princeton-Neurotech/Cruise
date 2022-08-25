/*
import React, { useState } from 'react'

const fontFamilies = ["Select an Option", "First Option", "Second Option", "Third Option"];
class FontFamilies extends React.Component {
    constructor(props) {
        super(props);

        this.state = { value: 'Select an Option' };
    }
    // onChange= (e) => {
    //     this.setState({
    //         value: e.target.value
    //     })
    //     this.props.parentCallback(e.target.value);
    // }
    getInputValue = (e) =>{
        this.props.parentCallback(e.target.value);
    };
    // onChange={this.onChange.bind(this)}
    render() {
        return (
            <div className="form-group fontFamiliesSection">
                <label htmlFor="fontFamilies">Font Family</label>
                <select value={this.state.value} onChange={this.getInputValue} className="form-control">
                    {fontFamilies.map(option => {
                        return <option value={option} key={option} >{option}</option>
                    })}
                </select>
            </div>

        )
    }
}
export default FontFamilies
*/