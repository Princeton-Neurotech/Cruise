import React from 'react'
import NumericInput from 'react-numeric-input';

class FontSize extends React.Component {
    constructor(props) {
        super(props);
    }
    getInputValue = (e) => {
        this.props.parentCallback(e.target.value);
    };
    render() {
        return (
            <div className="form-group fontFamiliesSection">
                <label htmlFor="fontFamilies">Font Size</label>
                <input type="number"
                    title="Rate"
                    id="lineSpace"
                    className="form-control"
                    min="1"
                    step="1"
                    max="400"
                    onChange={this.getInputValue}
                />
                {/* <input type="number" id="tentacles" name="tentacles"
                    min="1" max="400" step={1} onChange={this.getInputValue}></input> */}
                {/* <NumericInput className="form-control"
                    value={12}
                    min={0}
                    max={400}
                    step={1}
                    precision={0}
                    onChange={this.getInputValue} /> */}
            </div>

        )
    }
}
export default FontSize