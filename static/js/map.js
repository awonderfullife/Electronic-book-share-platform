$.ajax({
    type: 'GET',
    url: '/api/v1/subject_map',
    success: function(data) {
        draw_map(data);
    },
});

function draw_map(data) {
    var diameter = 800, margin = 20;
    var svg = d3.select("svg"),
        g = svg.append("g")
        .attr("transform", "translate(" + diameter  + "," + diameter / 2 + ")");

    var color = d3.scaleLinear()
        .domain([-1, 5])
        .range(["hsl(152,80%,80%)", "hsl(228,30%,40%)"])
        .interpolate(d3.interpolateHcl);

    var pack = d3.pack()
        .size([diameter - margin, diameter - margin])
        .padding(2);

    var root = d3.hierarchy(data)
        .sum(function (d) {
            return d.size;
        })
        .sort(function (a, b) {
            return b.value - a.value;
        });

    var focus = root,
        nodes = pack(root)
        .descendants(),
        view;

    var circle = g.selectAll("circle")
        .data(nodes)
        .enter()
        .append("circle")
        .attr("class", function (d) {
            if (d.parent) {
                if (d.children) {
                    return "node";
                } else {
                    return "node node--leaf unclickable";
                }
            } else {
                return "node node--root";
            }
        })
        .style("fill", function (d) {
            return d.children ? color(d.depth) : null;
        })
        .on("click", function (d) {
            if (!d.children) {
                console.log(d);
                window.open(d.data.url);
            } else if (focus !== d) {
                zoom(d);
            }
            d3.event.stopPropagation();
        });

    g.selectAll("text")
        .data(nodes)
        .enter()
        .append("text")
        .attr("class", "label")
        .style("fill-opacity", function (d) {
            return d.parent === root ? 1 : 0;
        })
        .style("display", function (d) {
            return d.parent === root ? "inline" : "none";
        })
        .text(function (d) {
            return d.data.name;
        });

    var node = g.selectAll("circle, text"),
        leaf = g.selectAll(".node--leaf");

    svg.on("click", function () {
        zoom(root);
    });

    zoomTo([root.x, root.y, root.r * 2 + margin]);

    function zoom(d) {
        var focus = d;

        var transition = d3.transition()
            .duration(1500)
            .tween("zoom", function (d) {
                var i = d3.interpolateZoom(view, [focus.x, focus.y, focus.r * 2 + margin]);
                return function (t) {
                    zoomTo(i(t));
                };
            });

        if (focus.height === 1) {
            leaf.classed("unclickable", function (d) {
                return d.parent === focus ? false : true;
            });
        } else {
            leaf.classed("unclickable", true);
        }

        transition.selectAll("text")
            .filter(function (d) {
                return d.parent === focus || this.style.display === "inline";
            })
            .style("fill-opacity", function (d) {
                return d.parent === focus ? 1 : 0;
            })
            .on("start", function (d) {
                if (d.parent === focus) this.style.display = "inline";
            })
            .on("end", function (d) {
                if (d.parent !== focus) this.style.display = "none";
            });
    }

    function zoomTo(v) {
        var k = diameter / v[2];
        view = v;
        node.attr("transform", function (d) {
            return "translate(" + (d.x - v[0]) * k + "," + (d.y - v[1]) * k + ")";
        });
        circle.attr("r", function (d) {
            return d.r * k;
        });
    }
}
