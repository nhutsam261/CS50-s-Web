document.addEventListener("DOMContentLoaded", function(){
    document.querySelectorAll('.like-btn').forEach(button => {
        const post_id = button.dataset.post;
        // Check if there is already a vlaue in local storage
        if (!localStorage.getItem(`post-${post_id}-likes`)) {
            // If not, set the counter to 0 in local storage
            localStorage.setItem(`post-${post_id}-likes`, 0);
        }

        document.getElementById(`post-${post_id}-likes`).innerText = localStorage.getItem(`post-${post_id}-likes`);

        button.onclick = function(){
            like_post(this.dataset.post);
        }
    })
});



function like_post(post_id){
    fetch(`/like_post/${post_id}`)
    .then(response => response.json())
    .then(result => {
        console.log(result);
        localStorage.setItem(`post-${post_id}-likes`, result.likes)
        document.getElementById(`post-${post_id}-likes`).innerText = result.likes;
        if (result.liked_state){
            document.getElementById(`like-btn-${post_id}`).classList.remove('btn-outline-primary');
            document.getElementById(`like-btn-${post_id}`).classList.add('btn-primary');
        }
        else{
            document.getElementById(`like-btn-${post_id}`).classList.remove('btn-primary');
            document.getElementById(`like-btn-${post_id}`).classList.add('btn-outline-primary');
        }
    })
}