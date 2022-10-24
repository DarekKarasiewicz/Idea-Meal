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
