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

//helper
$('.nav_recipe_helper').on('click',function(){
  Swal.fire({
    title: '<strong>Results explanation</strong>',
    icon: 'info',
    html:
      '<p>On the right side of the recipe name is colored block that determines difficulty level of recipe:</p>' +
      '<p><span style="color:green;">green</span> - easy , <span style="color:yellow";>yellow</span> - medium , <span style="color:red";>red</span> - hard</p>' +
      '<ul>'+
      '<li class="result_helper_li"><div class="verificated_helper_img"></div><div class="img_info">Tells if recipe was accepted by moderators</div></li>'+
      '<li class="result_helper_li"><div class="spicy_helper_img"></div><div class="img_info">Tells about spiciness of recipe</div></li>'+
      '<li class="result_helper_li"><ul>'+
      '<li class="result_helper_li"><span style="color:green;">green</span> - mild , <span style="color:yellow";>yellow</span> - slightly spicy</li>'+
      '<li class="result_helper_li"><span style="color:orange";>orange</span> - medium spicy , <span style="color:red";>red</span> - very spicy</li>'+
      '</ul></li>'+
      '<li class="result_helper_li"><div class="time_img"></div><div class="img_info">Tells about time prepare time of recipe</div></li>'+
      '<li class="result_helper_li"><div class="people_img"></div><div class="img_info">Tells how many portion you receive</div></li>'+
      '<li class="result_helper_li"><div class="cuisine_img"></div><div class="img_info">Tells about cuisine origin of that recipe</div></li>'+
      '</ul>',
    showCloseButton: true,
    showCancelButton: false,
    showConfirmButton: false,
    focusConfirm: false,
  })
})