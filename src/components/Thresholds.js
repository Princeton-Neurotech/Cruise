import React, { useState } from 'react';
import Collapse from 'react-bootstrap/Collapse';
import Button from 'react-bootstrap/Button';
import WordCount from './WordCount';
import PageCount from './PageCount';
import axios from 'axios';
import reportValidity from 'report-validity'
import ReactNotifications from 'react-browser-notifications';
// import {NotificationContainer, NotificationManager} from 'react-notifications';
import toast, { Toaster } from 'react-hot-toast';
import Swal from 'sweetalert2';
import notifications from 'chrome';
window.Swal = Swal;

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
        // do this every 5 min
        setInterval(() => {
            this.sendML()
        }, 300000);

        let form = document.getElementById('fontSettingsList');
        let res = reportValidity(form);
        if (res) {
            axios.post("http://127.0.0.1:3000/api/thr/", { wordCount: this.state.wordCount,
                                                            pageCount: this.state.pageCount })
                .then(res => {
                    console.log(res);
                    console.log(res.data['wordcount']);
                    /*
                    if (!res.ok) {
                        Swal.fire(
                            'Unsuccessful',
                            'Unable to delete selected user. Please contact administrator.',
                            'error'
                        );
                        return;
                    }
                    */
                    Swal.fire({
                        title: 'We expect you to take ' + ((res.data['wordcount'])/60, 2).toFixed(2) + ' minutes',
                        text: "",
                        icon: 'success',
                        confirmButtonColor: '#3085d6',
                        cancelButtonColor: '#d33',
                        confirmButtonText: 'success',
                    })
                })
        }

        setInterval(() => {
            this.checkCompletion()
        }, 5000);
    })

    sendML = (() => {
        axios.get("http://127.0.0.1:3000/api/ml/")
    })

    checkRoadblock() {
        axios.get("http://127.0.0.1:3000/api/roadblock/")
            .then(res => {
                if (res.data[0] == 'True') {
                    console.log("roadblock notifs");
                    this.roadblock_notif();
                    // this.showRoadblockNotifications();
                    this.state.isRoadblock = true;
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
        axios.get("http://127.0.0.1:3000/api/completion/")
            .then(res => {
                if (res.data[0] == 'True') {
                    console.log("completion notifs");
                    this.completion_notif();
                    // this.showCompNotifications();
                    this.state.isCompletion = true;
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
        console.log(childData);
        // this.setState({LineSpace: childData})
        this.state.wordCount = childData;
    }

    handleCallbackTwo = (childData) =>{
        console.log(childData);
        // this.setState({LineSpace: childData})
        this.state.pageCount = childData;
    }

    roadblock_notif() {
        console.log("made roadblock notif");
        chrome.notifications.create('roadblock', {
            type: 'basic',
            iconUrl: 'src/components/sad_whale.jpg',
            title: 'roadblock',
            message: 'You have approached a roadblock!',
            priority: 2
        })
    }

    completion_notif() {
        console.log("made completion notif");
        chrome.notifications.create('completion', {
            type: 'basic',
            iconUrl: 'src/components/happy_whale.jpg',
            title: 'completion',
            message: 'You have completed your goal!',
            priority: 2
        })
    }

    /*
    askNotificationPermission() {
        // function to actually ask the permissions
        function handlePermission(permission) {
          // set the button to shown or hidden, depending on what the user answers
          notificationBtn.style.display =
            Notification.permission === 'granted' ? 'none' : 'block';
        }
      
        // Let's check if the browser supports notifications
        if (!('Notification' in window)) {
          console.log("This browser does not support notifications.");
        } else if (checkNotificationPromise()) {
          Notification.requestPermission().then((permission) => {
            handlePermission(permission);
          });
        } else {
          Notification.requestPermission((permission) => {
            handlePermission(permission);
          });
        }
    }
    completion_img = 'src/components/happy_whale.jpg';
    completion_text = `You have completed your goal!`;
    completion_notification = new Notification('Completion', { body: completion_text, icon: completion_img });
    roadblock_img = 'src/components/sad_whale.jpg';
    roadblock_text = `You have approached a roadblock!`;
    roadblock_notification = new Notification('Roadblock', { body: roadblock_text, icon: roadblock_img });
    
    notify = () => toast('Here is your toast.');

    App = () => {
    return (
        <div>
        <button onClick={notify}>Make me a toast</button>
        <Toaster />
        </div>
    );
    };

    createNotification = (type) => {
        return () => {
          switch (type) {
            case 'info':
              NotificationManager.info('Info message');
              break;
            case 'success':
              NotificationManager.success('Success message', 'Title here');
              break;
            case 'warning':
              NotificationManager.warning('Warning message', 'Close after 3000ms', 3000);
              break;
            case 'error':
              NotificationManager.error('Error message', 'Click me!', 5000, () => {
                alert('callback');
              });
              break;
          }
        };
    };
    */

    // const [open, setOpen] = useState(false);
    render() {
        console.log("notifications")
        return (
            <div className='roadblock_completion_notifs'>
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