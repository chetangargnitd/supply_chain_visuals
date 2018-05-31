{% load staticfiles %}

var screenWidth = $(window).width();

var margin = {left: 10, top: 30, right: 10, bottom: 10},
	width = Math.min(screenWidth, 600) - margin.left - margin.right,
	height = Math.min(screenWidth, 600)*5/6 - margin.top - margin.bottom;
			
var svg = d3.select("#chart").append("svg")
			.attr("width", (width + margin.left + margin.right))
			.attr("height", (height + margin.top + margin.bottom));
			
var wrapper = svg.append("g").attr("class", "chordWrapper")
			.attr("transform", "translate(" + (width / 2 + margin.left) + "," + (height / 2 + margin.top) + ")");;
			
var outerRadius = Math.min(width, height) / 2  - 100,
	innerRadius = outerRadius * 0.95,
	opacityDefault = 0.7; //default opacity of chords
	
////////////////////////////////////////////////////////////
////////////////////////// Data ////////////////////////////
////////////////////////////////////////////////////////////

var Names = ["From Manufacturing","From Distribution","From Procurement","From Retail","From Transportation","To Manufacturing","To Distribution","To Procurement","To Retail","To Transportation"];


d3.json("{% static 'visualizations/json/data.json' %}", function(data){
	var chord = d3.layout.chord()
		.padding(.02)
		.sortSubgroups(d3.descending) //sort the chords inside an arc from high to low
		.sortChords(d3.descending) //which chord should be shown on top when chords cross. Now the biggest chord is at the bottom
		.matrix(data);


	var arc = d3.svg.arc()
		.innerRadius(innerRadius)
		.outerRadius(outerRadius);

	var path = d3.svg.chord()
		.radius(innerRadius);
		
	var fill = d3.scale.ordinal()
	    .domain(d3.range(Names.length))
	    .range(["#f48c42","#6541f4","#9a41f4","#fed800","#850303","#f48c42","#6541f4","#9a41f4","#fed800","#850303",]);

////////////////////////////////////////////////////////////
//////////////////// Draw outer Arcs ///////////////////////
////////////////////////////////////////////////////////////

	var g = wrapper.selectAll("g.group")
		.data(chord.groups)
		.enter().append("g")
		.attr("class", "group");;

	g.append("path")
		.style("stroke", function(d) { return fill(d.index); })
		.style("fill", function(d) { return fill(d.index); })
		.attr("d", arc);

////////////////////////////////////////////////////////////
////////////////////// Append Names ////////////////////////
////////////////////////////////////////////////////////////

g.append("text")
	.each(function(d) { d.angle = ((d.startAngle + d.endAngle) / 2);})
	.attr("dy", ".35em")
	.attr("class", "titles")
	.attr("text-anchor", function(d) { return d.angle > Math.PI ? "end" : null; })
	.attr("transform", function(d,i) { 
		var c = arc.centroid(d);
		return "rotate(" + (d.angle * 180 / Math.PI - 90) + ")"
		+ "translate(" + (outerRadius + 5) + ")"
		+ (d.angle > Math.PI ? "rotate(180)" : "")
	})
	.text(function(d,i) {
		var ctr = 0; 
		for(var j=0;j<10;j++){
			if(data[i][j]==0)
				ctr++;
		}
		if(ctr!=10)
			return Names[i]; 
		else
			return " ";

	});

//+ "translate(" + (innerRadius + 55) + ")"

////////////////////////////////////////////////////////////
//////////////////// Draw inner chords /////////////////////
////////////////////////////////////////////////////////////
 
var colors = ["#00A0B0","#CC333F","#EDC951"];
var chords = wrapper.selectAll("path.chord")
	.data(chord.chords)
	.enter().append("path")
	.attr("class", "chord")
	.style("stroke", "none")
	.style("fill", function(d,i) { return fill(d.source.index); })
	.style("opacity", opacityDefault)
	.attr("d", path);	

////////////////////////////////////////////////////////////
///////////////////////// Tooltip //////////////////////////
////////////////////////////////////////////////////////////

//Arcs
g.append("title")	
	.text(function(d, i) {return Math.round(d.value) + " stages of " + Names[i];});
	
//Chords
chords.append("title")
	.text(function(d) {
		return [Math.round(d.source.value), " edges ",Names[d.source.index], " ", Names[d.target.index]].join(""); 
	});
})