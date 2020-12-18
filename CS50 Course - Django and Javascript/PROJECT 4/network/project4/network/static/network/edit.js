document.addEventListener("DOMContentLoaded", function(){
    document.querySelectorAll('.edit-link').forEach(link => {
        link.onclick = function(){
            const post_id = this.dataset.post;
            edit_handler(post_id); 
            document.getElementById('save-btn').onclick = function(){
                edit(post_id);
            }
            
        }
    })
});



function edit_handler(post_id){
    document.querySelector('.container').style.display = 'none';
    document.querySelector('.edit-container').style.display = 'block';

    fetch(`/post/${post_id}`)
    .then(response => response.json())
    .then(post => {
        console.log(post);
        document.getElementById('edit-content').value = post.content;
    })    
    
}


function edit(post_id){
    fetch(`/post/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            'content': document.getElementById('edit-content').value
        })
    });
    document.querySelector('.container').style.display = 'block';
    document.querySelector('.edit-container').style.display = 'none';
    

}