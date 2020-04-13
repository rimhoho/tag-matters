// import { csv, json } from 'd3-fetch'


// Base URL logic: If hosted on Heroku, format differently
var host = window.location.hostname;

if (host.includes("heroku")) {
    var base_url = "https://" + host;
} else {
    var base_url = "http://127.0.0.1:5000";
};


function dashboard() {
    Promise.all([
        fetch(base_url + '/times'),
        fetch(base_url + '/google')
    ])
    .then(resp => Promise.all( resp.map(r => r.json()) ))
    .then(([times, google]) => {

        // var table = d3.select(".monthly_table")
        //     , columns = ["Tag", "Frequency"]
        //     , thead = table.append("thead")
        //     , tbody = table.append("tbody");

        // // append the header row
        // thead.append("tr")
        //     .selectAll("th")
        //     .data(columns)
        //     .enter()
        //     .append("th")
        //     .text(function (d) { return d; });
        
        // // create a row for each object in the data
        // var rows = tbody.selectAll("tr")
        //     .data(times)//.filter(tag_list => tag_list['Category'] == '2018-03'))
        //     .enter()
        //     .append("tr");

        // // create cells for each object in the data                  
        // rows.selectAll("td")
        //     // data = [{'Tag': '', 'Frequency': '', 'Title': '', 'Date': '', 'Url': '', 'Description': '', 'img_URL': ''},{...}]
        //     .data(function (row) {
        //         return columns.map(function(key) {
        //             if (key == 'Tag' || key == 'Frequency'){
        //                 return row[key];
        //             }
        //         }); 
        //     })
        //     .enter()
        //     .append("td")
        //     .attr("style", "font-family: 'Lato'")
        //     .text(d => d);
        
        // thead.append("tr")
        //     .selectAll("th")
        //     .append("th")
        //     .text('Google Search Trends');

        // create a google json
        var new_google = []
        var date_fields = []

        for (t in google[0]){
            if (t !== 'Tag' && t !== 'Category' && t !== 'Busiest_date') {
                if (typeof google[0][t] === 'string'){
                        date_fields.push(google[0][t])
                }
            }
        }
        console.log('date_fields', date_fields);
        

        google.forEach(function(tag) {
            var tag_dict = {};
            var tags_list = [];
            
            var category = tag['Category'];

            if (category in tag_dict) {
                var each_rate = []
                for (const t in tag){
                    if (t == 'Tag') {
                        var tag_keword = tag[t];
                        // console.log('tag_keword', tag_keword);
                        each_tag['Tag'] = tag_keword;
                    }
                    if (typeof tag[t] == 'number'){
                        // console.log('Rates', tag[t]);
                        each_rate.push(tag[t]);
                    }
                }
                each_tag['Rate'] = each_rate;
                tags_list.push(+each_tag);

            } else {
                tag_dict[category] = []; //[tag['Tag'], tag['Busiest_date']];

                var each_tag = {}
                var each_rate = []
                for (const t in tag){
                    if (t == 'Tag') {
                        var tag_keword = tag[t];
                        // console.log('tag_keword', tag_keword);
                        each_tag['Tag'] = tag_keword;
                    }
                    if (typeof tag[t] == 'number'){
                        // console.log('Rates', tag[t]);
                        each_rate.push(tag[t]);
                    }
                }
                each_tag['Rate'] = each_rate;
                tags_list.push(each_tag);
            }
            
            tag_dict[category].push(tags_list)
            // tag_dict[category].push(date_list, rate_list)
            new_google.push(tag_dict);
        })
        // new_google = [{'2018-01': [{'Tag': 'New York City', 'Rate' : [5, 48]]}, {'Tag': 'United States Politics and Government', 'Rate' : [50, 100]]}]
        console.log('new_google', new_google);
        

        makeVis(new_google)


        var makeVis = new_google => {
            // Define dimensions of vis
            var margin = { top: 4, right: 6, bottom: 4, left: 6 },
                width  = 400 - margin.left - margin.right,
                height = 80 - margin.top  - margin.bottom;

            // Make x scale
            var xScale = d3.scale.ordinal()
                .domain(date_fields)
                .rangeRoundBands([0, width], 0.1);

            // Make y scale, the domain will be defined on bar update
            var yScale = d3.scale.linear()
                .range([height, 0]);

            // Create canvas
            var canvas = d3.select("#vis-container")
              .append("svg")
                .attr("width",  width  + margin.left + margin.right)
                .attr("height", height + margin.top  + margin.bottom)
              .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            // add the line for the searches each month
            // try to set the x values so that they are 
            // roughly in the middle of the header cells
            svgLine.append("path")
                .attr("d", function(d) {
                    return (d3.svg.line()
                                .x(function(dValue,i) {
                                    return theWidth/24 + i*(theWidth/12); 
                                })
                                .y(function(dValue) {
                                    if (d.searchesRange===0) {
                                    //just return the middle
                                    return scaleY(0.5); 
                                    }
                                    else {
                                    var f = (dValue - d.minSearches) /
                                                    (d.searchesRange);
                                    return scaleY(f);
                                    }
                                })
                                //"d.values" is the array of 
                                //  searches for each month
                                .interpolate("linear"))(d.values);
                })
                .attr("stroke","blue")
                .attr("fill","none")
                .attr("stroke-width",1);

            // Make x-axis and add to canvas
            var xAxis = d3.svg.axis()
                .scale(xScale)
                .orient("bottom");

            canvas.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + height + ")")
                .call(xAxis);

            // Make y-axis and add to canvas
            var yAxis = d3.svg.axis()
                .scale(yScale)
                .orient("left");

            var yAxisHandleForUpdate = canvas.append("g")
                .attr("class", "y axis")
                .call(yAxis)
                .orient("left");

            yAxisHandleForUpdate.append("text")
                .attr("transform", "rotate(-90)")
                .attr("y", 6)
                .attr("dy", ".71em")
                .style("text-anchor", "end")
                .text("Value");



            var updateBars = new_google => {
                // First update the y-axis domain to match data
                yScale.domain( d3.extent(new_google) );
                yAxisHandleForUpdate.call(yAxis);

                var bars = canvas.selectAll(".bar").data(data);

                // Add bars for new data
                bars.enter()
                  .append("rect")
                    .attr("class", "bar")
                    .attr("x", function(d,i) { return xScale( date_fields[i] ); })
                    .attr("width", xScale.rangeBand())
                    .attr("y", function(d,i) { return yScale(d); })
                    .attr("height", function(d,i) { return height - yScale(d); });

                // Update old ones, already have x / width from before
                bars
                    .transition().duration(250)
                    .attr("y", function(d,i) { return yScale(d); })
                    .attr("height", function(d,i) { return height - yScale(d); });

                // Remove old ones
                bars.exit().remove();
            };
        };


        // // Handler for dropdown value change
        // var dropdownChange = () => {
        //     var tag = d3.select(this).property('value'),
        //         newData   = new_google[tag];

        //     updateBars(newData);
        // };


        // // Get names of cereals, for dropdown
        // var tags = Object.keys(new_google).sort();

        // var dropdown = d3.select("#vis-container")
        //     .insert("select", "svg")
        //     .on("change", dropdownChange);

        // dropdown.selectAll("option")
        //     .data(tags)
        //     .enter().append("option")
        //     .attr("value", function (d) { return d; })
        //     .text(function (d) {
        //         return d[0].toUpperCase() + d.slice(1,d.length); // capitalize 1st letter
        //     });

        // var initialData = new_google[ tags[0] ];
        
        
        // updateBars(initialData);

        
        

        // // create a select dropdown menu
        // var selection = d3.select("#selectButton")
        //                 .data(data)
        //                 .enter();

        // // add the options to the button
        // selection.selectAll('myOptions')
        // .data(function (row) {
        //     return Object.keys(row).map(function(key) {
        //         if (key == 'Tag' || key == 'Frequency'){
        //             return row[key];
        //         }
        //     }); 
        // })
        // .enter()
        //     .append('option')
        // .text(d => d) // text showed in the menu
        // .attr("value", function (d) {
        //      console.log('Option: ',d);
        //      return d; 
        // }) // corresponding value returned by the button

        // // When the button is changed, run the updateChart function
        // d3.select("#selectButton").on("change", function(d) {
        //     // recover the option that has been chosen
        //     var selectedOption = d3.select(this).property("value")
        //     // run the updateChart function with this selected option
        //     update(selectedOption)
        // })


    }).catch(function(err) {
        if (err) return console.warn(err);
    })

};


dashboard();
