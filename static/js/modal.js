

let open = $('#open-modal')
let close = $('#close')

let modal = $('#modal')

open.click(() => {
    modal.removeClass('d-none')
    modal.addClass('showAnim')
})

close.click(()=>{
    modal.removeClass('showAnim')
    modal.addClass('d-none')
})

let _open = $('#open-modal-add-people')
let _close = $('#close-add-people')

let _modal = $('#modal-add-people')

if (_open != null && _close != null && _modal != null) {
    _open.click(function() {
        _modal.removeClass('d-none')
        _modal.addClass('showAnim')
    })

    _close.click(function() {
        _modal.removeClass('showAnim')
        _modal.addClass('d-none')
    })
}
