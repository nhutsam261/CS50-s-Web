import React from 'react';
import { connect } from 'react-redux';
import Hoc from '../hoc/hoc';
import axios from 'axios';


class Profile extends React.Component {

    state = {
        profile:  [],
    }


    get_profile = (token, username) => {
        axios.defaults.headers = {
            "Content-Type": "application/json",
            Authorization: `Token ${token}`
        };
        axios.get(`http://127.0.0.1:8000/profile/?username=${username}`)
        .then(res => {
            // console.log(res.data);
            this.setState({ profile: res.data })
        });
    }


    componentWillReceiveProps(newProps) {
        if (newProps.token !== null && newProps.username !== null) {
            this.get_profile(newProps.token, newProps.username);
        }
    }

    render() {
        const user_profile = this.state.profile.map(p => {
            console.log(p.image)
            return (
                <Hoc key>
                    <img src={p.image} alt="" />
                    <p>{p.username}</p>
                </Hoc>
            )
        })



        return (
            <div className="contact-profile">
            {
                this.props.username !== null ?

                // <Hoc>
                //     <img src="http://emilcarlsson.se/assets/harveyspecter.png" alt="" />
                //     <p>{this.props.username}</p>
                //     <div className="social-media">
                //     <i className="fa fa-facebook" aria-hidden="true"></i>
                //     <i className="fa fa-twitter" aria-hidden="true"></i>
                //     <i className="fa fa-instagram" aria-hidden="true"></i>
                //     </div>
                // </Hoc>
                user_profile
                :

                null
            }
            </div>
        )
    }
}



const mapStateToProps = state => {
    return {
        token: state.token,
        username: state.username
    }
}
    
export default connect(mapStateToProps)(Profile);