/*
Answer Bounty
Alex Haas
*/
$(document).ready(function () {
   $('#c_form').click(function () {
      if ($('#c_f_lostudy')[0].value == 'none') {
         document.getElementById('popup_div_lostudy').style.display = 'flex';
      }
      if ($('#c_f_type')[0].value == 'none') {
         document.getElementById('popup_div_type').style.display = 'flex';
      }
      if ($('#c_f_lostudy')[0].value != 'none' && $('#c_f_type')[0].value != 'none') {
         document.getElementById('container_the_rest').style.display = 'flex';
      }
   });
   $('#c_f_s_l_main').click(function () {
      document.getElementById('popup_div_lostudy').style.display = 'none';
   });
   $('#c_f_s_t_main').click(function () {
      document.getElementById('popup_div_type').style.display = 'none';
   });
   $('#c_f_egbonus').change(function () {
      if (document.getElementById('c_f_egbonus').value > 0) {
         document.getElementById('grade_wait_no').checked = false;
         document.getElementById('grade_wait_yes').checked = true;
      }
   });
   $('#grade_wait_no').click(function () {
      document.getElementById('c_f_egbonus').value = '0.0';
   });
});

// lostudy
function choose_lostudy_g() {
   // document.getElementById('c_f_s_l_graduate').style.borderStyle = "dotted";
   // document.getElementById('c_f_s_l_h_school').style.borderStyle = "none";
   // document.getElementById('c_f_s_l_undergraduate').style.borderStyle = "none";
   // document.getElementById('c_f_s_l_main').style.borderStyle = "none";
   document.forms['c_form']['c_f_lostudy'].value = "graduate";
}
function choose_lostudy_hs() {
   // document.getElementById('c_f_s_l_graduate').style.borderStyle = "none";
   // document.getElementById('c_f_s_l_h_school').style.borderStyle = "dotted";
   // document.getElementById('c_f_s_l_undergraduate').style.borderStyle = "none";
   // document.getElementById('c_f_s_l_main').style.borderStyle = "none";
   document.forms['c_form']['c_f_lostudy'].value = "high school";
}
function choose_lostudy_u() {
   // document.getElementById('c_f_s_l_graduate').style.borderStyle = "none";
   // document.getElementById('c_f_s_l_h_school').style.borderStyle = "none";
   // document.getElementById('c_f_s_l_undergraduate').style.borderStyle = "dotted";
   // document.getElementById('c_f_s_l_main').style.borderStyle = "none";
   document.forms['c_form']['c_f_lostudy'].value = "undergraduate";
}
// type
function choose_type_a() {
   // document.getElementById('c_f_s_t_assignment').style.borderStyle = "dotted";
   // document.getElementById('c_f_s_t_test').style.borderStyle = "none";
   // document.getElementById('div_e_f_bonus').style.display = "flex";
   // document.getElementById('c_f_s_t_main').style.borderStyle = "none";
   document.getElementById('c_f_type').value = "assignment";
   document.getElementById('c_f_t_a_deadline').required = true
   document.getElementById('c_f_t_a_d_time').required = true
   document.getElementById('c_f_t_t_start').required = false;
   document.getElementById('c_f_t_t_s_time').required = false;
   document.getElementById('c_f_t_t_end').required = false;
   document.getElementById('c_f_t_t_e_time').required = false;

   // all ***
   var all_arr = document.getElementsByClassName('all');
   for (var i=0; i < all_arr.length; i++){
      all_arr[i].style.display = "flex";
   }
   var a_arr = document.getElementsByClassName('aonly');
   for (var i=0; i < a_arr.length; i++){
      a_arr[i].style.display = "flex";
   }
   var t_arr = document.getElementsByClassName('tonly');
   for (var i=0; i < t_arr.length; i++){
      t_arr[i].style.display = "none";
   }
}
function choose_type_t() {
   // document.getElementById('c_f_s_t_assignment').style.borderStyle = "none";
   // document.getElementById('c_f_s_t_test').style.borderStyle = "dotted";
   // document.getElementById('div_e_f_bonus').style.display = "none";
   // document.getElementById('c_f_s_t_main').style.borderStyle = "none";
   document.getElementById('c_f_type').value = "test"
   document.getElementById('c_f_t_a_deadline').required = false
   document.getElementById('c_f_t_a_d_time').required = false
   document.getElementById('c_f_t_t_start').required = true
   document.getElementById('c_f_t_t_s_time').required = true
   document.getElementById('c_f_t_t_end').required = true
   document.getElementById('c_f_t_t_e_time').required = true
   // all ***
   var all_arr = document.getElementsByClassName('all');
   for (var i=0; i < all_arr.length; i++){
      all_arr[i].style.display = "flex";
   }
   var a_arr = document.getElementsByClassName('aonly');
   for (var i=0; i < a_arr.length; i++){
      a_arr[i].style.display = "none";
   }
   var t_arr = document.getElementsByClassName('tonly');
   for (var i=0; i < t_arr.length; i++){
      t_arr[i].style.display = "flex";
   }
}
// // // // // // // // // // // // // // //
// let contract_type = "assignment"
// // INCOMPLETE:
// function show_type_assignment() {
//    contract_type = "assignment"
//    document.getElementById('d_t_assignment').style.display = "flex";
//    document.getElementById('d_t_test').style.display = "none";
//    document.forms['c_form']['c_f_type'].value = "assignment";
// }
// // INCOMPLETE:
// function show_type_test() {
//    contract_type = "test"
//    document.getElementById('d_t_assignment').style.display = "none";
//    document.getElementById('d_t_test').style.display = "flex";
//    document.forms['c_form']['c_f_type'].value = "test";
// }