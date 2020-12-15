function post() {
    var description = document.querySelector('#description').value;
    console.log(description)
    fetch('/post', {
        method: 'PUT',
        body: JSON.stringify({
            description: description,
        })
    }).
    then(response => response.json()).
    then(result => {
        var message = document.querySelector('#message');
        if (result['error']) {
            message.innerHTML = "Can't post the post"
            message.style.color = 'red';
        }
    });

}

function follow_click() {
    var button_follow = document.querySelector('#follow_button');
    var value_follow = button_follow.value;
    if (value_follow == 'Follow') {
        button_follow.value = 'UnFollow';
    } else {
        button_follow.value = 'Follow';
    }
}

function post_comment(post_id) {
    var content = document.querySelector(`#cmt_content_${post_id}`).value;
    console.log(content);
    fetch(`/comments/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            content: content,
        })
    }).
    then(response => response.json()).
    then(result => {
        var message = document.querySelector('#message');
        if (result['error']) {
            message.innerHTML = "Can't comments"
            message.style.color = 'red';
        }
    });

}

function list_comments(post_id) {
    var list_of_comments = document.querySelector(`#cmts_${post_id}`);
    if (list_of_comments.innerHTML == '') {
        list_of_comments.style.display = '';
        console.log('debug is here!');
    } else {
        list_of_comments.innerHTML = '';
        list_of_comments.style.display = 'none';
        return;
    }
    fetch(`/comments/${post_id}`).
    then(response => response.json()).
    then(comments => {
        let n = comments.length;
        var hr = document.createElement('hr')
        list_of_comments.appendChild(hr);
        var comment_textarea = document.createElement('div');
        comment_textarea.innerHTML = `
        <form class="row" id="new_form">

        <textarea class="comment_description" id="cmt_content_${post_id}" placeholder="Write your comment"></textarea>
        <input onclick="post_comment(${post_id})" type="submit" value="Submit" class="btn btn-primary">
    </form>`;

        list_of_comments.appendChild(comment_textarea);
        if (n == 0) {
            document.querySelector(`#cmts_${post_id}`).innerHTML = '<hr> <p> NO COMMENTS </p>';
        } else {
            console.log('log in there');



            for (let i = 0; i < n; i++) {
                var comment = document.createElement('div');
                comment.classList.add('comment_field');
                comment.innerHTML = `<h5> ${comments[i]['user']}</h5>
                <p class='comment_content'> ${comments[i]['content']} </p>
                <p> ${comments[i]['date_commented']} </p>
                `;
                list_of_comments.appendChild(comment);
            }
        }
    });
}

function post_edit(post_id) {
    var description = document.querySelector(`#content_${post_id}`).value;
    console.log(description);
    fetch(`/edit/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            description: description,
        })
    }).
    then(response => response.json()).
    then(result => {
        var message = document.querySelector('#message');
        if (result['error']) {
            message.innerHTML = "Can't post the post"
            message.style.color = 'red';
        }
    });

}

function edit(post_id) {
    var content = document.querySelector(`#d_${post_id}`);
    var childContent = content.children[0];

    content.innerHTML = `<form id="new_form">

    <textarea class="form-control" id="content_${post_id}">${childContent.innerHTML}</textarea>
    <input onclick="post_edit(${post_id})" type="submit" value="Save" class="btn btn-primary">
</form>`;


    document.getElementById(`btn-gr-${post_id}`).style.display = 'none';
}

function like(post_id) {

    var like_button = document.querySelector(`#like_button${post_id}`);
    let numOflike = document.querySelector(`#numOfLike${post_id}`).innerHTML;

    //console.log(post_id)
    if (like_button.classList[1] == "fa-heart-o") {
        document.querySelector(`#like_button${post_id}`).className = 'fa fa-heart';
        numOflike++;
        fetch(`/like/${post_id}`, {
            method: 'PUT',
            body: JSON.stringify({
                liked: false,
            })
        }).
        then(response => response.json()).
        then(result => {
            var message = document.querySelector('#message');
            if (result['error']) {
                message.innerHTML = `ERROR`;
                message.style.color = 'red';
            }
            /*else {
                document.querySelector(`#like_button${post_id}`).className = 'fa fa-heart';
                numOflike++;
            }*/
        });
    } else {
        document.querySelector(`#like_button${post_id}`).className = 'fa fa-heart-o';
        numOflike--;
        fetch(`/like/${post_id}`, {
            method: 'PUT',
            body: JSON.stringify({
                liked: true,
            })
        }).
        then(response => response.json()).
        then(result => {
            var message = document.querySelector('#message');
            if (result['error']) {
                message.innerHTML = `ERROR`;
                message.style.color = 'red';
            }
            /*else {
                document.querySelector(`#like_button${post_id}`).className = 'fa fa-heart-o';
                numOflike--;
            }*/
        });
    }
    //console.log(numOflike);
    document.querySelector(`#numOfLike${post_id}`).innerHTML = numOflike;
}