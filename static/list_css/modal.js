let openBtn = document.getElementById('openBtn');
let closeBtn = document.getElementById('closeBtn');
let modal = document.getElementById('modal');
let registerBtn = document.getElementById("registerBtn")
// let friend_modal = document.getElementById("friend_modal")
// let changeBtn = document.getElementById("changeBtn")
// let friend_closeBtn = document.getElementById("friend_closeBtn")
// let friend_changeBtn = document.getElementById("friend_changeBtn")
openBtn.addEventListener('click', function(){
    modal.style.display = 'block';
})
closeBtn.addEventListener('click', function(){
    modal.style.display = 'none';
})
// 背景クリックで非表示（modalというidの部分がクリックされたら、display:noneになる）
addEventListener('click', function(close_bg){
   if(close_bg.target === modal){
     modal.style.display = 'none';
   }
})
// registerBtn.addEventListener("click", function(){
//     friend_modal.style.display = 'block';
// })
changeBtn.addEventListener("click", function(){
  modal.style.display = "none";
})
// friend_closeBtn.addEventListener("click", function(){
//   friend_modal.style.display = 'none';
// })
// // 背景クリックで非表示（modalというidの部分がクリックされたら、display:noneになる）
// addEventListener('click', function(close_bg){
//   if(close_bg.target === friend_modal){
//     friend_modal.style.display = 'none';
//   }
// })
// friend_changeBtn.addEventListener("click", function(){
//   friend_modal.style.display = "none";
// })