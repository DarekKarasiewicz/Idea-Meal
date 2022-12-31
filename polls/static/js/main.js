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

function comment_section_toggle(){
  $("#recipe_comment_section").toggle("fast");
  if($('#comments_display_btn').css('left') == '0px'){
    $('#comments_display_btn').css('left','300px');
  }else{
    $('#comments_display_btn').css('left','0px');
  }
}

function all_recipes_filter_section_toggle(){
  $("#all_recipe_filters_section").toggle("fast");
  if($('#all_recipe_filters_display_btn').css('left') == '0px'){
    $('#all_recipe_filters_display_btn').css('left','300px');
  }else{
    $('#all_recipe_filters_display_btn').css('left','0px');
  }
}

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
})

const navBtn = document.querySelector('.navbar__toggle_btn');
const navbar = document.getElementById("nav");
let navOpen = false;

navBtn.addEventListener('click',() => {
  if(!navOpen){
    navBtn.classList.add("open")
    navbar.classList.add("short");
    navOpen = true;
  }else{
    navBtn.classList.remove('open');
    navbar.classList.remove("short");
    navOpen = false;
  }
})

//if given element even exists
if ($('.links').length > 0) {
  //function for buttons
  let btnContainer = document.getElementById("links");
  let btns = btnContainer.getElementsByClassName("link");

  for (let i = 0; i < btns.length; i++) {
    btns[i].addEventListener("click", function() {
      let current = document.getElementsByClassName("active");

      if (current.length > 0) {
        current[0].className = current[0].className.replace(" active", "");
      }
    })}
  }
$("#gear-btn").on("click",() => {
  document.getElementById("user_panel").classList.toggle("open");
  document.getElementById("blank_space").classList.toggle("open");
  document.getElementById("sun").classList.toggle("open");
  document.getElementById("moon").classList.toggle("open");
})

//recipe tools button function
function openTools(id){
  document.getElementById("recipe_update"+id).classList.toggle("open");
}

$('.navbar__toggle_btn').on('click',function(){
  if($('#nav').hasClass('short')){
    $('.switch-box_wrapper').hide();
  }else{
    $('.switch-box_wrapper').show();
  }
})


//theme switcher controller
$(document).ready(function(){
  if(localStorage.getItem('current_theme') == 'dark'){
    $('html').attr('data-theme', 'dark')
    $("#theme_switcher").find('input').prop("checked",true);
    $('#checkbox_sun').hide('fast');
    $('#checkbox_moon').show('fast');
  }else{
    $('html').attr('data-theme', 'light');
    $('#checkbox_moon').hide('fast');
    $('#checkbox_sun').show('fast');
  }
})
  $('#theme_switcher').on('change',function(){
    if($('html').attr('data-theme') == 'dark'){
      localStorage.setItem('current_theme', 'light');
      $('#checkbox_moon').hide('fast');
      $('#checkbox_sun').show('fast');
      $('html').attr('data-theme', 'light');
    }else{
      localStorage.setItem('current_theme', 'dark');
      $('#checkbox_sun').hide('fast');
      $('#checkbox_moon').show('fast');
      $('html').attr('data-theme', 'dark');
    }
  })

//main page helper
$('.nav_recipe_helper').on('click',function(){
  Swal.fire({
    title: '<strong>Results explanation</strong>',
    icon: 'info',
    html:
      '<div id="nav_helper_color">'+
      '<p>On the right side of the recipe name is colored block that determines difficulty level of recipe:</p>' +
      '<p class="text_visibility"><span style="color:green;">green</span> - easy , <span style="color:yellow;";>yellow</span> - medium , <span style="color:red";>red</span> - hard</p>' +
      '<ul>'+
      '<li class="result_helper_li"><div class="verificated_helper_img"></div><div class="img_info">Tells if recipe was accepted by moderators</div></li>'+
      '<li class="result_helper_li"><div class="spicy_helper_img"></div><div class="img_info">Tells about spiciness of recipe</div></li>'+
      '<li class="result_helper_li"><ul>'+
      '<li class="result_helper_li text_visibility"><span style="color:green;">green</span> - mild , <span style="color:yellow; text-shadow: 0 0 1px black, 0 0 1px black;";>yellow</span> - slightly spicy</li>'+
      '<li class="result_helper_li text_visibility"><span style="color:orange";>orange</span> - medium spicy , <span style="color:red";>red</span> - very spicy</li>'+
      '</ul></li>'+
      '<li class="result_helper_li"><div class="time_img"></div><div class="img_info">Tells about time prepare time of recipe</div></li>'+
      '<li class="result_helper_li"><div class="people_img"></div><div class="img_info">Tells how many portion you receive</div></li>'+
      '<li class="result_helper_li"><div class="cuisine_img"></div><div class="img_info">Tells about cuisine origin of that recipe</div></li>'+
      '</ul>'+
      '<div>',
    showCloseButton: true,
    showCancelButton: false,
    showConfirmButton: false,
    focusConfirm: false,
  })
})

