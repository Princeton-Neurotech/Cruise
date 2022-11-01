// Import the functions you need from the SDKs you need
import React, { useState } from 'react';
import Collapse from 'react-bootstrap/Collapse';
import Button from 'react-bootstrap/Button';
import WordCount from './WordCount';
import PageCount from './PageCount';
import axios from 'axios';
import reportValidity from 'report-validity'
import ReactNotifications from 'react-browser-notifications';
import {NotificationContainer, NotificationManager} from 'react-notifications';
// import Notification  from 'Notification';
import Swal from 'sweetalert2';
window.Swal = Swal;
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

/*
const functions = require('firebase-functions');
const express = require('express');

const app = express();
// middleware
app.use(express.json({ extended: false }));

// Define Routes
app.use('/api/thr');
app.use('/api/roadblock');
app.use('/api/completion');
app.use('/api/ml');
*/

var cors = require('cors');
const port = process.env.PORT || 80;
class Thresholds extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isRoadblock: false,
            isCompletion: false,
            wordCount: 0,
            pageCount: 0,
            open: false,
            title: ""
        };
    }

  showRoadblockNotifications() {
      console.log(this.n.supported())
      if (this.n.supported()); 
      this.n.show();
  }

  showCompNotifications() {
      console.log(this.a.supported())
      if (this.a.supported());
      this.a.show();
  }

  handleRoadClick(event) {
      this.n.close(event.target.tag);
  }
  handleCompClick(event) {
      this.a.close(event.target.tag);
  }

  sendThr = (() => {
    // 5s for testing, final is every min
    setInterval(() => {
        this.checkRoadblock()
    }, 5000);

    // 5s for testing, final is every min
    setInterval(() => {
        this.checkCompletion()
    }, 5000);

    // do this every 5 min
    setInterval(() => {
        this.sendML()
    }, 300000);

    // let axiosConfig = {
    //     headers: {
    //         'Content-Type': 'application/json;charset=UTF-8',
    //         "Access-Control-Allow-Origin": "*",
    //     }
    //   };
 
    body = { wordCount: this.state.wordCount, pageCount: this.state.pageCount }
    axios.get("https://cruise-extension.herokuapp.com:80/api/thr", body).then(res => {
        console.log("post")                                                    
        console.log(res);
        console.log(res.data['wordcount']);
        if (!res.ok) {
            Swal.fire(
                'Unsuccessful',
                'Unable to delete selected user. Please contact administrator.',
                'error'
            );
            return;
        }
        Swal.fire({
            title: 'We expect you to take ' + (res.data['wordcount']/60).toFixed(2) + ' minutes',
            text: "",
            icon: 'OK',
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'OK',
        })
    })
})

  sendML = (() => {
    axios.get("https://cruise-extension.herokuapp.com/api/ml", {port:80})
})

  checkRoadblock() { 
    axios.get("https://cruise-extension.herokuapp.com/api/roadblock", {port:80}) 
      .then(res => {
              if (res.data[0] == 'True') {
                  console.log("roadblock notifs");
                  this.state.isRoadblock = true;
                  if (this.state.isRoadblock == true) {
                      Swal.fire({
                          title: 'You have approached a roadblock!',
                          text: "",
                          icon: 'OK',
                          confirmButtonColor: '#3085d6',
                          cancelButtonColor: '#d33',
                          confirmButtonText: 'OK',
                          iconHtml: '<img src="/src/components/sad_whale.png">'
                      })
                      }   
                      this.state.isRoadblock = false;
                  }
              // need to then set back to false!
              // console.log(res);
              // console.log(res.data);
          }).catch (
              function (error) {
                  console.log('Show error notification! ' + error)
                  return Promise.reject(error)
               }
          )
      }

  checkCompletion() {
    axios.get("https://cruise-extension.herokuapp.com/api/completion", {port:80}) 
          .then(res => {
              if (res.data[0] == 'True') {
                  this.state.notRun = true;
                  console.log("completion notifs");
                  // this.showCompNotifications();
                  this.state.isCompletion = true;
                  if (this.state.isCompletion == true) {
                  Swal.fire({
                      title: 'You have completed your goal!',
                      text: "",
                      icon: 'OK',
                      confirmButtonColor: '#3085d6',
                      cancelButtonColor: '#d33',
                      confirmButtonText: 'OK',
                      iconHtml: '<img src="/src/components/happy_whale.png">'
                  })
              }
              this.state.isCompletion = false;
              }
              // console.log(res);
              // console.log(res.data);
          }).catch (
              function (error) {
                  console.log('Show error notification! ' + error)
                  return Promise.reject(error)
              }
          )
  }

  handleCallbackOne = (childData) =>{
      // console.log(childData);
      // this.setState({LineSpace: childData})
      this.setState({ ...this.state , wordCount: childData });
  }

  handleCallbackTwo = (childData) =>{
      console.log(childData);
      // this.setState({LineSpace: childData})
      
      this.setState({ ...this.state , pageCount: childData });
  }

  handleButtonClick() {
      if(this.state.ignore) {
        return;
      }
  
      const now = Date.now();
  
      const title = 'React-Web-Notification' + now;
      const body = 'Hello' + new Date();
      const tag = now;
      // const icon = 'http://mobilusoss.github.io/react-web-notification/example/Notifications_button_24.png';
      // const icon = 'http://localhost:3000/Notifications_button_24.png';
  
      // Available options
      // See https://developer.mozilla.org/en-US/docs/Web/API/Notification/Notification
      const options = {
        tag: tag,
        body: body,
        // icon: icon,
        lang: 'en',
        dir: 'ltr',
        // sound: './sound.mp3'  // no browsers supported https://developer.mozilla.org/en/docs/Web/API/notification/sound#Browser_compatibility
      }
      this.setState({
        title: title,
        options: options
      });
    }
  
    handleButtonClick2() {
      this.props.swRegistration.getNotifications({}).then(function(notifications) {
        console.log(notifications);
      });
    }
    
  // const [open, setOpen] = useState(false);
  render() {
      return (
          <div className='thresholdsList'>
              <ReactNotifications
                  onRef={ref => (this.n = ref)} 
                      title="You have approached a roadblock!"
                      body="You have approached a roadblock!"
                      tag="roadblock"
                      timeout="2000"
                  onClick={event => this.handleRoadClick(event)}
              />
              <ReactNotifications
                  onRef={ref => (this.a = ref)} 
                      title="You have completed your goal!"
                      body="You have completed your goal!"
                      tag="completion"
                      timeout="2000"
                  onClick={event => this.handleCompClick(event)}
              />
              <div>
                      {/* <button onClick={this.handleButtonClick.bind(this)}>Notify!</button> */}
                      {/* {document.title === 'swExample' && <button onClick={this.handleButtonClick2.bind(this)}>swRegistration.getNotifications</button>}
                      <Notification
                      ignore={this.state.ignore && this.state.title !== ''}
                      // notSupported={this.handleNotSupported.bind(this)}
                      // onPermissionGranted={this.handlePermissionGranted.bind(this)}
                      // onPermissionDenied={this.handlePermissionDenied.bind(this)}
                      // onShow={this.handleNotificationOnShow.bind(this)}
                      timeout={5000}
                      title={this.state.title}
                      options={this.state.options}
                      swRegistration={this.props.swRegistration}
                    /> */}
                  </div>
              <div id="thresholdsList">
                  <WordCount parentCallback = {this.handleCallbackOne} />
                  <PageCount parentCallback = {this.handleCallbackTwo}/>
                  <button className="btn btn-success" onClick={this.sendThr}>submit</button>
              </div>
          </div>)
      }
}

export default Thresholds