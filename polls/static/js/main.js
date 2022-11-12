$(document).ready(()=>{
  $('#test').trigger('click');
  $('#disable_nav').on('click',()=>{
    $('#nav').show();
  })
  $('#nav_reciper_hidder').on('click',()=>{
    $('#nav_recipe_res_div').hide("fast");
    $('#nav_reciper_show').show("fast");
  })
  $('#nav_reciper_show').on('click',()=>{
    $('#nav_recipe_res_div').show("fast");
    $('#nav_reciper_show').hide("fast");
  })
})

$('.recipe_box_simple').on('click',function(){
  if($(this).siblings('.recipe_box_extended').hasClass('showclass')){
    $(this).siblings('.recipe_box_extended').removeClass('showclass');
  }else{
    $(this).siblings('.recipe_box_extended').addClass('showclass');
  }
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
