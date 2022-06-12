/*
Answer Bounty
Alex Haas
*/
let contract_type = "assignment"
// INCOMPLETE:
function show_type_assignment() {
   contract_type = "assignment"
   document.getElementById('d_assignment').style.display = "flex";
   document.getElementById('d_test').style.display = "none";
}
// INCOMPLETE:
function show_type_test() {
   contract_type = "test"
   document.getElementById('d_assignment').style.display = "none";
   document.getElementById('d_test').style.display = "flex";
}