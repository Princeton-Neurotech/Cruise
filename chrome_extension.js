var bgl1;
bgl1 = document.getElementsByClassName("kix-page");
function flashRed() {
    bgl1.forEach.call(els,function(el){
        el.style = "overflow-x: auto; background-color: rgb(80, 0, 0); height: 500px; cursor: auto; touch-action: pan-x pan-y;"});}
function flashGrey() {
bgl1[0].style = "overflow-x: auto; background-color: rgb(0, 0, 0); height: 500px; cursor: auto; touch-action: pan-x pan-y;"}

for(let i = 0; i < 1000; i+=2) {
setTimeout(flashRed, 40*(i))
setTimeout(flashGrey, 40*(i+1))
}