document.addEventListener("DOMContentLoaded", function(){
    document.querySelector("#compose-form").addEventListener("submit", send_email)
});


function send_email(event){
    event.preventDefault();

    fetch("/emails", {
        method: 'POST',
        body: JSON.stringify({
            recipients: document.querySelector('#compose-recipients').value,
            subject: document.querySelector('#compose-subject').value,
            body:  document.querySelector('#compose-body').value,
        })
    }).then(response => response.json())
    .then(result => {
        console.log(result);
        if (!result.error){
            alert(`${result.message}`);
            load_mailbox("sent");
        }
        else{
            alert(`${result.error}`);
        }
    });
}