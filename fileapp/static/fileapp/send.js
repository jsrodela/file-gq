let form = document.querySelector('form')
let send = document.querySelector('.send_to_cloud')

send.addEventListener('click', function(event) {
  form.submit()
})