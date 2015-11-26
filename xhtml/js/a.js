function show_off_pali(){
    if (document.getElementById("show_off").childNodes[0].nodeValue == "显示巴利经文") {
        document.getElementById("pali").removeAttribute("hidden");
        document.getElementById("show_off").childNodes[0].nodeValue = "不显示巴利经文";
    } else {
        document.getElementById("pali").setAttribute("hidden","hidden");
        document.getElementById("show_off").childNodes[0].nodeValue = "显示巴利经文";
    }
}
