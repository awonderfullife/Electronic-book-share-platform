function drawBubbleGraph(root) {

	var diameter = 800, margin = 0;

	var pack = d3.layout.pack().padding(2).size(
			[ diameter - margin, diameter - margin ]).value(function(d) {
		return d.rank;
	})

	var svg = d3.select('#knowledgegraph').append("svg")
			.attr("id", "graph").attr("height", diameter).append("g").attr(
					"transform",
					"translate(" + diameter  + "," + diameter / 2 + ")");

	var focus = root, nodes = pack.nodes(root), view;

	var maxWeight = d3.max(nodes, function(d) {
		return +d.weight;
	});
	var minWeight = d3.min(nodes, function(d) {
		return +d.weight;
	});
	console.log("Weight: " + minWeight + "," + maxWeight);
	
	var color = d3.scale.linear().domain([ minWeight, 0, maxWeight ]).interpolate(
			d3.interpolateHsl).range([ "#50bbdb", "#3176b2", "#59b559" ]);

	var circle = svg.selectAll("circle").data(nodes).enter().append("circle")
			.attr(
					"class",
					function(d) {
						return d.parent ? d.children ? "node"
								: "node node--leaf" : "node node--root";
					}).style("fill", function(d) {
				return color(d.weight);
			}).on("click", function(d) {
				if (focus !== d)
					zoom(d), d3.event.stopPropagation();
			});

	var text = svg.selectAll("text").data(nodes).enter().append("text").attr(
			"class", "label").style("fill-opacity", function(d) {
		return d.parent === root ? 1 : 0;
	}).style("display", function(d) {
		return d.parent === root ? "inline" : "none";
	}).text(function(d) {
		return d.name;
	});

	var node = svg.selectAll("circle,text");

	d3.select('#knowledgegraph').on("click", function() {
		zoom(root);
	});

	zoomTo([ root.x, root.y, root.r * 2 + margin ]);

	function zoom(d) {
		var focus0 = focus;
		focus = d;

		var transition = d3.transition().duration(d3.event.altKey ? 7500 : 750)
				.tween(
						"zoom",
						function(d) {
							var i = d3.interpolateZoom(view, [ focus.x,
									focus.y, focus.r * 2 + margin ]);
							return function(t) {
								zoomTo(i(t));
							};
						});

		transition.selectAll("text").filter(function(d) {
			return d.parent === focus || this.style.display === "inline";
		}).style("fill-opacity", function(d) {
			return d.parent === focus ? 1 : 0;
		}).each("start", function(d) {
			if (d.parent === focus)
				this.style.display = "inline";
		}).each("end", function(d) {
			if (d.parent !== focus)
				this.style.display = "none";
		});
	}

	function zoomTo(v) {
		var k = diameter / v[2];
		view = v;
		node.attr("transform", function(d) {
			return "translate(" + (d.x - v[0]) * k + "," + (d.y - v[1]) * k
					+ ")";
		});
		circle.attr("r", function(d) {
			return d.r * k;
		});
	}
}

function demoGraph() {
	
	var data = {"children":[{"children":[{"children":[],"name":"计算机科学","rank":26153,"weight":-2,"id":12454},{"children":[{"children":[],"name":"People by nationality and occupation","rank":143,"weight":-2,"id":46849},{"children":[],"name":"Indian people","rank":156,"weight":-1,"id":14378},{"children":[],"name":"Ecuadorian people","rank":32,"weight":-1,"id":149331},{"children":[],"name":"Italian people","rank":84,"weight":-1,"id":2662},{"children":[],"name":"German people","rank":96,"weight":-1,"id":2693},{"children":[],"name":"British people","rank":115,"weight":-1,"id":19834},{"children":[],"name":"American people","rank":84,"weight":1,"id":53037}],"name":"People by nationality","rank":326,"weight":-6,"id":20406},{"children":[{"children":[],"name":"J. R. R. Tolkien","rank":18,"weight":-1,"id":23935},{"children":[],"name":"Theodore Roosevelt","rank":18,"weight":-1,"id":156593},{"children":[],"name":"John F. Kennedy","rank":11,"weight":-1,"id":156602}],"name":"Categories named after people","rank":348,"weight":-3,"id":121457},{"children":[{"children":[],"name":"Lawyers","rank":169,"weight":-1,"id":25056},{"children":[],"name":"Writers","rank":180,"weight":-1,"id":5845},{"children":[],"name":"Politicians","rank":64,"weight":-1,"id":6767},{"children":[],"name":"Sailors","rank":53,"weight":-1,"id":141497},{"children":[],"name":"Models","rank":70,"weight":1,"id":28449}],"name":"People by occupation","rank":81,"weight":-3,"id":23211},{"children":[],"name":"Time People of the Year","rank":105,"weight":-1,"id":103173},{"children":[{"children":[],"name":"Royalty and nobility","rank":90,"weight":1,"id":12890}],"name":"People by wealth or status","rank":12,"weight":1,"id":112726}],"name":"People","rank":142,"weight":-14,"id":2255},{"children":[{"children":[{"children":[],"name":"Literature","rank":182,"weight":-1,"id":2563},{"children":[],"name":"Psychology","rank":666,"weight":-1,"id":11625},{"children":[],"name":"Society","rank":170,"weight":-1,"id":11372},{"children":[],"name":"Human geography","rank":44,"weight":-2,"id":53782},{"children":[],"name":"Gender","rank":62,"weight":-1,"id":115342},{"children":[],"name":"Marriage","rank":148,"weight":1,"id":27219}],"name":"Social sciences","rank":259,"weight":-5,"id":9701},{"children":[{"children":[],"name":"Biology","rank":292,"weight":-1,"id":1888},{"children":[],"name":"Chemistry","rank":1142,"weight":-2,"id":1890},{"children":[],"name":"Geology","rank":331,"weight":1,"id":2469}],"name":"Scientific disciplines","rank":25,"weight":-2,"id":76431},{"children":[],"name":"Mathematics","rank":1171,"weight":-1,"id":1877},{"children":[{"children":[],"name":"Landforms","rank":151,"weight":1,"id":24652}],"name":"Nature","rank":58,"weight":1,"id":2565},{"children":[{"children":[],"name":"Systems","rank":105,"weight":1,"id":22780}],"name":"Technology","rank":284,"weight":1,"id":2557}],"name":"Science","rank":204,"weight":-6,"id":2216},{"children":[{"children":[{"children":[],"name":"Comedy","rank":71,"weight":-1,"id":19486},{"children":[],"name":"Media franchises","rank":32,"weight":-1,"id":182551},{"children":[],"name":"Sports","rank":246,"weight":-4,"id":1798},{"children":[],"name":"Performing arts","rank":73,"weight":-1,"id":97391},{"children":[],"name":"Entertainment awards","rank":52,"weight":-1,"id":113980},{"children":[],"name":"Competitions","rank":54,"weight":1,"id":18836}],"name":"Entertainment","rank":145,"weight":-7,"id":2238},{"children":[{"children":[],"name":"Writing tools","rank":69,"weight":-1,"id":24409}],"name":"Tools","rank":527,"weight":-1,"id":1808},{"children":[{"children":[],"name":"20th century in music","rank":43,"weight":-1,"id":123208},{"children":[],"name":"Music awards","rank":50,"weight":-1,"id":109388},{"children":[],"name":"Music genres","rank":176,"weight":-1,"id":10398},{"children":[],"name":"Musical entertainers","rank":27,"weight":-1,"id":38332},{"children":[],"name":"Opera","rank":48,"weight":-1,"id":23062},{"children":[],"name":"Music events","rank":18,"weight":0,"id":24282},{"children":[],"name":"Music technology","rank":65,"weight":1,"id":27124}],"name":"Music","rank":282,"weight":-4,"id":2240},{"children":[{"children":[],"name":"Drinks","rank":93,"weight":-1,"id":2235},{"children":[],"name":"Foods","rank":316,"weight":-1,"id":2230}],"name":"Food and drink","rank":148,"weight":-2,"id":17979},{"children":[{"children":[],"name":"Transport by country","rank":79,"weight":-1,"id":54896}],"name":"Transport","rank":152,"weight":-1,"id":2531},{"children":[{"children":[],"name":"Art","rank":297,"weight":0,"id":2242},{"children":[],"name":"Awards","rank":79,"weight":0,"id":12516},{"children":[],"name":"Culture by nationality","rank":74,"weight":-1,"id":46845}],"name":"Culture","rank":175,"weight":-1,"id":16940},{"children":[{"children":[],"name":"Calendars","rank":115,"weight":-1,"id":25172}],"name":"Time","rank":131,"weight":0,"id":2236},{"children":[{"children":[],"name":"Games","rank":179,"weight":1,"id":2239}],"name":"Leisure","rank":75,"weight":1,"id":24626}],"name":"Everyday life","rank":355,"weight":-15,"id":2231},{"children":[{"children":[{"children":[],"name":"Categories by geographical location","rank":177,"weight":-6,"id":76106}],"name":"Places","rank":22,"weight":-6,"id":76126},{"children":[{"children":[],"name":"Geography of Europe","rank":38,"weight":-1,"id":33015}],"name":"Geography by continent","rank":38,"weight":-1,"id":40466},{"children":[{"children":[],"name":"Geography of the United Kingdom","rank":46,"weight":-1,"id":33014}],"name":"Geography by country","rank":234,"weight":-1,"id":40464},{"children":[{"children":[],"name":"Categories by region","rank":30,"weight":-1,"id":76394},{"children":[],"name":"Regions by country","rank":26,"weight":0,"id":147657}],"name":"Regions","rank":42,"weight":-1,"id":53801},{"children":[{"children":[],"name":"World Heritage Sites by country","rank":82,"weight":-1,"id":126460}],"name":"World Heritage Sites","rank":36,"weight":-1,"id":32599}],"name":"Geography","rank":125,"weight":-10,"id":2217},{"children":[{"children":[{"children":[],"name":"Educators","rank":202,"weight":-1,"id":104735}],"name":"Education","rank":212,"weight":-1,"id":29978},{"children":[{"children":[],"name":"Symbols","rank":151,"weight":0,"id":14854}],"name":"Reference","rank":18,"weight":0,"id":29502}],"name":"Knowledge","rank":49,"weight":-1,"id":29503},{"children":[{"children":[{"children":[],"name":"Categories by time","rank":45,"weight":-2,"id":76115}],"name":"Chronology","rank":25,"weight":-2,"id":76118},{"children":[{"children":[],"name":"20th century","rank":100,"weight":0,"id":4550},{"children":[],"name":"Categories by year","rank":45,"weight":-1,"id":46877}],"name":"Years","rank":207,"weight":-1,"id":2536},{"children":[{"children":[],"name":"History of Pakistan","rank":140,"weight":-1,"id":29980},{"children":[],"name":"History of Australia","rank":92,"weight":-1,"id":24447},{"children":[],"name":"History of the United States","rank":155,"weight":-1,"id":14871}],"name":"History by country","rank":100,"weight":-3,"id":24445},{"children":[{"children":[],"name":"Geological periods","rank":46,"weight":-1,"id":88381}],"name":"Periods and ages in history","rank":37,"weight":-1,"id":114541},{"children":[],"name":"Middle Ages","rank":90,"weight":-1,"id":27770},{"children":[{"children":[],"name":"History by continent","rank":25,"weight":1,"id":24444}],"name":"History by region","rank":16,"weight":1,"id":24443},{"children":[{"children":[],"name":"Former countries in Europe","rank":103,"weight":1,"id":23944}],"name":"Former countries","rank":45,"weight":1,"id":15434}],"name":"History","rank":111,"weight":-6,"id":2581},{"children":[{"children":[{"children":[],"name":"Islam by country","rank":41,"weight":-1,"id":122575}],"name":"Religion by country","rank":35,"weight":-1,"id":64485},{"children":[{"children":[],"name":"Caliphates","rank":27,"weight":-1,"id":122574},{"children":[],"name":"Vatican City","rank":39,"weight":1,"id":5015}],"name":"Theocracies","rank":21,"weight":0,"id":123830},{"children":[{"children":[],"name":"Bible","rank":113,"weight":1,"id":19646}],"name":"Religious texts","rank":75,"weight":1,"id":14534},{"children":[{"children":[],"name":"Christian theology","rank":124,"weight":1,"id":28318}],"name":"Theology","rank":170,"weight":1,"id":45477}],"name":"Religion","rank":224,"weight":1,"id":2325}],"name":"Articles","rank":49,"weight":-51,"id":58229};
	var content = "<div id='knowledgegraph'></div>";
	$("#map").html(content);
	drawBubbleGraph(data);
	
}
