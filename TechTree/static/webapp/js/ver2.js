var width = 3600,
    height = 1000;

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

// Per-type markers, as they don't inherit styles.
svg.append("defs").selectAll("marker")
    .data(["suit", "licensing", "resolved"])
    .enter().append("marker")
    .attr("id", function(d) { return d; })
    .attr("viewBox", "0 -5 10 10")
    .attr("refX", 15)
    .attr("refY", -1.5)
    .attr("markerWidth", 6)
    .attr("markerHeight", 6)
    .attr("orient", "auto")
    .append("path")
    .attr("d", "M0,-5L10,0L0,5");

d3.json("/static/webapp/graph.json", function(error, graph) {
    if (error) throw error;

    function assignXY() {
        for(i = 0; i < graph.nodes.length; i++) {
            d = graph.nodes[i];
            posArr = d.pos.split(',')
            console.log(posArr);
            scale = 1
            offset = 50 + Math.floor(Math.random() * 30) - 15
            d.x = parseInt(posArr[0], 10)*scale + offset;
            scale = 0.8 
            offset = 100 + Math.floor(Math.random() * 50) - 25
            d.y = (height - parseInt(posArr[1], 10))*scale + offset;
            d.px = d.x
            d.py = d.y
            d.fixed = true;
            console.log(d.x);
            console.log(d.y);
        }
    }

    assignXY();

    var force = d3.layout.force()
        .size([width, height])
        .linkDistance(60)
        .charge(-300)
        .nodes(graph.nodes)
        .links(graph.links)
        .on("tick", tick)
        .start();

    console.log(graph.nodes)
    console.log(graph.links)

    var path = svg.append("g").selectAll("path")
        .data(force.links())
        .enter().append("path")
        .attr("class", function(d) { return "link " + d.type; })
        //.attr("marker-end", function(d) { return "url(#" + d.type + ")"; });
        .attr("marker-end", function(d) { return "url(#suit)"; });

    var circle = svg.append("g").selectAll("circle")
        .data(force.nodes())
        .enter().append("circle")
        .attr("r", 6)
        .call(force.drag);

    var text = svg.append("g").selectAll("text")
        .data(force.nodes())
        .enter().append("text")
        .attr("x", 8)
        .attr("y", ".31em")
        .text(function(d) { return d.label; });

    // Use elliptical arc path segments to doubly-encode directionality.
    function tick() {
      path.attr("d", linkArc);
      circle.attr("transform", transform);
      text.attr("transform", transform);
    }

    function linkArc(d) {
      var dx = d.target.x - d.source.x,
          dy = d.target.y - d.source.y,
          dr = Math.sqrt(dx * dx + dy * dy);
      return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + d.target.x + "," + d.target.y;
    }

    function transform(d) {
      return "translate(" + d.x + "," + d.y + ")";
    }
});
