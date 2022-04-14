document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#save').addEventListener('click', () => foo());

});

function foo(){
    alert('Foo')
}