function getNotification(){
    var req = new XMLHttpRequest();
    var url = "{% url 'notifications' %}";
    req.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200){
            alert(req.responseText);
        } 
    };
    req.open("GET", url, true);
    req.send();
}