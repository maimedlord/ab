// runs at load:
// window.onload = function () {
//
//    // nowDateTime = new Date().toISOString().split('T');
//    // datePart = nowDateTime[0];
//    // timePart = nowDateTime[1];
//    // // console.log(datePart);
//    // // console.log(timePart);
//    // var graph_children = document.getElementById('container_graph').children;
//    // // console.log(graph_children);
//    // for (var i = 0; i < graph_children.length; i++) {
//    //    console.log(graph_children[i].id);
//    //    if (graph_children[i].id < datePart) {
//    //       // console.log(graph_children[i].children);
//    //       for (var ii = 0; ii < graph_children[i].children.length - 1; ii++) {
//    //          // graph_children[i].children[ii].style.backgroundColor = 'lightgray';
//    //          graph_children[i].children[ii].style.borderColor = 'gray';
//    //          graph_children[i].children[ii].style.boxShadow = 'inset 3px 3px dimgray';
//    //       }
//    //    }
//    //    if (graph_children[i].id <= datePart) {
//    //       // console.log(graph_children[i]);
//    //       for (var ii = 0; ii < graph_children[i].children.length - 1; ii++) {
//    //          // console.log(graph_children[i].children[ii].id);
//    //          if (graph_children[i].children[ii].id <= timePart) {
//    //             // graph_children[i].children[ii].style.backgroundColor = 'lightgray';
//    //             graph_children[i].children[ii].style.borderColor = 'gray';
//    //             graph_children[i].children[ii].style.boxShadow = 'inset 3px 3px dimgray';
//    //          }
//    //       }
//    //    }
//    // }
// };

function set_timeline_graph(phase, tl_arr) {
   // prep graph_day:
   container = document.getElementById('container_graph');
   graph_day = document.createElement('div');
   graph_day.classList.add('graph_day');
   // other vars:
   earlyPhases = ['creation', 'open']
   console.log(phase);
   console.log(tl_arr);
   // if not in early phases we don't want to show creation and stall data:
   // if (!earlyPhases.includes(phase)) {
   //    tl_arr[0]['time'] = null;
   //    tl_arr[2]['time'] = null;
   // }
   // nowDateTime = new Date().toISOString().split('T');
   previousElement = [null, null];
   for (var i = 0; i < tl_arr.length; i++) {
      if (tl_arr[i]['time']) {
         // console.log(typeof tl_arr[i]['time']);
         // console.log(tl_arr[i]['time']);
         var tempDate = new Date(tl_arr[i]['time']);// creates user-local date
         if (tempDate.getMonth() == previousElement[0] && tempDate.getDate() == previousElement[1]) {
            // same day
            console.log('same day');
         }
         else {
            previousElement[0] = tempDate.getMonth();
            previousElement[1] = tempDate.getDate();
            console.log(previousElement);
            // lakjds ;flakjd f;lkaj sxcclkjz Xclkj zlkcxj vxl;zkjc xv;lkzj cvlkzj xcv
         }
      }
   }

   // container.appendChild(graph_day);
   // console.log(container);
}

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
   //
});