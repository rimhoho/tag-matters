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
    // fetch(base_url + '/tagbyperiode'),
    // fetch(base_url + '/frequency'),
    // fetch(base_url + '/month')
])
.then(resp => Promise.all( resp.map(r => r.json()) ))
.then(([times, google, youtube]) => {

    var combined_pre_data = [];
    google.forEach((g_item, index) => {
        const t_item = times[index];
        var google_times =  Object.assign(t_item, g_item)
        combined_pre_data.push(google_times);
      });
   
    // Create grouping data sorting by category and tag using d3.nest
    var combined = d3.nest()
        .key(function(d) { return d.periode; })
        .entries(combined_pre_data);

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
    console.log('* youtube * ',youtube );

    var makeTables = function(filteredTime) {

        console.log(filteredTime);
        selectTime = combined.filter(function(d){
            return d['key'] == filteredTime;
        });
        convert_Youtube = selectTime[0].values.concat(youtube);
        console.log('* selectTime * ', selectTime)
        //////////////////////
        // Initialize Table //
        //////////////////////

        var tbody = table.append("tbody").attr("class", '_' + filteredTime)
            , thead = table.append("thead").attr("class", '_' + filteredTime).append("tr")
            , columnNames = ["Tag", "Recent News", "Frequency", "Youtube"]
            , times_colspan = 4
            , youtube_colspan = 3
            , columns = ["tag", "title", "date", "img_URL", "url", "frequency", "commentCount", "likeCount", "viewCount"]
            , graph_data = ['trendIndex', 'trendDate', 'busiest']

        // append the header row
        thead.selectAll("th")
        .data(columnNames)
        .enter()
        .append("th")
        .each(function (d) {
            var col = d3.select(this);
            if (d == 'Recent News') {
                col.attr('colspan', times_colspan).text(d);
            } else if (d == 'Youtube') {
                col.attr('colspan', youtube_colspan).text(d);
            } else {
                col.text(d);
            }
        });

        var times_google_youtube = [];
        
        convert_Youtube.forEach((item, index) => {
            if (index < 10){
                times_google_youtube.push(item)
            } else {
                times_google_youtube.forEach((times)=>{
                    if (item.tag == times.tag) {
                        times['youtube'] = [item.commentCount, item.viewCount, item.likeCount];
                    } else {
                        if (!item.commentCount) {
                            times['youtube'] = [0, 0, 0];
                        }
                    }
                })
            };
          });
        console.log('* combined *', times_google_youtube);
        // Add rows for new data
        var rows = tbody.selectAll("tr")
        .data(times_google_youtube)
        .enter()
        .append("tr");

        var flag = {};

        rows.selectAll("td")
        .data(function (row){
            return columns.map( function (column) {
                // console.log('index: ', column);
                if (column == 'commentCount') {
                   return { column: column, value: row['youtube'][0]};
                } else if (column == 'viewCount') {
                   return { column: column, value: row['youtube'][1]};
                } else if (column =='likeCount') {
                   return { column: column, value: row['youtube'][2]};
                } else {
                   return { column: column, value: row[column]};
                }
            });
        })
        .enter()
        .append('td').attr('class', 'table-narrow')
        .each(function (d, index) {
            var cell = d3.select(this);
            if (d.column == 'title' || d.column == 'url' || d.column == 'date' || d.column == 'img_URL') {
                if (d.column == 'title'){
                    var Ttitle = d.value;
                    // if (Ttitle.length > 28) {
                    //     Ttitle = Ttitle.slice(0, 27);
                    //     Ttitle = Ttitle + '...';
                    // }
                    flag['title'] = Ttitle;
                } else if (d.column == 'url'){
                    var Thref = d.value;
                    flag['href'] = Thref;
                } else if (d.column == 'date'){
                    var Tdate = d.value;
                    flag['date'] = Tdate;
                } else if (d.column == 'img_URL'){
                    var Timg_URL = d.value;
                    flag['img_URL'] = Timg_URL;
                }
                if (Object.keys(flag).length == times_colspan) {
                    // console.log('index', index)
                    cell.attr('colspan', times_colspan).html('<div><p class="make_small make_bold mb-2">' + flag['date'] + '</p><a href="' + flag['href'] + '" class="text-secondary" target="_blank"><img src=' + flag['img_URL'] + ' width="100%" height="100%"><p class=" pt-2 text_height">' + flag['title'] + '</p></div>')
                    flag = {};
                }
            } else if (d.column == 'commentCount' || d.column == 'likeCount' || d.column == 'viewCount') {
                if (d.column == 'commentCount'){
                    var YcommentCount = d.value;
                    flag['commentCount'] = YcommentCount
                } else if (d.column == 'viewCount'){
                    var YviewCount = d.value;
                    flag['viewCount'] = YviewCount
                } else if (d.column == 'likeCount'){
                    var YlikeCount = d.value;
                    flag['likeCount'] = YlikeCount
                }
                if (Object.keys(flag).length == youtube_colspan) {
                    // console.log('index', index)
                    cell.attr('colspan', youtube_colspan).html('<div> <ul class="pl-1"> <li class="pb-2"><small class="pb-1">Comment: </small>' + flag['commentCount'] + '</li><li class="pb-2"><small>Like: </small>' + flag['likeCount'] + '</li><li class="pb-2"><small>View: </small>' + flag['viewCount'] + '</li>' +' <ul> </div>').attr('class', 'make_small');
                    flag = {};
                }
            } else {
                // console.log('index', index)
                if(index == 0){
                    cell.html(d.value).attr('class', 'text_height table-narrow');
                } else {
                    cell.html(d.value).attr('class', 'text_height');
                }
            }
            
            if (index > 0 && index < 8 && index != 4 && index != 5) {
                cell.remove(); // except 0 4 5 8
            }
        });

        //////////////////
        // Update Graph //
        //////////////////

        // update Thead(add a column with graphs)
        thead.append("th").attr('colspan', 3).text('Google Search');

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
        .each(function (google_data, index) {
            // index= google_data[0], dates = google_data[1], busiest_Day = google_data[2]
            var margin = {top: 400},
                height = 200,
                width = 700;
            var data = []
                for (i = 0; i < google_data[0].length; i++) {
                    data[i] = {
                        'x': i,
                        'y': google_data[0][i]
                    }
                };
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
                .attr("viewBox", `0 0 660 1100`)
                .append("g")
                    .attr("transform", "translate(0," + margin.top + ")")
                .append('path')
                    .attr('class','line')
                    .datum(data)
                    .attr('d', line);

            /////////////////////
            // Delete old rows //
            /////////////////////
            
            if (index > 0) {
                d3.select(this).remove();
            }

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
