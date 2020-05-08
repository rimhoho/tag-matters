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
        fetch(base_url + '/google'),
        fetch(base_url + '/reddit')
    ])
    .then(resp => Promise.all( resp.map(r => r.json()) ))
    .then(([times, google, reddit]) => {

        // Create grouping data sorting by category and tag using d3.nest
        var d3_times = d3.nest()
            .key(function(d) { return d.periode; })
            .entries(times).reverse();
        var d3_google = d3.nest()
            .key(function(d) { return d.periode; })
            .entries(google).reverse();
        var d3_reddit = d3.nest()
        .key(function(d) { return d.createdDate; })
        .entries(reddit).reverse();
        
        // var combined_data = []
        
        // d3_times.forEach(monthly_dict => {
        //     var monthly_time = monthly_dict.key,
        //         monthly_values = monthly_dict.values,
        //         new_dict = {},
        //         tags_list = [];

        //     new_dict['time'] = monthly_time
            
        //     monthly_values.forEach(monthly_news => {
        //         var tag_dict = {}, tag_infos = [], single_tag = {}, frequency = {}, article = {};
        //         single_tag['Tag'] = monthly_news.key;
        //         frequency['Frequency'] = monthly_news.values[0].Frequency;
        //         article['Date'] = monthly_news.values[0].Date;
        //         article['Title'] = monthly_news.values[0].Title;
        //         article['Url'] = monthly_news.values[0].Url;
        //         article['img_URL'] = monthly_news.values[0].img_URL;
        //         tag_infos.push(article, single_tag, frequency);
        //         tag_dict[monthly_news.key] = tag_infos;
        //         tags_list.push(tag_dict);
        //         new_dict['Tag_list'] = tags_list;
        //     });
        //     combined_data.push(new_dict);
        // });

        // return d3_times;

        // Create initial table
        var table = d3.select(".monthly_table")
            , columns = ["tag", "frequency", "title", "date", "url", "img_URL"]//, "Interest on Google"]//, "Reddit Comment"]
            , thead = table.append("thead")
            , tbody = table.append("tbody");
            
        // append the header row
        thead.append("tr")
            .selectAll("th")
            .data(columns)
            .enter()
            .append("th")
            .text(function (d) { return d; });

        // Create a dropdown
        var select_menu = d3.select("#monthly_selection")

        select_menu
            .selectAll("option")
            .data(d3_times)
            .enter()
            .append("option")
            .attr("value", function(d){
                return d['key'];
            })
            .text(function(d){
                return d['key'];
            })

        // Function to create the initial graph
        var initial_table = function(Time){
            // Filter the data to include only Time of interest
            var selectTime = d3_times.filter(function(d){
                    return d['key'] == Time;
                })
            console.log('* 1 *', selectTime);

            // create a row for each object in the data
            var rows = tbody.selectAll("tr")
                .data(selectTime[0].values)
                .enter()
                .append("tr");
            
            // create cells for each object in the data                  
            rows.selectAll("td")//.filter(":nth-child(1)")
                .data(function (row){
                    // row['values'].forEach(d => {
                    //     // console.log('* 2 *', d);
                    //     return columns.map( function ( column ) {
                    //         console.log('* key *', column);
                    //         console.log('* value *', d[column]);
                    //         return { column: column, value: d[column]};
                    //     } );
                    // })
                    return columns.map( function ( column ) {
                        console.log('* key *', column);
                        console.log('* value *',row[column]);
                        return { column: column, value: row[column] };
                    } );
                } )
                .enter()
                .append('td')
                .html(function (d, i) {
                    console.log('* ', i, ' *', d.value);
                    if (d.column == 'url' ) {
                        return '<a href="' + d.value + '">' + 'The most recent article containing the tag is here</a>';
                    } else if (d.column == 'img_URL') {
                        return '<img src="' + d.value + '" height="120px">';
                    } else {
                        return d.value;
                    }
                })
                .attr("class", (d,i) => d[i].tag);
                
                return table;
        }

        initial_table("2020-05");



        // Update the data
        var updateTable = function(Time){

            // Filter the data to include only Time of interest
            var selectTime = combined_data.filter(function(d){
                return d.key == Time;
                })
            console.log('selectTime', selectTime);

            var rows = tbody.selectAll("tr")
                .data(selectTime)
                .enter()
                .append("tr")

            // create cells for each object in the data                  
            rows.selectAll("td").filter(":first-child")
                .data(function(d){
                    var d_arr = []
                    console.log('updated td: ', d);
                    d_arr.push(d)
                    return d_arr;})
                .enter()
                .append("td")
                .attr("style", "font-family: 'Lato'")
                .text(function(d){
                    console.log('td-text: ', Object.keys(d));
                    return Object.keys(d);});

            rows.selectAll("td").filter(":nth-child(2)")
                .data(function(d){
                    var d_arr = []
                    // console.log('td: ', d);
                    d_arr.push(d)
                    return d_arr;})
                .enter()
                .append("td")
                .attr("style", "font-family: 'Lato'")
                .text(function(d){
                    // console.log('Frequency: ', d.Frequency);
                    return d.Frequency;})
            
        }          

        // Run update function when dropdown selection changes
        select_menu.on('change', function(){

            // Find which fruit was selected from the dropdown
            var selectedTime = d3.select(this).property("value")
            // .select("select")
            

            console.log('Selection!!: ', selectedTime)
            // Run update function with the selected Time
            updateTable(selectedTime)

        });


        

        
        // create a google json
        // var date_fields = []
        // 

        // for (t in google[0]){
        //     if (t !== 'Tag' && t !== 'Category' && t !== 'Busiest_date') {
        //         if (typeof google[0][t] === 'string'){
        //                 date_fields.push(google[0][t])
        //         }
        //     }
        // }
        

        // makeVis(google_tag)


        // var makeVis = google_tag => {
        //     // Define dimensions of vis
        //     var margin = { top: 4, right: 6, bottom: 4, left: 6 },
        //         width  = 400 - margin.left - margin.right,
        //         height = 80 - margin.top  - margin.bottom;

        //     // Make x scale
        //     var xScale = d3.scale.ordinal()
        //         .domain(date_fields)
        //         .rangeRoundBands([0, width], 0.1);

        //     // Make y scale, the domain will be defined on bar update
        //     var yScale = d3.scale.linear()
        //         .range([height, 0]);

        //     // Create canvas
        //     var canvas = d3.select("#vis-container")
        //       .append("svg")
        //         .attr("width",  width  + margin.left + margin.right)
        //         .attr("height", height + margin.top  + margin.bottom)
        //       .append("g")
        //         .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        //     // add the line for the searches each month
        //     // try to set the x values so that they are 
        //     // roughly in the middle of the header cells
        //     svgLine.append("path")
        //         .attr("d", function(d) {
        //             return (d3.svg.line()
        //                         .x(function(dValue,i) {
        //                             return theWidth/24 + i*(theWidth/12); 
        //                         })
        //                         .y(function(dValue) {
        //                             if (d.searchesRange===0) {
        //                             //just return the middle
        //                             return scaleY(0.5); 
        //                             }
        //                             else {
        //                             var f = (dValue - d.minSearches) /
        //                                             (d.searchesRange);
        //                             return scaleY(f);
        //                             }
        //                         })
        //                         //"d.values" is the array of 
        //                         //  searches for each month
        //                         .interpolate("linear"))(d.values);
        //         })
        //         .attr("stroke","blue")
        //         .attr("fill","none")
        //         .attr("stroke-width",1);

        //     // Make x-axis and add to canvas
        //     var xAxis = d3.svg.axis()
        //         .scale(xScale)
        //         .orient("bottom");

        //     canvas.append("g")
        //         .attr("class", "x axis")
        //         .attr("transform", "translate(0," + height + ")")
        //         .call(xAxis);

        //     // Make y-axis and add to canvas
        //     var yAxis = d3.svg.axis()
        //         .scale(yScale)
        //         .orient("left");

        //     var yAxisHandleForUpdate = canvas.append("g")
        //         .attr("class", "y axis")
        //         .call(yAxis)
        //         .orient("left");

        //     yAxisHandleForUpdate.append("text")
        //         .attr("transform", "rotate(-90)")
        //         .attr("y", 6)
        //         .attr("dy", ".71em")
        //         .style("text-anchor", "end")
        //         .text("Value");



        //     var updateBars = google_tag => {
        //         // First update the y-axis domain to match data
        //         yScale.domain( d3.extent(google_tag) );
        //         yAxisHandleForUpdate.call(yAxis);

        //         var bars = canvas.selectAll(".bar").data(data);

        //         // Add bars for new data
        //         bars.enter()
        //           .append("rect")
        //             .attr("class", "bar")
        //             .attr("x", function(d,i) { return xScale( date_fields[i] ); })
        //             .attr("width", xScale.rangeBand())
        //             .attr("y", function(d,i) { return yScale(d); })
        //             .attr("height", function(d,i) { return height - yScale(d); });

        //         // Update old ones, already have x / width from before
        //         bars
        //             .transition().duration(250)
        //             .attr("y", function(d,i) { return yScale(d); })
        //             .attr("height", function(d,i) { return height - yScale(d); });

        //         // Remove old ones
        //         bars.exit().remove();
        //     };
        // };


        // // Handler for dropdown value change
        // var dropdownChange = () => {
        //     var tag = d3.select(this).property('value'),
        //         newData   = google_tag[tag];

        //     updateBars(newData);
        // };


        // // Get names of cereals, for dropdown
        // var tags = Object.keys(google_tag).sort();

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

        // var initialData = google_tag[ tags[0] ];
        
        
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
