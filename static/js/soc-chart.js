var ctx = document.getElementById('socChart');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
      labels: [],
      datasets: [{
        //lineTension: 0.3,
        backgroundColor: "rgba(35, 45, 75, 0.05)",
        borderColor: "rgba(35, 45, 75, 1)",
        //pointRadius: 1.5,
        //pointBackgroundColor: "rgba(35, 45, 75, 1)",
        //pointBorderColor: "rgba(35, 45, 75, 1)",
        //pointHoverRadius: 3,
        //pointHoverBackgroundColor: "rgba(35, 45, 75, 1)",
        //pointHoverBorderColor: "rgba(35, 45, 75, 1)",
        //pointHitRadius: 10,
        //pointBorderWidth: 2,
        data: [],
      }]
    },

    // Configuration options go here
    options: {
        scales: {
            xAxes:[{
                display:false
            }],
            yAxes: [{
                ticks: {
                    suggestedMin: 0,
                    suggestedMax: 100
                }
            }]
        },
        animation: {
            duration: 0 // general animation time
        },
        hover: {
            animationDuration: 0 // duration of animations when hovering an item
        },
        responsiveAnimationDuration: 0 // animation duration after a resize
        ,        
        elements: {
            line: {
                tension: 0 // disables bezier curves
            },
            point: {
                radius: 0
            }
            
        },

        legend: {
            display: false
        }
    }        

});

var n = 100;

function addData(chart, data) {
    chart.data.labels.push('');
    n = n - (n * (data * 0.0002));
    chart.data.datasets[0].data.push(n);

    chart.update();
}

