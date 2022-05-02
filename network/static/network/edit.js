document.addEventListener('DOMContentLoaded', function () {


    
   var id = window.location.pathname.split('/edit/')[1]
  
   //
   let save = document.querySelector('#save');
    if(save !== null){
        save.addEventListener('click', (event) => {
      event.preventDefault()
      save(id)
      
       });
    }
    //Number of Likes
    let like = document.querySelectorAll('.like')
    
    if(like.length !== 0){        
        like.forEach( (post) => { 
            let id = post.dataset.id
            GET_likes(post, id)
            post.innerHTML = id
                
        })
    }

    //Like Button
    let like_buttons = document.querySelectorAll('.like-button');
    
    if(like_buttons.length !== 0){

        like_buttons.forEach( (button) =>{

            button.addEventListener('click', (click) => {
                click.preventDefault()
                like_post(click.currentTarget.dataset.id)
            })
        } )

    }
   

});

function save(post_id){
    var text =  document.querySelector('textarea').value
    
    fetch(`/editor/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({text:text})
    })

    

}

function like_post(post_id){

    const csrftoken = getCookie('csrftoken');

    fetch(`postlike/${post_id}`, {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        body: JSON.stringify({
            like: true,
        })
      })
    
}


function GET_likes(post, post_id){


    fetch(`getlikes/${post_id}`)
    .then(response => response.json())
    .then(data => {

        post.innerHTML += `Likes: ${data.count}`

    } )



}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
