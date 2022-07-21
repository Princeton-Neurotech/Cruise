import React from 'react'

class LineSpace extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            LineSpace: '',
        };
    }

    getInputValue = (e) =>{
        this.props.parentCallback(e.target.value);
    };
    render() {
        return (
            <div className="form-group fontFamiliesSection">
                <label htmlFor="lineSpace">Line Spacing</label>
                <input type="number"
                    title="Rate"
                    id="lineSpace"
                    className="form-control"
                    min="1.0"
                    step="0.05"
                    max="2.0"
                    onChange={this.getInputValue}
                />
            </div>

        )
    }
}
export default LineSpace