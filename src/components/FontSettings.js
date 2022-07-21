import React, { useState } from 'react'
import Collapse from 'react-bootstrap/Collapse';
import Button from 'react-bootstrap/Button';
import FontFamilies from './FontFamilies';
import FontSize from './FontSize';
import LineSpace from './LineSpace';
import axios from 'axios';
import reportValidity from 'report-validity'

class FontSettings extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            LineSpace: '',
            FontSize: 12,
            FontFamily: '',
            open: false,
        };
    }
    // const [open, setOpen] = useState(false);
    handleCallbackThree = (childData) =>{
        console.log(childData);
        this.setState({LineSpace: childData})
    }
    handleCallbackTwo = (childData) =>{
        console.log(childData);
        this.setState({FontSize: childData})
    }
    handleCallbackOne = (childData) =>{
        console.log(childData);
        this.setState({FontFamily: childData})
    }
    setOpen= (() => {
        this.setState({open: !this.state.open})
    })
    sendFont = (() => {
        let form = document.getElementById('fontSettingsList');
        let res = reportValidity(form);
        
        if (res) {
            
            axios.post("http://127.0.0.1:8080/api/fonts/", { LineSpace: this.state.LineSpace,
                                                            FontSize: this.state.FontSize,
                                                            FontFamily: this.state.FontFamily })
                .then(res => {
                    console.log(res);
                    console.log(res.data);
                })
        }
    }
    )
    render() {
        return (
            <div className='fontSettings' >
                <Button
                    id='fontSettingsBtn'
                    onClick={this.setOpen}
                    aria-controls="fontSettingsList"
                    aria-expanded={this.state.open}
                >
                    Font Settings
                </Button>
                <Collapse in={this.state.open}>
                    <form id="fontSettingsList">
                        {/* <FontFamilies value={this.state.value}
                            onChangeValue={this.handleChangeValue} 
                            parentCallback = {this.handleCallback}/> */}
                        <FontFamilies parentCallback = {this.handleCallbackOne} />
                        <FontSize parentCallback = {this.handleCallbackTwo} />
                        <LineSpace parentCallback = {this.handleCallbackThree} />
                        <button className="btn btn-success" onClick={this.sendFont}>Submit</button>
                    </form>
                </Collapse>
            </div>
        )
    }
}

export default FontSettings