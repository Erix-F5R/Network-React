document.addEventListener('DOMContentLoaded', function () {

   
   var id = window.location.pathname.split('/edit/')[1]
  // Use buttons to toggle between views
  document.querySelector('#save').addEventListener('click', (event) => {
      event.preventDefault()
      save(id)
      
       });

});

function save(post_id){
    var text =  document.querySelector('textarea').value
    
    fetch(`/editor/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({text:text})
    })

    

}