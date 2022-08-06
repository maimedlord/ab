// runs at load:
window.onload = function () {
   nowDateTime = new Date().toISOString().split('T');
   datePart = nowDateTime[0];
   timePart = nowDateTime[1];
   console.log(datePart);
   console.log(timePart);
   var graph_children = document.getElementById('container_graph').children;
   console.log(graph_children);
   for (var i = 0; i < graph_children.length; i++) {
      // console.log(graph_children[i].id);
      if (graph_children[i].id <= datePart) {
         // console.log(graph_children[i]);
         for (var ii = 0; ii < graph_children[i].children.length - 1; ii++) {
            // console.log(graph_children[i].children[ii].id);
            if (graph_children[i].children[ii].id <= timePart) {
               graph_children[i].children[ii].style.backgroundColor = 'lightgray';
            }
         }
      }
   }
};

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