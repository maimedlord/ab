/*
Answer Bounty
Alex Haas
*/
function choose_a_lostudy_g() {
   document.getElementById('s_l_graduate').style.borderStyle = "dotted";
   document.getElementById('s_l_h_school').style.borderStyle = "none";
}
function choose_a_lostudy_hs() {
   document.getElementById('s_l_graduate').style.borderStyle = "none";
   document.getElementById('s_l_h_school').style.borderStyle = "dotted";
   document.getElementById('s_l_undergraduate').style.borderStyle = "none";
}
function choose_a_lostudy_u() {
   document.getElementById('s_l_graduate').style.borderStyle = "none";
   document.getElementById('s_l_h_school').style.borderStyle = "none";
   document.getElementById('s_l_undergraduate').style.borderStyle = "dotted";
}
// // // // // // // // // // // // // // //
let contract_type = "assignment"
// INCOMPLETE:
function show_type_assignment() {
   contract_type = "assignment"
   document.getElementById('d_t_assignment').style.display = "flex";
   document.getElementById('d_t_test').style.display = "none";
}
// INCOMPLETE:
function show_type_test() {
   contract_type = "test"
   document.getElementById('d_t_assignment').style.display = "none";
   document.getElementById('d_t_test').style.display = "flex";
}