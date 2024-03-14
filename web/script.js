function sendData() {
    var inputField = document.getElementById('inputField');
    var inputValue = inputField.value;
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/submit?data=" + encodeURIComponent(inputValue), true);
    xhr.send();
    console.log("Data sent");
}
function addKey(key){
    var inputField = document.getElementById("inputField")
    inputField.value += key
    console.log("Added key: " + key);
}
function uploadFile() {
    var fileInput = document.getElementById('fileInput');
    var inputField = document.getElementById('inputField');
    if (!fileInput.files || fileInput.files.length === 0) {
        alert('Please select a file.');
        return;
    }
    var file = fileInput.files[0];
    var reader = new FileReader();
    reader.onload = function(event) {
        var content = event.target.result;

        inputField.value = content;
    
    };
    reader.readAsText(file);
}

function download(data, filename, type){
    var file = new Blob([data], {type: type});
    if (window.navigator.msSaveOrOpenBlob){
        window.navigator.msSaveOrOpenBlob(file, filename)
    }else{
        var a = document.createElement("a"),
            url = URL.createObjectURL(file);
        a.href = url;
        a.download = filename;
        document.body.appendChild(a)
        a.click();
        setTimeout(function() {
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);

        }, 0);
    }
}

function downloadFile(){
    var inputField = document.getElementById("inputField")
    download(inputField.value, "payload.dd", "text/plain")
}