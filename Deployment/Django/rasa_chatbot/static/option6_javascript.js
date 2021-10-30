AmCharts.makeChart("chartdiv",
		{
			"type": "serial",
			"categoryField": "date",
			"columnWidth": 0,
			"dataDateFormat": "YYYY-MM-DD HH",
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
					"title": "GRUPOSURA",
					"type": "smoothedLine",
					"valueField": "GRUPOSURA"
				},
				{
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
				}
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
			"dataProvider": [
				{
					"date": "2018-08-19 15:00",
					"GRUPOSURA": 36308,
					"PFGRUPOSURA": 35419,
					"LOREM": 36521
				},
				{
					"date": "2018-08-19 16:00",
					"GRUPOSURA": 36196,
					"PFGRUPOSURA": 35132,
					"LOREM": 36623
				},
				{
					"date": "2018-08-19 17:00",
					"GRUPOSURA": 36907,
					"PFGRUPOSURA": 35293,
					"LOREM": 36237
				},
				{
					"date": "2018-08-19 18:00",
					"GRUPOSURA": 36312,
					"PFGRUPOSURA": 35296,
					"LOREM": 36144
				},
				{
					"date": "2018-08-19 19:00",
					"GRUPOSURA": 36399,
					"PFGRUPOSURA": 35398,
					"LOREM": 36275
				},
				{
					"date": "2018-08-19 20:00",
					"GRUPOSURA": 36473,
					"PFGRUPOSURA": 35368,
					"LOREM": 36595
				},
				{
					"date": "2018-08-19 21:00",
					"GRUPOSURA": 36182,
					"PFGRUPOSURA": 35257,
					"LOREM": 36423
				}
			]
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