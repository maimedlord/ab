/*
Answer Bounty
Alex Haas
*/
// function show_login() {
//    document.getElementById('login_form').style.display = "none";
//    document.getElementById('login_text').style.display = "flex";
// }
// function show_login_form() {
//    document.getElementById('login_form').style.display = "flex";
//    document.getElementById('login_text').style.display = "none";
// }
// // // // // // // // // // // // // // // // // // // // // // // // //
function show_display_bought() {
   document.getElementById('display_bought').style.display = "flex";
   document.getElementById('display_sold').style.display = "none";
}
function show_display_sold() {
   document.getElementById('display_bought').style.display = "none";
   document.getElementById('display_sold').style.display = "flex";
}