function create_pie_chart_config(data, labels, colours){
    var pie_chart_config = {
      type: 'doughnut',
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
        responsive: true,
        title: {
            display: true,
            text: 'All Spending'
        } 
      }
    };
    return pie_chart_config
}

function create_line_chart_config(datasets, labels, colours, time_interval, start_date, end_date){
    for (var i=0; i< colours.length; i++){
        datasets[i].backgroundColor = colours[i]
        datasets[i].borderColor = colours[i]
    }
    var cap_time_interval = time_interval.charAt(0).toUpperCase() + time_interval.substring(1);
    var title = `${cap_time_interval} Spending between ${start_date} and ${end_date}`
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
          },
          title: {
              display: true,
              text: title
          } 
        }
    };
    return line_config
  }