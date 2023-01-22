

let open = document.querySelector('#open-modal')
let close = document.querySelector('#close')

let modal = document.querySelector('#modal')


open.addEventListener('click', function() {
    modal.classList.remove('d-none')
    modal.classList.add('showAnim')
})


close.addEventListener('click', function() {
    modal.classList.remove('showAnim')
    modal.classList.add('d-none')
})

// update-modal
let close_update_model = document.querySelector('#close-update-model')
let update_modal = document.querySelector('#update-modal')

close_update_model.addEventListener('click', function() {
    update_modal.classList.remove('showAnim')
    update_modal.classList.add('d-none')
})

function openUpdateModal(data) {
    update_modal.classList.remove('d-none')
    update_modal.classList.add('showAnim')

    document.getElementById('id').value=data['id']
    document.getElementById('fish-input').value=data['full_name']
    document.getElementById('birthday-input').value=data['birthday']
    document.getElementById('phone-input').value=data['phone']
}
// delete-modal 

let close_delete_model = document.querySelector('#close-delete-model'),
    close_delete_model2 = document.querySelector('#back-button'),
    delete_modal = document.querySelector('#delete-modal')

close_delete_model.addEventListener('click', function() {
    delete_modal.classList.remove('showAnim')
    delete_modal.classList.add('d-none')
})


close_delete_model2.addEventListener('click', function() {
    delete_modal.classList.remove('showAnim')
    delete_modal.classList.add('d-none')
})

function openDeleteModal(data) {
    delete_modal.classList.remove('d-none')
    delete_modal.classList.add('showAnim')
    
    document.getElementById('fn-delete').textContent=data['full_name']

    document.getElementById('url').href = `${window.location.origin}/delete-people/?id=${data['id']}`
}


