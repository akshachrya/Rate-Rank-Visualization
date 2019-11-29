function divnpsscale(series){
  var newElement = []; //Outer div
  var newElement1 = []; //inner div
  var newElement2 = []; //inner div

  newElement2=document.createElement('div');
  newElement2.className="row";
  newElement2.id="row";
  document.body.appendChild(newElement2);

  for(var i=0;i<series.length;i++){
    newElement1[i]=document.createElement('div');
    newElement1[i].className="col-lg-4";
    newElement1[i].id=((series[i])[0])['name'];
    document.getElementById("row").appendChild(newElement1[i]);

    newElement[i]=document.createElement('div');
    newElement[i].id=((series[i])[0])['name'];
    document.getElementById(((series[i])[0])['name']).appendChild(newElement[i]);



  }

}


function npsscale(id,name,series){
  (function (H) {
    H.seriesType('lineargauge', 'column', null, {
        setVisible: function () {
            H.seriesTypes.column.prototype.setVisible.apply(this, arguments);
            if (this.markLine) {
                this.markLine[this.visible ? 'show' : 'hide']();
            }
        },
        drawPoints: function () {
            // Draw the Column like always
            H.seriesTypes.column.prototype.drawPoints.apply(this, arguments);

            // Add a Marker
            var series = this,
                chart = this.chart,
                inverted = chart.inverted,
                xAxis = this.xAxis,
                yAxis = this.yAxis,
                point = this.points[0], // we know there is only 1 point
                markLine = this.markLine,
                ani = markLine ? 'animate' : 'attr';

            // Hide column
            point.graphic.hide();

            if (!markLine) {
                var path = inverted ? ['M', 0, 0, 'L', -5, -5, 'L', 5, -5, 'L', 0, 0, 'L', 0, 0 + xAxis.len] :
                   ['M', 0, 0, 'L', -5, -5, 'L', -5, 5, 'L', 0, 0, 'L', xAxis.len, 0];
                markLine = this.markLine = chart.renderer.path(path)
                    .attr({
                        fill: series.color,
                        stroke: series.color,
                        'stroke-width': 1
                    }).add();
            }
            markLine[ani]({
                translateX: inverted ? xAxis.left + yAxis.translate(point.y) : xAxis.left,
                translateY: inverted ? xAxis.top : yAxis.top + yAxis.len -  yAxis.translate(point.y)
            });
        }
    });
  }(Highcharts));

  Highcharts.chart(id, {
      chart: {
          type: 'lineargauge',
          inverted: true,
          height: 150
      },
      title: {
          text:name
      },
      tooltip: {
        formatter: function() {
            return '</b> NPS Score: <b>' + this.y;
        }
      },
      xAxis: {
          lineColor: '#C0C0C0',
          labels: {
              enabled: false
          },
          tickLength: 0
      },
      yAxis: {
          min:-100,
          max:100,
          tickLength: 5,
          tickWidth: 1,
          tickColor: '#C0C0C0',
          gridLineColor: '#C0C0C0',
          gridLineWidth: 0,
          minorTickInterval:0,
          minorTickWidth: 0,
          minorTickLength: 0,
          minorGridLineWidth: 0,

          title: null,
          labels: {
              format: '{value}'
          },
          plotBands: [{
              from: -100,
              to: 0,
              color: '#FF3333'
          },
          {
              from: -50,
              to: 0,
              color: '#FF9999'
          },{
              from:0,
              to: 50,
              color: '#99FF99'
          },
          {
              from:50,
              to: 100,
              color: '#00CC00'
          }]
      },
      legend: {
          enabled: false
      },
      credits:{
        enabled:false
      },
      plotOptions:{
        series:{
          color: '#000000',
          dataLabels: {
              enabled: true,
              align: 'center',
              format: '{point.y}',
              color:'white'
          }
        }

      },

      series:series

  });


}
