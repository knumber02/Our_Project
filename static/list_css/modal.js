let openBtn = document.getElementById('openBtn');
let closeBtn = document.getElementById('closeBtn');
let modal = document.getElementById('modal');
let registerBtn = document.getElementById("registerBtn")

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

// changeBtn.addEventListener("click", function(){
//   modal.style.display = "none";
// })

