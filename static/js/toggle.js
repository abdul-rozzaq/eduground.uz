
let buttons = document.querySelectorAll('.list-button')
let pages = document.querySelectorAll('._page')

let ids = {
    0: 1,
    1: 0
}

for (let i = 0; i < buttons.length; i++) {
    const e = buttons[i];
    

    e.addEventListener('click', ()=>{
        if (!e.classList.contains('active')){
            e.classList.add('active')
            pages[i].classList.remove('d-none')

            buttons[ids[i]].classList.remove('active')
            pages[ids[i]].classList.add('d-none')
        }

    })
}