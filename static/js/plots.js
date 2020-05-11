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
    fetch(base_url + '/reddit')
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

    console.log('* combined *', combined);
    

    //////////////////////////////////////
    //  Make TimesTag | Google tables!  //
    //////////////////////////////////////

    var makeTables = function(combined) {

        //////////////////////
        // Initialize Table //
        //////////////////////

        var table = d3.select(".times_table")
            , thead = table.append("thead")
            , tbody = table.append("tbody")
            , rows = tbody.selectAll("tr")
            , columnNames = ["Tag", "Frequency", "Most Peack Date", "Overall Trends"]//, "Reddit Comment"]
            , columns = ["tag", "frequency", "busiest", "trendIndex"]

        // append the header row
        thead.append("tr")
            .selectAll("th")
            .data(columnNames)
            .enter()
            .append("th")
            .text(function (d) { return d; });

        ///////////////////////
        // Initialize SVG //
        ///////////////////////


        //////////////////
        // Update Times //
        //////////////////

        var updateTimes = function(filteredTime) {
            selectTime = combined.filter(function(d){
                return d['key'] == filteredTime;
            });
            
        
        // Add rows for new data
        rows.data(selectTime[0].values)
            .enter()
            .append("tr")
            .attr("class", '_' + filteredTime)
            .selectAll("td")
            .data(function (row){
                return columns.map( function (column) {
                    return { column: column, value: row[column] };
                });
            })
            .enter()
            .append('td')
            .html(function (d) {
                // console.log('* column *', d);
                return d.value;
            });
        
        d3.select("tbody").selectAll("tr").each(function(d,i) {
            // Get all classlist
            // console.log("Rows of " + i + " is " + d3.select(this).attr("class"))

            // delete old rows 
            if (d3.select(this).attr("class") != '_' + filteredTime){
                d3.select(this).remove();
            }
            });

            var updateTimes = function(filteredTime) {
                selectTime = combined.filter(function(d){
                    return d['key'] == filteredTime;
                });
                
            console.log('* rows *', selectTime[0].values);
            // var tag_num = selectTime[0].values.length;
            // var count = 0
            
            // Add rows for new data
            rows.data(selectTime[0].values)
                .enter()
                .append("tr")
                .attr("class", '_' + filteredTime)
                .selectAll("td")
                .data(function (row){
                    return columns.map( function (column) {
                        return { column: column, value: row[column] };
                    });
                })
                .enter()
                .append('td')
                .html(function (d) {
                    if (d.value) {

                    }
                    // console.log('* column *', d.column);
                    // console.log('* value *', d.value);
                    return d.value
                });
            
            d3.select("tbody").selectAll("tr").each(function(d,i) {
                // Get all classlist
                // console.log("Rows of " + i + " is " + d3.select(this).attr("class"))
    
                // delete old rows 
                if (d3.select(this).attr("class") != '_' + filteredTime){
                    d3.select(this).remove();
                }
                });
                
            }
        }

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
        
        //////////////////////////////////////////
        // Initialize Times data - recent month //
        //////////////////////////////////////////

        var initialData = combined[0]['key'];
        updateTimes(initialData);

    };

    makeTables(combined);


}).catch(function(err) {
    if (err) return console.warn(err);
});
