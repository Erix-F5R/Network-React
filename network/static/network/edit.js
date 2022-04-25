document.addEventListener('DOMContentLoaded', function () {

   
    
   var id = window.location.pathname.split('/edit/')[1]
  
   // Use buttons to toggle between views
   let save = document.querySelector('#save');
    if(save !== null){
        save.addEventListener('click', (event) => {
      event.preventDefault()
      save(id)
      
       });
    }
    
    //Like Button
    let like = document.querySelectorAll('.like')



    
    if(like.length !== 0){        
        like.forEach( (post) => { 
            let id = post.dataset.id
            GET_likes(post, id)
            post.innerHTML = id
                
        })
    }
   

});

function save(post_id){
    var text =  document.querySelector('textarea').value
    
    fetch(`/editor/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({text:text})
    })

    

}

function GET_likes(post, post_id){


    fetch(`getlikes/${post_id}`)
    .then(response => response.json())
    .then(data => {

        post.innerHTML += `Likes: ${data.count}`

    } )



}