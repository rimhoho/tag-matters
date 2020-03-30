// Base URL logic: If hosted on Heroku, format differently
var host = window.location.hostname;
if (host.includes("heroku")) {
    var base_url = "https://" + host;
} else {
    var base_url = "http://127.0.0.1:5000";
}

function init() {
    endpoint = base_url + '/init';
    d3.csv(endpoint, function (error, data) {
        console.log('data: ', data);
        if (error) return console.warn(error);

        // main_table
        var table = d3.select(".monthly_table")
            , columns = ["Tag", "Frequency", "Google Search Trends", "Emotions"]
            , thead = table.append("thead")
            , tbody = table.append("tbody");

        // append the header row
        thead.append("tr")
            .selectAll("th")
            .data(columns)
            .enter()
            .append("th")
            .text(function (d) { return d; });

        // create a row for each object in the data
        var rows = tbody.selectAll("tr")
            .data(data)
            .enter()
            .append("tr");
        
        // create cells for each object in the data                  
        rows.selectAll("td")
            // data = [{'Tag': '', 'Frequency': '', 'Title': '', 'Date': '', 'Url': '', 'Description': '', 'img_URL': ''},{...}]
            .data(function (row) {
                console.log('row: ', row);
                col_only = ["Tag", "Frequency"];
                return col_only.map(function(key) {
                    return {
                        key: key,
                        value: row[key]
                    };
                });
            })
            .enter()
            .append("td")
            .attr("style", "font-family: 'Lato'")
            .text(function (d) { 
                    console.log('d.value: ', d.value);
                    return d.value;       
            })

        // create a graph cell in last row for each column
        // var Graphcells = rows.append("td")
        //     .attr("colspan",12)
        //     .append("div")
        //     .style("height","100%")
        //     .style("width","100%");      
        
        //     var theWidth = (Graphcells.style("width"));
        //     var theHeight = 40; // doesn't work:Graphcells.style("height");
    
        //     //add the svg element with the desired width and height
        //     var svgLine = Graphcells
        //                 .append("svg")
        //                 .attr("width",theWidth)
        //                 .attr("height",theHeight)
        //                 .attr("class","svgCell");
    
        //     //helper function - I should change this to use D3's built-in
        //     //   scaling functions.  Did lots of silly putzing with this.
        //     var scaleY = function(fraction) {
        //             //  0 --> height - 4
        //             //  1 --> 4
        //             return (8-theHeight)*fraction + (theHeight-4);
        //     };
    
        //     //add the line for the searches each month
        //     //try to set the x values so that they are 
        //     // roughly in the middle of the header cells
        //     svgLine.append("path")
        //            .attr("d", 
        //              function(d) {
        //               return (d3.svg.line()
        //                             .x(function(dValue,i) {
        //                                 return theWidth/24 + i*(theWidth/12); 
        //                              })
        //                              .y(function(dValue) {
        //                                  if (d.searchesRange===0) {
        //                                   //just return the middle
        //                                   return scaleY(0.5); 
        //                                  }
        //                                  else {
        //                                   var f = (dValue - d.minSearches) /
        //                                                   (d.searchesRange);
        //                                   return scaleY(f);
        //                                  }
        //                              })
        //                              //"d.values" is the array of 
        //                              //  searches for each month
        //                              .interpolate("linear"))(d.values);
        //                         })
        //                 .attr("stroke","blue")
        //                 .attr("fill","none")
        //                 .attr("stroke-width",1);

        return table;
    });
};

init();