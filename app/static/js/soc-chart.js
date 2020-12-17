var ctx = document.getElementById('socChart');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
      labels: [],
      datasets: [{
        backgroundColor: "rgba(35, 45, 75, 0.05)",
        borderColor: "rgba(35, 45, 75, 1)",
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
    chart.data.datasets[0].data.push(data);

    chart.update();
}

function setData(chart,data){
    chart.data.datasets[0].data = data;
}

function clearGraph(chart){
    chart.data.datasets[0].data = [];
    chart.data.labels = [];
}
