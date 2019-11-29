function chartdesigner(title,xAxis,yAxis,series){

  var newElement = [];
  newElement=document.createElement('div');
  newElement.id=title["text"];
  document.body.appendChild(newElement);

  Highcharts.chart(title["text"], {

        chart:{
          type:'column'
        },
        legend: {
            reversed: false
            
        },
        tooltip: {
               formatter: function() {
                    return '<b>'+ Highcharts.numberFormat(this.y, 0) +'</b><br/>'+
                        'Rankings: '+ this.x;
                }
            },
        plotOptions: {
            series: {
                 dataLabels: {
                  enabled:false
                }
            }
        },
        title:title,
        xAxis: xAxis,
        yAxis: yAxis,
        series: series
  });
}