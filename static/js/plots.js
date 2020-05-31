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
                    cell.attr('colspan', times_colspan).html('<div><p class="make_small make_bold mb-2">' + flag['date'] + '</p><a href="' + flag['href'] + '" class="text-secondary" target="_blank"><img src=' + flag['img_URL'] + ' width="100%" height="100%"><p class=" pt-2 text_height">' + flag['title'] + ' »</p></div>')
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
                    cell.attr('colspan', youtube_colspan).html('<ul class="pl-1"> <li class="pb-2"><small class="pb-1">Comment: </small>' + flag['commentCount'] + '</li><li class="pb-2"><small>Like: </small>' + flag['likeCount'] + '</li><li class="pb-2"><small>View: </small>' + flag['viewCount'] + '</li>' +' <ul>').attr('class', 'make_small');
                    flag = {};
                }
            } else {
                // console.log('index', index)
                cell.html(d.value).attr('class', 'text_height table-super-narrow');
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
            var margin = {top: 100, bottom: 20},
                height = 800,
                width = 700;
            // console.log('d3', d3.version);
            var parseDate = d3.time.format("%Y-%m-%d").parse
            var formatDate = d3.time.format("%b-%Y")
            var graph_data = []
                for (i = 0; i < google_data[0].length; i++) {
                    graph_data[i] = {
                        'dates': parseDate(google_data[1][i]),
                        'index': google_data[0][i],
                        'busiest': google_data[2]
                    }
                };
            console.log('* graph data * ', graph_data);

            // Set the ranges
            var xScale = d3.time.scale().range([0, width]);
            var yScale = d3.scale.linear().range([height, 0]);
            xScale.domain(d3.extent(graph_data, function(d) {return d.dates; }));
            yScale.domain([0, d3.max(graph_data, function(d) { return d.index; })]);
            
            var color = "#5d7293"; //  Set the color
            const maxY = d3.max(graph_data, function(d) {return d.index;});
            
            // Define the axes
            var xAxis = d3.svg.axis().scale(xScale)
            .orient("bottom").ticks(5).tickFormat(formatDate);
            var yAxis = d3.svg.axis().scale(yScale)
            .orient("left").ticks(10).tickSize(-width);

            // Set the area
            var area = d3.svg.area()
                .x(function(d) {
                  return xScale(d.dates);
                })
                .y0(function(d) {
                    return yScale(0);
                  })
                .y1(function(d) {
                  return yScale(d.index);
                })
                .interpolate("monotone");

            var outline = d3.svg.line()
                .x(function(d) {
                  return xScale(d.dates);
                })
                .y(function(d) {
                  return yScale(d.index);
                });

            var svg = d3.select(this).append("svg")
                .attr("viewBox", `0 0 700 1000`)
                .append("g")
                .attr("transform", "translate(0," + margin.top + ")");
            
            //LINE
            svg.append("path") //select line path within line-group (which represents a vehicle category), then bind new data 
            .attr("class", "line")
            .attr("d", outline(graph_data));
        
            // Add Gradient

            svg.append("path")
                .attr("class", "area")
                .attr("fill", "url(#gradient)")
                .attr("d", area(graph_data));

            svg.append("linearGradient")
                .attr("id", "gradient")
                .attr("gradientUnits", "userSpaceOnUse")
                .attr("x1", 0).attr("y1", yScale(0))
                .attr("x2", 0).attr("y2", yScale(maxY))
                .selectAll("stop")
                .data([{
                    offset: "0%",
                    color: "white" //transparent
                    },
                    {
                    offset: "90%",
                    color: color + "90"
                    },
                    {
                    offset: "100%",
                    color: color
                    }
                ])
                .enter().append("stop")
                .attr("offset", function(d) {
                    return d.offset;
                })
                .attr("stop-color", function(d) {
                    return d.color;
                });
        
            svg.append("g")
                .attr("transform", "translate(0, 800)")
                .attr("class", "x axis")
                .call(xAxis)
                .call(g => {
                    g.selectAll("text")
                    .style("text-anchor", "middle")
                    .attr("y", 30)
                    .attr('fill', '#A9A9A9')
        
                    g.selectAll("line")
                      .attr('stroke', 'black')
                      .attr('stroke-width', 0.7) // make horizontal tick thinner and lighter so that line paths can stand out
                      .attr("y2", 16);
                    g.select(".domain").remove();
        
                   })

            svg.append("g")
                .attr("class", "y axis")
                .call(yAxis)
                .call(g => {
                  g.selectAll("text")
                  .style("text-anchor", "middle")
                  .attr("x", 30)
                  .attr('fill', '#A9A9A9')
      
                  g.selectAll("line")
                    .attr('stroke', '#A9A9A9')
                    .attr('stroke-width', 0.7) // make horizontal tick thinner and lighter so that line paths can stand out
                    .attr('opacity', 0.5)
                    .attr("x1", 50);
      
                  g.select(".domain").remove();
      
                 })
                .append('text')
                  .attr('x', 0)
                  .attr("y", -66)
                  .attr("fill", "#5d7293")
                  .text("Search Interest Index")
                  .style("font-size", '2rem');

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

            ////////////////////////
            // Set the hovor tips //
            ////////////////////////

            // CREATE HOVER TOOLTIP WITH VERTICAL LINE //
            var tooltip = d3.select(this).append("div")
                .style("opacity", 0)
                .attr("class", "tooltip")
                .style('position', 'absolute')
                .style("background-color", "#D3D3D3")
                .style('padding', 6)
                .style('display', 'none')

            var mouseG = svg.append("g")
                .attr("class", "mouse-over-effects");

            mouseG.append("path") // create vertical line to follow mouse
                .attr("class", "mouse-line")
                .style("stroke", "#A9A9A9")
                .style("stroke-width", "4px")
                .style("opacity", "0");

            var mousePerLine = mouseG.selectAll('.mouse-per-line')
                .data(graph_data)
                .enter()
                .append("g")
                .attr("class", "mouse-per-line");

            mousePerLine.append("circle")
                .attr("r", 4)
                .style("class", "line")
                .style("opacity", "0");

            mouseG.append('svg:rect') // append a rect to catch mouse movements on canvas
                .attr('width', width) 
                .attr('height', height)
                .attr('fill', 'none')
                .attr('pointer-events', 'all')
                .on('mouseout', function () { // on mouse out hide line, circles and text
                    d3.select(".mouse-line")
                    .style("opacity", "0");
                    d3.selectAll(".mouse-per-line circle")
                    .style("opacity", "0");
                    d3.selectAll(".mouse-per-line text")
                    .style("opacity", "0");
                    d3.selectAll(".tooltip")
                    .style('display', 'none')

                })
                .on('mouseover', function () { // on mouse in show line, circles and text
                        d3.select(".mouse-line")
                        .style("opacity", "1");
                        d3.selectAll(".mouse-per-line circle")
                        .style("opacity", "1");
                        d3.selectAll("#tooltip")
                        .style('display', 'block')
                    })
                .on('mousemove', function () { // update tooltip content, line, circles and text when mouse moves

                    d3.selectAll(".mouse-per-line")
                    .attr("transform", function (d, i) {
                        const m = d3.mouse(this);
                        var xDate = xScale.invert(m[0]); // use 'invert' to get date corresponding to distance from mouse position relative to svg
                        var bisect = d3.bisectLeft(function (d) { return d.dates; }, xDate) // retrieve row index of date on parsed 
                        
                        d3.select(".mouse-line")
                        .attr("d", function () {
                            var data = "M" + xScale(d.values[idx].date) + "," + (height);
                            data += " " + xScale(d.values[idx].date) + "," + 0;
                            return data;
                        });
                        return "translate(" + xScale(d.values[idx].date) + "," + yScale(d.values[idx].premium) + ")";

                    });

                    updateTooltipContent(mouse, graph_data)

                })

            function updateTooltipContent(mouse, graph_data) {

            sortingObj = []
            graph_data.map(d => {
                var xDate = xScale.invert(mouse[0])
                var bisect = d3.bisector(function (d) { return d.date; }).left
                var idx = bisect(d.values, xDate)
                sortingObj.push({key: d.values[idx].vehicle_class, premium: d.values[idx].premium, bidding_no: d.values[idx].bidding_no, year: d.values[idx].date.getFullYear(), month: monthNames[d.values[idx].date.getMonth()]})
            })

            sortingObj.sort(function(x, y){
                return d3.descending(x.premium, y.premium);
            })

            var sortingArr = sortingObj.map(d=> d.key)

            var graph_data1 = graph_data.slice().sort(function(a, b){
                return sortingArr.indexOf(a.key) - sortingArr.indexOf(b.key) // rank vehicle category based on price of premium
            })

            tooltip.html(sortingObj[0].month + "-" + sortingObj[0].year + " (Bidding No:" + sortingObj[0].bidding_no + ')')
                .style('display', 'block')
                .style('left', d3.event.pageX + 20)
                .style('top', d3.event.pageY - 20)
                .style('font-size', 11.5)
                .selectAll()
                .data(graph_data1).enter() // for each vehicle category, list out name and price of premium
                .append('div')
                .style('color', d => {
                return color(d.key)
                })
                .style('font-size', 10)
                .html(d => {
                var xDate = xScale.invert(mouse[0])
                var bisect = d3.bisector(function (d) { return d.date; }).left
                var idx = bisect(d.values, xDate)
                return d.key.substring(0, 3) + " " + d.key.slice(-1) + ": $" + d.values[idx].premium.toString()
                })
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
    console.log('* initialData * ', initialData)
    makeTables(initialData);

}).catch(function(err) {
    if (err) return console.warn(err);
});
