let searchInput = document.querySelector('#search-input'),
    select = document.querySelector('#people-select'),
    groupSelect = document.querySelector('#group-select')


function updateGroupSelect() {
    let url = `${window.location.origin}/api/groups/?id=${select.value}`
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
            html_options += `<option value='${ e.pk }'>${e['name']}</option>`
        })


        groupSelect.innerHTML = html_options


    })
    .catch(error => {
        console.log(error)
    })


}


searchInput.addEventListener('input', (e) => {
    let getPeopleUrl = `${window.location.origin}/api/peoples/?q=${searchInput.value}`


        fetch(getPeopleUrl, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(result => {
            let html_options = ''

            result.map(e => {
                html_options += `<option value='${ e.pk }'>${e['full-name']}</option>`
            })


            select.innerHTML = html_options

            updateGroupSelect()

        })
        .catch(error => {
            console.log(error)
        })

})

select.addEventListener('change', () => {updateGroupSelect()})