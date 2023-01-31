
let searchInput = document.querySelector('#search-input')
let select = document.querySelector('#people-select')

searchInput.addEventListener('input', (e) => {
    let url = `${window.location.origin}/api/peoples/?q=${searchInput.value}`
    
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(result => {
        let html_options = ''

        result.map(e => {
            html_options += `<option value="${ e.pk }">${e['full-name']}</option>`
        })


        select.innerHTML = html_options
    })
    .catch(error => {
        console.log(error)
    })

})


