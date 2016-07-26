function show_off(){

    if (document.getElementById('main').getAttribute('hidden') == null) {

        document.getElementById('main').setAttribute('hidden', 'hidden')

        document.getElementById('pali').removeAttribute('hidden')
        document.getElementById('chinese').removeAttribute('hidden')

    } else {

        document.getElementById('main').removeAttribute('hidden')

        document.getElementById('pali').setAttribute('hidden', 'hidden')
        document.getElementById('chinese').setAttribute('hidden', 'hidden')

    }
}
