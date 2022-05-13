function show_display_buyer() {
   document.getElementById('display_buyer').style.display = "flex";
   document.getElementById('display_seller').style.display = "none";
}
function show_display_seller() {
   document.getElementById('display_buyer').style.display = "none";
   document.getElementById('display_seller').style.display = "flex";
}
// // // // // // // // // // // // // // // // // // // // // // // // //
function show_display_bought() {
   document.getElementById('display_bought').style.display = "flex";
   document.getElementById('display_sold').style.display = "none";
}
function show_display_sold() {
   document.getElementById('display_bought').style.display = "none";
   document.getElementById('display_sold').style.display = "flex";
}