import React, { useState } from 'react'
import * as mdb from 'mdb-ui-kit'; // lib
import { counter } from 'mdb-ui-kit'; // module

class NavBar extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            settings: true,
            notifs: false
        };
    }
    setClicked() {
        this.setState({
            settings: true,
            notifs: false
        })
    }
    notifsClicked() {
        this.setState({
            settings: false,
            notifs: true
        })
    }
    render() {

        let set = this.state.settings ? "green" : "white";
        let notif = this.state.notifs ? "green" : "white";
        let settingsBtn = <button id="Settings" className={set} onClick={this.setClicked.bind(this)} autoFocus >Settings</button>;
        let notificationsBtn = <button id="Notifications" className={notif} onClick={this.notifsClicked.bind(this)}>
           
            Notifications</button>;
        return (
            <section className='NavWrap'>
                {settingsBtn}
                {notificationsBtn}
                <span className="counter counter-lg">9</span>
            </section>
        )
    }
}

export default NavBar