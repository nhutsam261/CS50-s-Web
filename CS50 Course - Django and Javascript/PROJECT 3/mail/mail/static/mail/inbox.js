document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));

  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));

  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});


function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}


function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  if (document.getElementById('show-email')){
    document.getElementById('show-email').remove()}


  // Empty the table 
  const t = document.querySelector('#emails-view').getElementsByTagName('table')[0];
  if (t){
    document.querySelector("#emails-view").removeChild(t);
  }

  // Show the mailbox name
  // document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  document.getElementById("mailbox-header").innerHTML = `${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}`

  fetch(`/emails/${mailbox}`).then(response => response.json())
  .then(emails => {
    var table = document.createElement("table");
    table.classList.add("table", "table-hover");

    emails.forEach(element => {
      // var table = document.getElementById("mails-table").getElementsByTagName("tbody")[0];
      
      var row = document.createElement("tr");
      if (element.read){row.className = "read"} else {row.className = "unread"};
    
      var cell1 = row.insertCell(0);
      var cell2 = row.insertCell(1);
      var cell3 = row.insertCell(2);
      cell1.className = "col-4";
      cell2.className = "col-4";
      cell3.className = "col-4";
      
      var text1 = document.createTextNode(element.recipients);
      var text2 = document.createTextNode(element.subject);
      var text3 = document.createTextNode(element.timestamp);

      cell1.appendChild(text1);
      cell2.appendChild(text2);
      cell3.appendChild(text3);

      table.appendChild(row);
      document.querySelector("#emails-view").appendChild(table);
      row.addEventListener('click', () => load_email(`${element.id}`, `${mailbox}`));
    });
    
  })
}


function load_email(mail_id, mailbox){
  document.querySelector('#emails-view').getElementsByTagName('table')[0].style.display = "none";

  fetch(`emails/${mail_id}`)
  .then(response => response.json())
  .then(email => {
    // print email
    var email_content = document.createElement("div");
    email_content.id = "show-email";
    email_content.className = "card";
    email_content.innerHTML = `<div class="card-body" style="white-space: pre-wrap;">
    Sender: ${email.sender}
    Recipients: ${email.recipients}
    Subject: ${email.subject}
    Time: ${email.timestamp}<hr>
    ${email.body}
        </div>`;
    
    document.querySelector('#emails-view').appendChild(email_content);

    if (email.read == false){
      fetch(`/emails/${mail_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      });
    }

    var btn_group = document.createElement('div');
    btn_group.className = "ml-4 mb-3";

    var reply_btn = document.createElement('button');
    reply_btn.className = "btn btn-primary";
    reply_btn.innerText = "Reply";
    reply_btn.addEventListener('click', () => {
      reply_mail(email.sender, email.subject, email.body, email.timestamp);
    });

    if (mailbox != 'sent'){
      var archive_btn = document.createElement('button');
      archive_btn.className = "btn btn-primary ml-2";
      if (email.archived){archive_btn.innerText = "Unarchive"} else {archive_btn.innerText = "Archive"}
      archive_btn.addEventListener('click', () => {
        archive_email(mail_id, email.archived);
        document.querySelector('#inbox').click();  
      });
    }

    btn_group.appendChild(reply_btn);
    if (mailbox != 'sent') {btn_group.appendChild(archive_btn)}
    document.querySelector('#show-email').appendChild(btn_group);

  })
}


function reply_mail(sender, subject, body, timestamp){
  compose_email();

  document.querySelector('#compose-recipients').value = sender;

  if (subject.search('Re:') == -1){
    document.querySelector('#compose-subject').value = `Re: ${subject}`;
  }

  document.querySelector('#compose-body').value = `On ${timestamp}, ${sender} wrote:\n${body}\n\n`;
}


function archive_email(email_id, archive_state){
  fetch(`emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: !archive_state
    })
  });
}

