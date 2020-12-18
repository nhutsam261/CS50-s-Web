document.addEventListener("DOMContentLoaded", function(){
    document.getElementById('follow-btn').onclick = function(){
        const profile_id = document.getElementById('follow-btn').dataset.profile;
        follow_unfollow(profile_id);
    }
});



function follow_unfollow(profile_id){
    fetch(`/follow_unfollow/${profile_id}`)
    .then(response => response.json())
    .then(result => {
        console.log(result);
        if (result.following_state){
            document.getElementById(`follow-btn`).innerText = 'Unfollow';
        }
        else{
            document.getElementById(`follow-btn`).innerText = 'Follow';
        }
    })
}