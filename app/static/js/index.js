// ctrl + F5 if error 304 appear


window.onpageshow = function(event) {
    if (event.persisted) {
        window.location.reload() 
    }
};