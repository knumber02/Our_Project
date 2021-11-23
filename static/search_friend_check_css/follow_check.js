let error_message = document.getElementById("error_message");
let changeBtn = document.getElementById("friend_changeBtn")
function changePage(){
    if (error_message.innerHTML == null) {
    changeBtn.style.display = "block";
    } else if (!!error_message.innerHTML) {
        changeBtn.style.display = "none";
        // console.log(error_message.innerHTML)
        // console.log(error_message)
    } 
}
changePage();
