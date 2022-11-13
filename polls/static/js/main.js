$(document).ready(()=>{
  $('#error_trigger').trigger('click');

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

function errorMessage(){
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
$('.navbar__toggle_btn').on('click',function(){
  if($('#nav').hasClass('short')){
    $('.switch-box_wrapper').hide();
  }else{
    $('.switch-box_wrapper').show();
  }
})

//theme switcher controller
$('#theme_switcher').on('change',function(){
  if($(this).find('input').is(':checked')){
    $('#checkbox_sun').hide('fast');
    $('#checkbox_moon').show('fast');
    console.log('checked true');
  }else{
    $('#checkbox_moon').hide('fast');
    $('#checkbox_sun').show('fast');
    console.log('checked false');
  }
})