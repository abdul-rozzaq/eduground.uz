window.addEventListener('DOMContentLoaded', ()=>{
    let loader = document.querySelector('.loader-back')
    console.log(loader);

    setTimeout(()=>{
        loader.style.display = 'none'
    }, 1000)
})