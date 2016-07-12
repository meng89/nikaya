
var button_text = '显示/关闭巴利经文及原始译文'

function is_show(){
    if (document.getElementById('pali').getAttribute('hidden') != null) {
        return true
    } else {
        return false
    }
}

function show_off(){
    if (is_show) {
        document.getElementById('pali').removeAttribute('hidden')
        document.getElementById('head').removeAttribute('hidden')
        is_show = false
    } else {
        document.getElementById('pali').setAttribute('hidden', 'hidden')
        document.getElementById('head').setAttribute('hidden', 'hidden')
        is_show = true
    }
}