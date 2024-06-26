import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";
import axios from "https://cdn.jsdelivr.net/npm/axios@1.6.8/+esm";

const dataSet = async function getData() {
    //return await d3.json("/transactions.json")
    //return await d3.json("/transactions.json");
    return await axios.get("/transactions.json");
}

async function drawChart() {
    const dataset = await dataSet();
    const data = dataset.data;

    // set the dimensions and margins of the graph
    const width = 450,
         height = 450,
         margin = 40
    
    // The radius of the pieplot is half the width or half the height (smallest one). I subtract a bit of margin.
    const radius = Math.min(width, height) / 2 - margin
    
    // append the svg object to the div called 'dataviz'
    const svg = d3.select("#dataviz")
        .append("svg")
        .attr("viewBox", `0 0 ${width} ${height}`)
        .append("g")
        .attr("transform", `translate(${width / 2}, ${height / 2})`);
        
    // set the color scale
    const color = d3.scaleOrdinal()
      .domain(["a", "b", "c", "d", "e", "f", "g", "h"])
      .range(d3.schemeDark2);
    
    // Compute the position of each group on the pie:
    const pieGenerator = d3.pie()
      .sort(null) // Do not sort group by size
      .value( function(data) {
        console.log(data);
        return data.MoneyIn
      } );

      // Call the pie generator to obtain the annotated data
    const data_ready = pieGenerator(data);

    // The arc generator
    const arc = d3.arc()
      .innerRadius(radius * 0.5)         // This is the size of the donut hole
      .outerRadius(radius * 0.8)
    
    // Another arc that won't be drawn. Just for labels positioning
    const outerArc = d3.arc()
      .innerRadius(radius * 0.9)
      .outerRadius(radius * 0.9)
    
    // Build the pie chart: Basically, each part of the pie is a path that we build using the arc function.
    svg
    .selectAll('allSlices')
    .data(data_ready)
    .enter()
    .append('path')
    .attr('d', arc)
    .attr('fill', function(d){ return(color(d.data.key)) })
    .attr("stroke", "white")
    .style("stroke-width", "2px")
    .style("opacity", 0.7)
    
    // Add the polylines between chart and labels:
    svg
    .selectAll('allPolylines')
    .data(data_ready)
    .enter()
    .append('polyline')
    .attr("stroke", "black")
    .style("fill", "none")
    .attr("stroke-width", 1)
    .attr('points', function (d) {
        var posA = arc.centroid(d) // line insertion in the slice
        var posB = outerArc.centroid(d) // line break: we use the other arc generator that has been built only for that
        var posC = outerArc.centroid(d); // Label position = almost the same as posB
        var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2 // we need the angle to see if the X position will be at the extreme right or extreme left
        posC[0] = radius * 0.95 * (midangle < Math.PI ? 1 : -1); // multiply by 1 or -1 to put it on the right or on the left
        return [posA, posB, posC]
    })
    
    // Add the polylines between chart and labels:
    svg
    .selectAll('allLabels')
    .data(data_ready)
    .enter()
    .append('text')
    .text(function (d) { console.log(d.data.key); return d.data.key })
    .attr('transform', function (d) {
        var pos = outerArc.centroid(d);
        var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2
        pos[0] = radius * 0.99 * (midangle < Math.PI ? 1 : -1);
        return 'translate(' + pos + ')';
    })
    .style('text-anchor', function (d) {
        var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2
        return (midangle < Math.PI ? 'start' : 'end')
    })

}

drawChart();
