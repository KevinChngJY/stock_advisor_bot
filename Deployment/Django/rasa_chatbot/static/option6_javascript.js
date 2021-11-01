AmCharts.makeChart("chartdiv",
		{
			"type": "serial",
			"categoryField": "date",
			"columnWidth": 0,
			"dataDateFormat": "YY-MM-DD",
			"maxSelectedSeries": 0,
			"zoomOutText": "Ver todo",
      "language": "es",
			"colors": [
				"#fff",
				"#022658",
				"#E3E829"
			],
			"sequencedAnimation": false,
			"startEffect": "easeOutSine",
			"backgroundColor": "#149FB9",
			"borderColor": "#000",
			"color": "#FFFFFF",
			"fontFamily": "Lato",
			"fontSize": 9,
			"handDrawScatter": 0,
			"handDrawThickness": 0,
			"processCount": 1002,
			"theme": "dark",
			"categoryAxis": {
				"autoRotateAngle": 0,
				"minPeriod": "hh",
				"parseDates": true,
				"fontSize": 9,
				"title": "",
				"titleBold": false
			},
			"chartCursor": {
				"enabled": true,
				"animationDuration": 0,
				"bulletSize": 0,
				"categoryBalloonDateFormat": "JJ:NN",
				"cursorAlpha": 0.2,
				"fullWidth": true,
				"graphBulletSize": 1,
				"selectionAlpha": 0.05,
				"showNextAvailable": true,
				"valueLineAlpha": 0.49,
				"valueLineBalloonEnabled": true,
				"valueLineEnabled": true,
        "cursorAlpha": 0.05
			},
			"chartScrollbar": {
				"enabled": true
			},
			"trendLines": [],
			"graphs": [
				{
					"balloonText": "Precio [[value]]",
					"bullet": "round",
					"id": "AmGraph-1",
					"title": "stock",
					"type": "smoothedLine",
					"valueField": "stock"
				}
				/*{
					"balloonText": "Precio [[value]]",
					"bullet": "round",
					"id": "AmGraph-2",
					"title": "PFGRUPOSURA",
					"type": "smoothedLine",
					"valueField": "PFGRUPOSURA"
				},
				{
					"balloonText": "Precio [[value]]",
					"bullet": "round",
					"id": "AmGraph-3",
					"title": "LOREM",
					"type": "smoothedLine",
					"valueField": "LOREM"
				}*/
			],
			"guides": [],
			"valueAxes": [
				{
					"id": "ValueAxis-2"
				}
			],
			"allLabels": [],
			"balloon": {
				"animationDuration": 0.2,
				"fadeOutDuration": 0
			},
			"legend": {
				"enabled": true,
				"bottom": 0,
				"equalWidths": false,
				"gradientRotation": 0,
				"labelWidth": 0,
				"markerBorderAlpha": 0,
				"markerSize": 14,
				"maxColumns": 4,
				"rollOverColor": "#DDE621",
				"rollOverGraphAlpha": 0.21,
				"useGraphSettings": true,
				"valueAlign": "left"
			},
			"titles": [],
			"dataProvider": getData(),
			//[
			//	{
			//		"date": "2018-08-19 15:00",
			//		"GRUPOSURA": 36308
			//	}
			//]
		}
	);

var $table = $('#table');
    $(function () {
        $('#toolbar').find('select').change(function () {
            $table.bootstrapTable('refreshOptions', {
                exportDataType: $(this).val()
            });
        });
    })

		var trBoldBlue = $("table");

	$(trBoldBlue).on("click", "tr", function (){
			$(this).toggleClass("bold-blue");
	});

function getData(){
	var table = document.getElementById('table');
	var chartData = [];
	for (var r = 1, n = table.rows.length; r < n; r++) {
			//for (var c = 0, m = table.rows[r].cells.length; c < m; c++) {
				//document.write(table.rows[r].cells[c].innerHTML);
				date=table.rows[r].cells[0].innerHTML;
				stock=table.rows[r].cells[1].innerHTML;
				chartData.push({date:date,stock:parseFloat(stock)});
			//}
	};

	return chartData
}
	
//AmCharts.dataProvider=chartData;