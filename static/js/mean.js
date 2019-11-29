function divmean(mainseries){
	var newElement = []; //Outer div
	var newElement1 = []; //inner div
	var newElement2 = []; //inner div

	newElement2=document.createElement('div');
	newElement2.className="row";
	newElement2.id="row";
	document.body.appendChild(newElement2);

	for(var i=0;i<mainseries.length;i++){
	  newElement1[i]=document.createElement('div');
	  newElement1[i].className="col-lg-4";
	  newElement1[i].id=((mainseries[i])[1])['name'];
	  document.getElementById("row").appendChild(newElement1[i]);

	  newElement[i]=document.createElement('div');
	  newElement[i].id=((mainseries[i])[1])['name'];
	  document.getElementById(((mainseries[i])[1])['name']).appendChild(newElement[i]);

	}

}

function gauge(id,series,target,min,max,name){


  var gaugeOptions = {

      chart: {
          type: 'solidgauge',
           height:400
      },

      title: null,

      pane: {
          center: ['50%', '58%'],
          size: '60%',
          startAngle: -90,
          endAngle: 90,
          background: {
              innerRadius: '60%',
              outerRadius: '100%',
              shape: 'arc'
          }
      },
      // the value axis
      yAxis: {
          stops: [
              [(target/max)-0.01, 'red'],
              [target/max, 'yellow'],
              [(target/max)+0.01, 'green'],
          ],
          lineWidth: 0,
          minorTickInterval: null,
          tickAmount: 1,
          title: {
              enabled:false
          },
          labels: {
              y: 24
          }
      },

      plotOptions: {
          solidgauge: {
              dataLabels: {
                 enabled:true
              }
          },
          series: {
                 dataLabels: {
                  enabled:true
                }
            },
          pie:{
          showInLegend: true,
          dataLabels: {
                  distance: -15,
                  format: '</b>{point.y}',
                  color: 'white'
              }
        }
      }
  };



  // The speed gauge
  var chartSpeed = Highcharts.chart(id, Highcharts.merge(gaugeOptions, {

      title:{
        text:name
      },

      yAxis: {
          min: min,
          max: max
      },

      credits: {
          enabled: false
      },

      series:series

  }));
  

  
}



