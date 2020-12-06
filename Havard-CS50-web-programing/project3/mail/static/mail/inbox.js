document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);

    // load inbox by default
    load_mailbox('inbox');
});
// test email
function validateEmail(email) {
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}

function compose_email() {

    // show compose field and other place
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    // reset the form
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
}



function send() {

    var recipients = document.querySelector('#compose-recipients').value;


    var subject = document.querySelector('#compose-subject').value;
    var body = document.querySelector('#compose-body').value;

    // check the recipients is not empty
    if (recipients != '') {
        var mailUsers = recipients.split(', ');

        var validated = true;

        for (id in mailUsers) {
            if (!validateEmail(mailUsers[id])) {

                validated = false;
            }
        }

        // if pass check email format
        if (validated) {
            for (id in mailUsers) {


                fetch('/emails', {
                    method: 'POST',
                    body: JSON.stringify({
                        recipients: mailUsers[id],
                        subject: subject,
                        body: body,
                        status: 1,
                    })
                }).
                then(response => response.json()).
                then(result => {
                    console.log(result)
                    var message = document.querySelector('#message')
                    if (result['error']) {
                        message.innerHTML = `User with ${mailUsers[id]} does not exist.`;
                        message.style.color = 'red';

                    } else {
                        message.innerHTML = 'Email sent successfully.';
                        message.style.color = 'green';
                        load_mailbox('sent');
                    }
                });
            }
        } else {
            var message = document.querySelector('#message');
            message.innerHTML = "Please enter the valid email with end ',' character";
            message.style.color = 'red';
        }
    } else {
        var message = document.querySelector('#message');
        message.innerHTML = 'At least one recipient required.';
        message.style.color = 'red';
    }
}

function load_mailbox(mailbox) {

    var email_view = document.querySelector('#emails-view');
    document.getElementById('emails-view').style.display = 'none';
    document.getElementById('compose-view').style.display = 'none';
    // show the mailbox and hide other views
    email_view.style.display = 'block';
    document.getElementById('compose-view').style.display = 'none';

    // show the mailbox name
    email_view.innerHTML = '';
    email_view.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    //GET request
    fetch(`/emails/${mailbox}`)
        .then(response => response.json())
        .then(emails => {

            if (emails.length == 0) {
                email_view.innerHTML =
                    `<p style = "font-size: large; font-weight: bold;">Your ${mailbox} is empty !!! </p>`;
            } else {
                let n = emails.length;
                for (let index = 0; index < n; index++) {
                    var content = document.createElement("div");
                    var email = document.createElement("div");
                    var writter = document.createElement('div'); // h5
                    var sub = document.createElement('div'); // p 
                    var time = document.createElement('div'); // p
                    var archive_button = document.createElement('div');
                    if (mailbox == 'inbox') {
                        var btn = document.createElement('button');
                        btn.innerText = 'Archive';
                        btn.classList.add('btn-secondary');
                        btn.classList.add('btn');

                        btn.addEventListener('click', () => {

                            fetch(`/emails/${emails[index]['id']}`, {
                                method: 'PUT',
                                body: JSON.stringify({
                                    archived: true
                                })
                            });

                            location.reload();
                            load_mailbox('inbox');
                        });
                    } else if (mailbox == 'archive') {
                        var btn = document.createElement('button');
                        btn.innerText = 'Move To Inbox';
                        btn.classList.add('btn-secondary');
                        btn.classList.add('btn');

                        btn.addEventListener('click', () => {

                            fetch(`/emails/${emails[index]['id']}`, {
                                method: 'PUT',
                                body: JSON.stringify({
                                    archived: false
                                })
                            });

                            location.reload();
                            load_mailbox('inbox');
                        });
                    }

                    email.id = `${emails[index]['id']}`;
                    content.classList.add('row')
                    email.classList.add('row');
                    email.classList.add('col-8')
                    writter.classList.add('col');
                    sub.classList.add('col');
                    time.classList.add('col');
                    if (mailbox === 'sent') {
                        writter.innerHTML = `<h5>To: ${emails[index]['recipients']} </h5>`;
                    } else {
                        writter.innerHTML = `<h5> ${emails[index]['sender']} </h5>`;
                    }

                    if (emails[index]['subject'] == '') {
                        sub.innerHTML = '<p> No Subject </p>';
                    } else {
                        sub.innerHTML = `<p> ${emails[index]['subject']} </p>`;
                    }
                    time.innerHTML = `<p> ${emails[index]['timestamp']} </p>`;

                    email.style.borderStyle = 'solid';
                    email.style.borderColor = 'black';
                    email.style.borderWidth = '0.1rem';
                    email.style.marginBottom = '0.2rem';
                    if (emails[index]['read'] == true) {
                        email.style.backgroundColor = 'white';
                    } else {
                        email.style.backgroundColor = '#A9A9A9';
                    }


                    email.appendChild(writter);
                    email.appendChild(sub);
                    email.appendChild(time);
                    email.addEventListener('click', () => load_email(emails[index]['id']), true);
                    if (mailbox == 'inbox' || mailbox == 'archive') {
                        archive_button.classList.add('col-4')
                        archive_button.appendChild(btn);
                        content.appendChild(email);
                        content.appendChild(archive_button);
                    } else {
                        content.append(email);
                    }


                    //console.log(emails[email]['id'])

                    email_view.appendChild(content);

                }
            }
        });
}



function load_email(id) {

    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    mail_view = document.querySelector('#emails-view');
    mail_view.style.display = 'block';
    console.log(id)

    mail_view.innerHTML = '';

    fetch(`/emails/${id}`)
        .then(response => response.json())
        .then(email => {

            var div = document.createElement('div');

            div.classList.add('container');
            div.classList.add('jumbotron');

            var sub = document.createElement('h5');
            sub.innerHTML = "<b>Subject: </b>" + `${email['subject']}`;

            var sender = document.createElement('h5');
            sender.innerHTML = "<b>From: </b>" + `${email['sender']}`;
            var recipients = document.createElement('h5');
            recipients.innerHTML = "<b>To: </b>" + `${email['recipients']}`;
            var body = document.createElement('p');
            body.innerText = email['body'];
            var time = document.createElement('h5');
            time.innerHTML = "<b>Timestamp: </b>" + `${email['timestamp']}`;

            var hr = document.createElement('hr');
            hr.className = "my-4";

            if (email['read'] == false) {

                fetch(`/emails/${id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        read: true,
                    })
                })


            }


            var archive = email['archived'];

            var btn = document.createElement('button');
            var reply = document.createElement('button');


            if (archive) {
                btn.innerText = 'Unarchive';
            } else {
                btn.innerText = 'Archive';
            }
            reply.innerText = 'Reply';

            //bootstrap sheeyit
            btn.classList.add('btn-primary');
            btn.classList.add('btn');
            reply.classList.add('btn-success');
            reply.classList.add('btn');

            btn.addEventListener('click', () => {

                fetch(`/emails/${id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        archived: !archive
                    })
                });

                location.reload();
                load_mailbox('inbox');
            });


            reply.addEventListener('click', () => {

                //reset value of current compose
                compose_email();
                //setting default values as specified
                document.querySelector('#compose-recipients').value = email['sender'];
                document.querySelector('#compose-body').value = `On ${email['timestamp']}, ${email['sender']} wrote: ${email['body']}`;
                //checking for subject
                console.log(email['subject'].search('Re: '))
                if (email['subject'].search('Re: ') >= 0) {
                    document.querySelector('#compose-subject').value = `${email['subject']}`;
                } else {
                    document.querySelector('#compose-subject').value = `Re: ${email['subject']}`;
                }
            });

            //adding the buttons to our HTML
            div.appendChild(sender);
            div.appendChild(recipients);
            div.appendChild(sub);
            div.appendChild(time);
            console.log(div)
            var divButton = document.createElement('div');

            divButton.appendChild(reply);
            divButton.appendChild(btn);

            divButton.className = 'btn-group';

            div.appendChild(divButton);
            div.appendChild(hr);
            div.appendChild(body);
            mail_view.appendChild(div);


        });
}