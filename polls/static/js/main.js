// console.log("Say hello to my little friend");

// $("#jquery_test").click(() => {
//   console.log("Finally!");
// });

$(document).ready(()=>{
  $('#test').trigger('click');
})

function testfunc(){
  Swal.fire({
    icon: 'error',
    title: 'Oops...',
    text: 'Something went wrong. Try again!',
    showConfirmButton: false,
    timer: 2000
  })
}

//function for hiding navbar
$("#navBtn").on("click",() => {
  document.getElementById("nav").classList.toggle("short");
})

//function for buttons
let btnContainer = document.getElementById("links");
let btns = btnContainer.getElementsByClassName("link");

for (let i = 0; i < btns.length; i++) {
  btns[i].addEventListener("click", function() {
    let current = document.getElementsByClassName("active");

    if (current.length > 0) {
      current[0].className = current[0].className.replace(" active", "");
    }

    this.className += " active";
  });
}
