function grade_no() {
   document.getElementById('div_grade_proof').style.display = 'flex';
   document.getElementById('grade_file').hidden = false;
   document.getElementById('grade_file').required = true;
}
function grade_yes() {
   document.getElementById('div_grade_proof').style.display = 'none';
   document.getElementById('grade_file').hidden = true;
   document.getElementById('grade_file').required = false;
   document.getElementById('grade_file').value = null;
}
$(document).ready(function () {
   $('#nav_top_col2').click(function () {
      console.log(moment('2017-07-08T06:30:02-0600').valueOf());
   });
});