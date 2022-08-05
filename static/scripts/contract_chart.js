//import 'chartjs-adapter-moment';
const ctx = document.getElementById('myChart');
const myChart = new Chart(ctx, {
    type: 'scatter',
    data: {
        labels: ['Red', 'Blue', 'Yellow'],
        datasets: [{
            label: 'My First Dataset',
            data: [
              {x: moment("2017-07-08T06:15:02-0600"), y: 23.375},
              {x: moment("2017-07-08T06:20:02-0600"),y: 23.312},
              {x: moment("2017-07-08T06:25:02-0600"),y: 23.312},
              {x: moment("2017-07-08T06:30:02-0600"),y: 23.25}
            ],
             backgroundColor: 'rgb(255, 99, 132)'
          }
          ]
        // datasets: [{
        //     grouped: false,
        //     label: '# of Votes',
        //     data: [24, 19, 3, 18, 2, 3],
        //     backgroundColor: [
        //         'rgba(255, 99, 132, 0.2)',
        //         'rgba(54, 162, 235, 0.2)',
        //         'rgba(255, 206, 86, 0.2)',
        //         'rgba(75, 192, 192, 0.2)',
        //         'rgba(153, 102, 255, 0.2)',
        //         'rgba(255, 159, 64, 0.2)'
        //     ],
        //     borderColor: [
        //         'rgba(255, 99, 132, 1)',
        //         'rgba(54, 162, 235, 1)',
        //         'rgba(255, 206, 86, 1)',
        //         'rgba(75, 192, 192, 1)',
        //         'rgba(153, 102, 255, 1)',
        //         'rgba(255, 159, 64, 1)'
        //     ],
        //     borderWidth: 1
        // }]
    },
    options: {
    scales: {
      x: {
        // type: 'time',
        //   time: {
        //     unit: 'day'
        //   }
      }
    }
  }
});