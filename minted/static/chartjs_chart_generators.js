function create_bar_chart_config(data, labels, colours){
    var pie_chart_config = {
      type: 'pie',
      data: {
        datasets: [{
          data: data,
          backgroundColor: colours,
          label: 'Total',
          hoverOffset: 5
        }],
        labels: labels,
      },
      options: {
        responsive: true
      }
    };
    return pie_chart_config
  }

function create_line_chart_config(datasets, labels, colours){
    for (var i=0; i< datasets.length; i++){
        datasets[i].backgroundColor = colours[i]
        datasets[i].borderColor = colours[i]
    }
    var line_config = {
        type: 'line',
        data:{
        labels: labels,
        datasets: datasets
        },
        options: {
        scales: {
            yAxes: [{
            ticks: {
                beginAtZero: true
            }
            }]
        }
        }
    };
    return line_config
  }