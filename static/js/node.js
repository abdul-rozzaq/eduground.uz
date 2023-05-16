let openButtons = document.querySelectorAll('.open-modal')
let modals = document.querySelectorAll('.back')
let closeButtons = document.querySelectorAll('.close')

window.addEventListener('click', function (event) {
    if (event.target.getAttribute('class') != null && event.target.getAttribute('class').includes('back')) {
        for (let w of modals) {
            w.classList.add('d-none')
            w.classList.remove('showAnim')
        }
    }
})

for (let x of openButtons) {
    console.log(x);
    x.addEventListener('click', (e) => {
        for (let y of modals) {
            if (x.getAttribute('data-modal-id') == y.getAttribute('data-modal-name')) {
                y.classList.remove('d-none')
                y.classList.add('showAnim')
            }
        }
    })
}


for (let z of closeButtons) {
    z.addEventListener('click', (e) => {
        for (let w of modals) {
            if (z.getAttribute('data-modal-id') == w.getAttribute('data-modal-name')) {
                w.classList.add('d-none')
                w.classList.remove('showAnim')
            }
        }
    })
}