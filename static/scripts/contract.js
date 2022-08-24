// runs at load:
window.onload = function () {
   document.getElementById('user_timezone').innerText = 'your timezone: '
       +  new Date().toString().match('([A-Z][a-z]+ [A-Za-z]+ [A-Za-z]+)')[0];

   if (document.getElementById('div_iparty_row').innerText == '') {
      document.getElementById('div_iparty_row').style.display = 'none';
   }
};

// don't forget test times...
function set_timeline_graph(phase, tl_arr) {
   // prep graph_day:
   container = document.getElementById('container_graph');
   console.log(container);
   // other vars:
   earlyPhases = ['creation', 'open']
   todayDateObj = {'event': 'page loaded', 'time': new Date()};
   todayDate_graph_cell = document.createElement('div');
   todayDate_graph_cell.classList.add('graph_cell');
   todayDate_graph_cell.innerText = todayDateObj.toString();
   // if not in early phases we don't want to show creation and stall data:
   if (!earlyPhases.includes(phase)) {
      tl_arr[0]['time'] = null;
      tl_arr[2]['time'] = null;
   }
   // nowDateTime = new Date().toISOString().split('T');
   previousElement = [null, null, null];// year, month, day
   nowIsWritten = false;
   // counter = 1;
   for (var i = 0; i < tl_arr.length; i++) {
      if (tl_arr[i]['time']) {
         const tempDate = new Date(tl_arr[i]['time']);// creates user-local date
         tempMinutes = tempDate.getMinutes().toString()
         if (tempMinutes.length < 2) {
            tempMinutes = '0' + tempMinutes;
         }
         div_graph_cell = document.createElement('div');
         div_g_c_event = document.createElement('div');
         div_g_c_event.innerText = tl_arr[i]['event'];
         div_g_c_time = document.createElement('div');
         div_g_c_time.classList.add('graph_cell_time');
         div_g_c_time.innerText = tempDate.getHours().toString() + ':' + tempMinutes;
         if (nowIsWritten) {
            div_graph_cell.classList.add('graph_cell');
         }
         else {
            div_graph_cell.classList.add('graph_cell_past');
         }
         div_graph_cell.appendChild(div_g_c_event);
         div_graph_cell.appendChild(div_g_c_time);
         // same day:
         if (tempDate.getFullYear() == previousElement[0] && tempDate.getMonth() == previousElement[1]
             && tempDate.getDate() == previousElement[2]) {
            container.lastChild.appendChild(div_graph_cell);
         }
         // new day:
         else {
            previousElement[0] = tempDate.getFullYear();
            previousElement[1] = tempDate.getMonth();
            previousElement[2] = tempDate.getDate();
            div_graph_day = document.createElement('div');
            div_graph_day.classList.add('graph_day');
            div_graph_day.innerText = tempDate.toString().match('[A-Za-z]+ [A-Za-z]+ [0-9]+')[0];
            div_graph_day.appendChild(div_graph_cell);
            container.appendChild(div_graph_day);
         }
         // write in todayDateObj:
         if (!nowIsWritten
            && i + 1 < tl_arr.length
            && todayDateObj['time'].getFullYear() >= tempDate.getFullYear()
            && todayDateObj['time'].getMonth() >= tempDate.getMonth()
            && todayDateObj['time'].getDate() >= tempDate.getDate()
            && (todayDateObj['time'] < new Date(tl_arr[i + 1]['time']) || todayDateObj['time'] < new Date(tl_arr[i + 2]['time']))) {
               // counter++;
               tempMinutes = todayDateObj['time'].getMinutes().toString()
               if (tempMinutes.length < 2) {
                  tempMinutes = '0' + tempMinutes;
               }
               div_graph_cell_2 = document.createElement('div');
               div_graph_cell_2.classList.add('graph_cell_today');
               div_g_c_event_2 = document.createElement('div');
               div_g_c_time_2 = document.createElement('div');
               div_g_c_time_2.classList.add('graph_cell_time');
               div_g_c_event_2.innerText = todayDateObj['event'];
               div_g_c_time_2.innerText = todayDateObj['time'].getHours().toString() + ':' + tempMinutes;;
               div_graph_cell_2.appendChild(div_g_c_event_2);
               div_graph_cell_2.appendChild(div_g_c_time_2);
               // todayDateObj is same day as existing events:
               if (todayDateObj['time'].getDate() == tempDate.getDate()) {
                  container.lastChild.appendChild(div_graph_cell_2);
               }
               // todayDateObj is on its own day:
               else {
                  div_graph_day_2 = document.createElement('div');
                  div_graph_day_2.classList.add('graph_day');
                  div_graph_day_2.innerText = todayDateObj['time'].toString().match('[A-Za-z]+ [A-Za-z]+ [0-9]+')[0];
                  div_graph_day_2.appendChild(div_graph_cell_2);
                  container.appendChild(div_graph_day_2);
               }
            nowIsWritten = true;
         }
      }
      // counter++;
   }
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