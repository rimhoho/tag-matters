// import { scaleLinear } from "d3"

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
    // fetch(base_url + '/month')
])
.then(resp => Promise.all( resp.map(r => r.json()) ))
.then(([times, google, youtube, tagbyperiode, frequency]) => {

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

    var makeTables = function(filteredTime) {

        console.log(filteredTime);
        selectTime = combined.filter(function(d){
            return d['key'] == filteredTime;
        });
        convert_Youtube = selectTime[0].values.concat(youtube);

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
        console.log('* times_google_youtube *', times_google_youtube);

        //////////////////////
        // Initialize Table //
        //////////////////////

        var thead_pre = table.append("thead").attr("class", '_' + filteredTime)
            , tbody = table.append("tbody").attr("class", '_' + filteredTime)
            , times_colspan = 4
            , youtube_colspan = 3
            , columnNames_1 = ["New York Times", "", ""]
            , columnNames_2 = ["Tag", "News", "Frequency"]
            , columns = ["tag", "title", "date", "img_URL", "url", "frequency"]
            , youtube_columns = ["commentCount", "likeCount", "viewCount"]
            , google_columns = ['trendIndex', 'trendDate', 'busiest']
            , color = "#5d7293"; //  Set the color;
        
        // append the first header row
        thead_pre
            .append("tr")
            .selectAll("th")
            .data(columnNames_1)
            .enter()
            .append("th")
            .each(function (d) {
                var col = d3.select(this);
                if (d == 'New York Times') {
                    col.attr('colspan', 6).attr("class", "heading").text(d);
                } else {
                    col.attr('colspan', youtube_colspan).attr("class", "no-line").text(d);
                }
            });
        
        // append the second header row
        var thead = thead_pre.append("tr");

        thead.selectAll("th")
            .data(columnNames_2)
            .enter()
            .append("th")
            .each(function (d) {
                var col = d3.select(this);
                if (d == 'News') {
                    col.attr('colspan', times_colspan).text(d);
                } else {
                    col.text(d);
                }
            });

        // Add rows for new data
        var rows = tbody.selectAll("tr")
            .data(times_google_youtube)
            .enter()
            .append("tr");

        var flag = {};

        rows
            .selectAll("td.times")
            .attr("class", 'times')
            .data(function (row){
                return columns.map( function (column) {
                    return { column: column, value: row[column]};
                });
            })
            .enter()
            .append('td').attr('class', 'table-narrow')
            .each(function (d, index) {
                var cell = d3.select(this);
                if (d.column == 'title' || d.column == 'url' || d.column == 'date' || d.column == 'img_URL') {
                    if (d.column == 'title'){
                        var Ttitle = d.value;
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
                        cell.attr('colspan', times_colspan).html('<div><p class="make_bold mb-2">' + flag['date'] + '</p><a href="' + flag['href'] + '" class="text-dark" target="_blank"><img src=' + flag['img_URL'] + ' width="100%" height="100%"><p class=" pt-2 text_height">' + flag['title'] + ' »</p></div>')
                        flag = {};
                    }
                } else {
                    // console.log('index', index)
                    if (typeof(d.value) == 'number') {
                        cell.html(d3.format(',')(d.value)).attr('class', 'text_height table-super-narrow');
                    } else {
                        cell.html(d.value).attr('class', 'text_height table-super-narrow');
                    }
                }
                
                if (index > 0 && index < 4) {
                    cell.remove(); // except 0 4 5 
                }
            });

        //////////////////
        // Create Graph //
        //////////////////

        // 1. Update Thead (add google column with graphs)
        thead
            .append("th").attr('colspan', 3).text('Google Search Trends');
        
        // Use a class so you don't re-select the existing <td> elements
        rows
            .selectAll("td.google-graph")
            .data(function (row, index){
                var arr = [];
                return google_columns.map( function (column) {
                    arr.push(row[column]);
                    return arr;
                });
            })
            .enter()
            .append('td')
            .attr("class", "google-graph")
            .attr('colspan', 3)
            .each(function (google_data, index) {
                // index= google_data[0], dates = google_data[1], busiest_Day = google_data[2]

                if (index == 0) {
                    var margin = {top: 6, bottom: 20},
                        height = 32,
                        width = 80;
                    // console.log('d3', d3.version);
                    var parseDate = d3.time.format("%Y-%m-%d").parse
                    var formatDate = d3.time.format("%b-%Y")
                    var google_graph = []
                        for (i = 0; i < google_data[0].length; i++) {
                            google_graph[i] = {
                                'dates': parseDate(google_data[1][i]),
                                'index': google_data[0][i],
                                'busiest': google_data[2]
                            }
                        };

                    // Set the ranges
                    var xScale = d3.time.scale().range([0, width]);
                    var yScale = d3.scale.linear().range([height, 0]);
                    xScale.domain(d3.extent(google_graph, function(d) {return d.dates; }));
                    yScale.domain([0, d3.max(google_graph, function(d) { return d.index; })]);
                    
                    const maxY = d3.max(google_graph, function(d) {return d.index;});
                    
                    // Define the axes
                    var xAxis = d3.svg.axis().scale(xScale)
                    .orient("bottom").ticks(5).tickFormat(formatDate);
                    var yAxis = d3.svg.axis().scale(yScale)
                    .orient("left").ticks(5).tickSize(-width);

                    // Set the area
                    var area = d3.svg.area()
                        .x(function(d) {return xScale(d.dates);})
                        .y0(function(d) {return yScale(0);})
                        .y1(function(d) {return yScale(d.index);})
                        .interpolate("monotone");

                    var outline = d3.svg.line()
                        .x(function(d) {return xScale(d.dates);})
                        .y(function(d) {return yScale(d.index);});

                    var svg = d3.select(this).append("svg")
                        .attr("viewBox", `0 0 80 50`)
                        .append("g")
                        .attr("transform", "translate(0," + margin.top + ")");

                    // LINE
                    svg.append("path") //select line path within line-group (which represents a vehicle category), then bind new data 
                        .attr("class", "line")
                        .attr("d", outline(google_graph));
                
                    // Add Gradient
                    svg.append("path")
                        .attr("class", "area")
                        .attr("fill", "url(#gradient)")
                        .attr("d", area(google_graph));

                    svg.append("linearGradient")
                        .attr("id", "gradient")
                        .attr("gradientUnits", "userSpaceOnUse")
                        .attr("x1", 0).attr("y1", yScale(0))
                        .attr("x2", 0).attr("y2", yScale(maxY))
                        .selectAll("stop")
                        .data([{offset: "0%",color: color + "20"},{offset: "40%",color: color + "60"},{offset: "100%",color: color}
                        ])
                        .enter().append("stop")
                        .attr("offset", function(d) {return d.offset;
                        })
                        .attr("stop-color", function(d) {return d.color;
                        });
                
                    // svg.append("g")
                    //     .attr("transform", "translate(0, )")
                    //     .attr("class", "x axis")
                    //     .call(xAxis)
                    //     .call(g => {
                    //         g.selectAll("text")
                    //         .style("text-anchor", "middle")
                    //         .attr("y", 30)
                    //         .attr('fill', '#A9A9A9')
                
                    //         g.selectAll("line")
                    //         .attr('stroke', '#A9A9A9')
                    //         .attr('stroke-width', 0.7) // make horizontal tick thinner and lighter so that line paths can stand out
                    //         .attr('opacity', 0.5)
                    //         .attr("y2", 2);
                    //         g.select(".domain").remove();
                    //     })

                    svg.append("g")
                        .attr("class", "y axis")
                        .call(yAxis)
                        .call(g => {
                            g.selectAll("text")
                            .style("text-anchor", "middle")
                            .attr("x", 2)
                            .attr('fill', '#A9A9A9')
                
                            g.selectAll("line")
                                .attr('stroke', '#A9A9A9')
                                .attr('stroke-width', 0.1) // make horizontal tick thinner and lighter so that line paths can stand out
                                .attr('opacity', 1)
                                .attr("x1", 2);
                
                            g.select(".domain").remove();
                        })

                    var toolTip = svg.append("div").attr("class", "toolTip");

                    svg.on("mouseover", function(d) {
                        console.log("left", window.pageXOffset + matrix.e + 15);
                        console.log("top", window.pageYOffset + matrix.f - 30);

                        var matrix = this.getScreenCTM()
                            .translate(+ this.getAttribute("cx"), + this.getAttribute("cy"));
                        toolTip.html(d)
                            .style("left", (window.pageXOffset + matrix.e + 15) + "px")
                            .style("top", (window.pageYOffset + matrix.f - 30) + "px");
                    })
                    
                    // svg.on("mouseout", function(d){
                    //     toolTip.style("display", "none");
                    //     });
                } else {
                    d3.select(this).remove();
                }
                delete_oldRows(index, filteredTime);
        });

        // 2. Update Thead (add Youtube column with graphs)
        thead.append("th").attr('colspan', 3).text("Youtube Stats");

        // Use a class so you don't re-select the existing <td> elements
        rows.selectAll("td.youtube-graph")
        .data(function (row){
            return youtube_columns.map( function (column) {
                // console.log('index: ', column);
                if (column == 'commentCount') {
                   return { column: column, value: row['youtube'][0]};
                } else if (column == 'viewCount') {
                   return { column: column, value: row['youtube'][1]};
                } else if (column =='likeCount') {
                   return { column: column, value: row['youtube'][2]};
                }
            });
        })
        .enter()
        .append('td')
        .attr("class", "youtube-graph")
        .each(function (youtube_data, index) {
            
            var youtube_graph = []

            if (youtube_data.column == 'commentCount'){
                var YcommentCount = youtube_data.value;
                flag['commentCount'] = YcommentCount
            } else if (youtube_data.column == 'viewCount'){
                var YviewCount = youtube_data.value;
                flag['viewCount'] = YviewCount
            } else if (youtube_data.column == 'likeCount'){
                var YlikeCount = youtube_data.value;
                flag['likeCount'] = YlikeCount
            }
        
            if (Object.keys(flag).length == youtube_colspan) {
                youtube_graph = [
                    {label:'commentCount', value: flag['commentCount']},
                    {label: 'likeCount', value: flag['likeCount']},
                    {label: 'viewCount', value: flag['viewCount']}
                ]
                flag = {};
            };
            if (index == 2) {

                // Set the ranges
                var axisMargin = 20,
                        margin = 0,
                        valueMargin = 30,
                        width = 400,
                        height = 800,
                        barHeight = 30,
                        barPadding = (height-axisMargin-margin)*0.8/youtube_graph.length,
                        bar, svg, scale, xAxis, labelWidth = 48;

                // max = d3.max(youtube_graph, function(d) { return d.value; });
                var comment_max = [], like_max = [], view_max = [];

                times_google_youtube.forEach( d => {
                    comment_max.push(d['youtube'][0])
                    like_max.push(d['youtube'][1])
                    view_max.push(d['youtube'][2])
                });
                max = d3.max(view_max);

                svg = d3.select(this)
                        .append("svg")
                        .attr("viewBox", `0 0 200 120`);
                        
                bar = svg.selectAll("g")
                        .data(youtube_graph)
                        .enter()
                        .append("g");

                bar.attr("class", "bar")
                    .attr("cx",0)
                    .attr("transform", function(d, i) {
                        if (i == 2) {
                            return "translate(" + margin + "," + (i * (barHeight + barPadding) - 402)+ ")";
                        } else if (i == 1){
                            return "translate(" + margin + "," + (i * (barHeight + barPadding) - 200)+ ")";
                        } else {
                            return "translate(" + margin + "," + (i * (barHeight + barPadding))+ ")";
                        }
                    });

                bar.append("text")
                    .attr("class", "label make_small")
                    .attr("y", barHeight / 2)
                    .attr("dy", ".35em") //vertical align middle
                    .text(function(d){
                        if (d.label == "commentCount") {
                            return 'Comment'
                        } else if (d.label == "viewCount") {
                            return 'View'
                        } else {
                            return 'Like'
                        }
                    })
                    .each(function() {
                    labelWidth = Math.ceil(Math.max(labelWidth, this.getBBox().width));
                    });
                
                // bar.append('svg:image')
                //     .attr({
                //         'xlink:href': 'http://www.iconpng.com/png/beautiful_flat_color/computer.png',  // can also add svg file here
                //         x: 0,
                //         y: barHeight / 2,
                //         width: '100%',
                //         height: '100%'
                //         })
                //     .each(function() {
                //         labelWidth = Math.ceil(Math.max(labelWidth, this.getBBox().width));
                //         });

                scale = d3.scale.linear()
                        .domain([0, max])
                        .range([0, width - margin - labelWidth]);

                xAxis = d3.svg.axis()
                        .scale(scale)
                        .tickSize(-height + 2*margin + axisMargin)
                        .orient("bottom");

                bar.append("rect")
                    .attr("transform", "translate("+labelWidth+", 0)")
                    .attr("height", barHeight)
                    .attr("width", function(d, i){
                        if (i != 2 ) {
                            return Math.max(3, scale(d.value)*0.3);
                        } else {
                            // console.log('view: ', d.value, 'or ',scale(d.value), 'or ', scale(d.value)*0.2)
                            return 150;
                        }
                    })
                    .style("fill", d => {
                        if (d.value == d3.max(comment_max) || d.value == d3.max(like_max) || d.value == d3.max(view_max)) {
                            return 'tomato';
                        }
                        return color;
                    });

                bar.append("text")
                    .attr("class", "value")
                    .attr("y", barHeight / 2)
                    .attr("dx", -valueMargin + labelWidth) //margin right
                    .attr("dy", ".35em") //vertical align middle
                    .attr("text-anchor", "end")
                    .text(function(d, i){
                        return d3.format(',')(d.value);
                    })
                    .attr("x", function(d, i){
                        var width = this.getBBox().width + 10;
                        scale_value = scale(d.value)*0.38;
                        // console.log('Which one is Max? ', width+valueMargin, 'vs ', scale_value)
                        if (i == 2) {
                            return Math.max(width + valueMargin, 175);
                        } else {
                            return Math.max(width + valueMargin, scale_value);
                        }
                    });
        
                } else {
                    d3.select(this).remove();
                }
                delete_oldRows(index, filteredTime);
            })
    };
    var delete_oldRows = function(index, filteredTime){    
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
    };

    var updateTimes = function(filteredTime) {
        selectTime = combined.filter(function(d){
            return d['key'] == filteredTime;
        });
        makeTables(selectTime[0]['key']);
    };

    var initialData = combined[0]['key'];
    console.log('* initialData * ', initialData)

    // Call the table
    makeTables(initialData);

    // Create a list Under the table

    console.log(tagbyperiode)
    console.log(frequency)

}).catch(function(err) {
    if (err) return console.warn(err);
});




            ////////////////////////
            // Set the hovor tips //
            ////////////////////////

            // CREATE HOVER TOOLTIP WITH VERTICAL LINE //
            // var tooltip = d3.select(this).append("div")
            //     .style("opacity", 0)
            //     .attr("class", "tooltip")
            //     .style('position', 'absolute')
            //     .style("background-color", "#D3D3D3")
            //     .style('padding', 6)
            //     .style('display', 'none')

            // var mouseG = svg.append("g")
            //     .attr("class", "mouse-over-effects");

            // mouseG.append("path") // create vertical line to follow mouse
            //     .attr("class", "mouse-line")
            //     .style("stroke", "#A9A9A9")
            //     .style("stroke-width", "4px")
            //     .style("opacity", "0");

            // var mousePerLine = mouseG.selectAll('.mouse-per-line')
            //     .data(times_google_youtube)
            //     .enter()
            //     .append("g")
            //     .attr("class", "mouse-per-line");

            // mousePerLine.append("circle")
            //     .attr("r", 4)
            //     .style("class", "line")
            //     .style("opacity", "0");

            // mouseG.append('svg:rect') // append a rect to catch mouse movements on canvas
            //     .attr('width', width) 
            //     .attr('height', height)
            //     .attr('fill', 'none')
            //     .attr('pointer-events', 'all')
            //     .on('mouseout', function () { // on mouse out hide line, circles and text
            //         d3.select(".mouse-line")
            //         .style("opacity", "0");
            //         d3.selectAll(".mouse-per-line circle")
            //         .style("opacity", "0");
            //         d3.selectAll(".mouse-per-line text")
            //         .style("opacity", "0");
            //         d3.selectAll(".tooltip")
            //         .style('display', 'none')

            //     })
            //     .on('mouseover', function () { // on mouse in show line, circles and text
            //             d3.select(".mouse-line")
            //             .style("opacity", "1");
            //             d3.selectAll(".mouse-per-line circle")
            //             .style("opacity", "1");
            //             d3.selectAll("#tooltip")
            //             .style('display', 'block')
            //         })
            //     .on('mouseover', function () { // update tooltip content, line, circles and text when mouse moves
            //         var mouse = d3.mouse(this);

            //         d3.selectAll(".mouse-per-line")
            //         .attr("transform", function (d) {
            //             var xDate = xScale.invert(mouse[0]); // use 'invert' to get date corresponding to distance from mouse position
            //             var yIndex = yScale.invert(mouse[1]);
            //             console.log('* xDate: ', xDate);
            //             console.log('* yIndex: ', yIndex);

            //             var bisect = d3.bisector(d => d.trendDate) // retrieve row index of date on parsed csv
            //             const idx = bisect.left(d.trendDate, xDate);

            //             d3.select(".mouse-line")
            //             .attr("d", function () {
            //                 var data = "M" + xScale(idx) + "," + (height);
            //                 data += " " + xScale(idx) + "," + 0;
            //                 return data;
            //             });
            //             return "translate(" + xScale(idx) + "," + yScale(yIndex) + ")";
            //         });

            //         // updateTooltipContent(mouse, times_google_youtube)

            //     })

            // function updateTooltipContent(mouse, times_google_youtube) {

            // sortingObj = []
            // times_google_youtube.map(d => {
            //     var xDate = xScale.invert(mouse[0])
            //     var bisect = d3.bisector(function (d) { return d.date; }).left
            //     var idx = bisect(d.values, xDate)
            //     sortingObj.push({key: d.values[idx].vehicle_class, premium: d.values[idx].premium, bidding_no: d.values[idx].bidding_no, year: d.values[idx].date.getFullYear(), month: monthNames[d.values[idx].date.getMonth()]})
            // })

            // sortingObj.sort(function(x, y){
            //     return d3.descending(x.premium, y.premium);
            // })

            // var sortingArr = sortingObj.map(d=> d.key)

            // var times_google_youtube1 = times_google_youtube.slice().sort(function(a, b){
            //     return sortingArr.indexOf(a.key) - sortingArr.indexOf(b.key) // rank vehicle category based on price of premium
            // })

            // tooltip.html(sortingObj[0].month + "-" + sortingObj[0].year + " (Bidding No:" + sortingObj[0].bidding_no + ')')
            //     .style('display', 'block')
            //     .style('left', d3.event.pageX + 20)
            //     .style('top', d3.event.pageY - 20)
            //     .style('font-size', 11.5)
            //     .selectAll()
            //     .data(times_google_youtube1).enter() // for each vehicle category, list out name and price of premium
            //     .append('div')
            //     .style('color', d => {
            //     return color(d.key)
            //     })
            //     .style('font-size', 10)
            //     .html(d => {
            //     var xDate = xScale.invert(mouse[0])
            //     var bisect = d3.bisector(function (d) { return d.date; }).left
            //     var idx = bisect(d.values, xDate)
            //     return d.key.substring(0, 3) + " " + d.key.slice(-1) + ": $" + d.values[idx].premium.toString()
            //     })
            // }