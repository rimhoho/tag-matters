// import { csv, json } from 'd3-fetch'


// Base URL logic: If hosted on Heroku, format differently
var host = window.location.hostname;

if (host.includes("heroku")) {
    var base_url = "https://" + host;
} else {
    var base_url = "http://127.0.0.1:5000";
};

Promise.all([
    fetch(base_url + '/times'),
    fetch(base_url + '/google'),
    fetch(base_url + '/youtube'),
    fetch(base_url + '/tagbyperiode'),
    fetch(base_url + '/frequency'),
    fetch(base_url + '/month')
])
.then(resp => Promise.all( resp.map(r => r.json()) ))
.then(([times, google, reddit]) => {

    var combined_pre_data = [];
    google.forEach((g_item, index) => {
        const t_item = times[index];
        // console.log('-------------');
        // console.log('* 1 *', t_item.tag, t_item.periode);
        // console.log('* 2 *', g_item.tag, g_item.periode);
        var google_times =  Object.assign(t_item, g_item)
        combined_pre_data.push(google_times);
      });
   
    // Create grouping data sorting by category and tag using d3.nest
    var combined = d3.nest()
        .key(function(d) { return d.periode; })
        .entries(combined_pre_data);
    
    var new_reddit = d3.nest()
    .key(function(d) { return d.tag; })
    .entries(reddit);

    console.log('* new_reddit *', new_reddit);

    /////////////////////
    // Update dropdown //
    /////////////////////
    
    // Handler for dropdown value change
    var dropdownChange = function() {
        var filteredTime = d3.select(this).property('value');
        updateTimes(filteredTime);
    };

    /////////////////////////
    // Initialize dropdown //
    /////////////////////////

    var select_menu = d3.select("#monthly_selection").on('change', dropdownChange);

    select_menu
    .selectAll("option")
    .data(combined)
    .enter()
    .append("option")
    .attr("value", function(d){
        return d['key'];
    })
    .text(function(d){
        return d['key'];
    });
    
    var table = d3.select(".times_table");

    //////////////////////////////////////
    //  Make TimesTag | Google tables!  //
    //////////////////////////////////////

    var makeTables = function(filteredTime) {

        console.log(filteredTime);
        selectTime = combined.filter(function(d){
            return d['key'] == filteredTime;
        });

        //////////////////////
        // Initialize Table //
        //////////////////////

        var tbody = table.append("tbody").attr("class", '_' + filteredTime)
            , thead = table.append("thead").attr("class", '_' + filteredTime).append("tr")
            , columnNames = ["Tag", "Frequency", "Most Peack Date"]//, "Reddit Comment"]
            , columns = ["tag", "frequency", "busiest"]
            , graph_data = ['trendIndex']

        // append the header row
        thead.selectAll("th")
        .data(columnNames)
        .enter()
        .append("th")
        .text(function (d) { return d; });
            
        // Add rows for new data
        var rows = tbody.selectAll("tr")
        .data(selectTime[0].values)
        .enter()
        .append("tr");

        var cells = rows.selectAll("td")
        .data(function (row){
            return columns.map( function (column) {
                return { column: column, value: row[column] };
            });
        })
        .enter()
        .append('td')
        .text(function (d) {
            return d.value;
        });

        //////////////////
        // Update Graph //
        //////////////////

        // update Thead(add a column with graphs)
        thead.append("th").text('Overall Trends on Google Search');

        //use a class so you don't re-select the existing <td> elements
        rows.selectAll("td.graph")
        .data(function (row){
            var arr = [];
            return graph_data.map( function (column) {
                arr.push(row[column]);
                return arr;
            });
        })
        .enter()
        .append('td')
        .attr("class", "graph")
        .each(lines);
        
        function lines(graph_data) {
            var margin = {top: 6, right: 0, bottom: 6, left: 20},
                height = 110,
                width = 500;
            var data = []
                for (i = 0; i < graph_data[0].length; i++) {
                    data[i] = {
                        'x': i,
                        'y': graph_data[0][i]
                    }
                };
            console.log('* * *', data);
            
            var x = d3.scale.linear()
                .domain(d3.extent(data, function(d) { return d.x; }))
                .range([ 0, width ]);

            //Add Y axis
            var y = d3.scale.linear()
                .domain([0, d3.max(data, function(d) { return d.y; })])
                .range([ height, 0 ]);
            
            var line = d3.svg.line()
                        .x(function(d) {return x(d.x)})
                        .y(function(d) {return y(d.y)}); 

            d3.select(this).append("svg")
                .attr("viewBox", `0 0 ${width} ${height}`)
                .append("g")
                    .attr("transform", "translate(0," + margin.right + ")")
                .append('path')
                    .attr('class','line')
                    .datum(data)
                    .attr('d', line);
        };

        /////////////////////
        // Delete old rows //
        /////////////////////
        
        d3.selectAll("tbody").each(function() {

            if (d3.select(this).attr("class") != '_' + filteredTime){
                d3.select(this).remove();
            }
        });
        
        d3.selectAll("thead").each(function() {

            if (d3.select(this).attr("class") != '_' + filteredTime){
                d3.select(this).remove();
            }
        });

    };

    var updateTimes = function(filteredTime) {
        selectTime = combined.filter(function(d){
            return d['key'] == filteredTime;
        });
        makeTables(selectTime[0]['key']);
    };

    var initialData = combined[0]['key'];
    makeTables(initialData);

}).catch(function(err) {
    if (err) return console.warn(err);
});
