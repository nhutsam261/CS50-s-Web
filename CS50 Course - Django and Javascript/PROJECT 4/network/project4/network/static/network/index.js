document.addEventListener("DOMContentLoaded", function(){
    document.querySelector('#post-content').value = '';
    document.querySelector("#post-form").addEventListener("submit", new_post);
});


function new_post(event){
    event.preventDefault();

    fetch("/new_post", {
        method: 'POST',
        body: JSON.stringify({
            content: document.querySelector('#post-content').value,
        })
    }).then(response => response.json())
    .then(result => {
        console.log(result);
        if (result.message){
            alert(`${result.message}`);
        }
        else{
            alert(`${result.error}`);
        }
        location.reload();
    })
}





