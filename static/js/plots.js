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
            , columnNames_2 = ["Tag", "Most Recent News", "Frequency"]
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
                if (d == 'Most Recent News') {
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
                    var formatDate = d3.time.format("%b %m, %Y")
                    var google_graph = []
                        for (i = 0; i < google_data[0].length; i++) {
                            google_graph[i] = {
                                'dates': parseDate(google_data[1][i]),
                                'index': google_data[0][i],
                                'busiest': google_data[2]
                            }
                        };

                    // Set the ranges
                    var xScale = d3.time.scale().range([0, width]).domain(d3.extent(google_graph, function(d) {return d.dates; }))
                    ,   yScale = d3.scale.linear().range([height, 0]).domain([0, d3.max(google_graph, function(d) { return d.index; })]);
                    
                    const maxY = d3.max(google_graph, function(d) {return d.index;});
                    
                    // Define the axes
                    var xAxis = d3.svg.axis().scale(xScale)
                    .orient("bottom").ticks(3).tickFormat(formatDate);
                    var yAxis = d3.svg.axis().scale(yScale)
                    .orient("left").ticks(4).tickSize(-width);

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
                        .data([{offset: "0%",color: color + "20"},{offset: "40%",color: color + "60"},{offset: "100%",color: color}])
                        .enter().append("stop")
                        .attr("offset", function(d) {return d.offset;})
                        .attr("stop-color", function(d) {return d.color;});
                
                    svg.append("g")
                        .attr("transform", `translate(0, 0)`)
                        .attr("class", "x axis")
                        .call(xAxis)
                        .call(g => {
                            g.selectAll("text")
                                .style("text-anchor", "middle")
                                .attr("y", 34)
                                .attr('fill', '#A9A9A9')
                            g.selectAll("line")
                                .attr('stroke', '#A9A9A9')
                                .attr('stroke-width', 0.3) // make horizontal tick thinner and lighter so that line paths can stand out
                                .attr('opacity', 0.3)
                                .attr("y2", 2);
                            g.select(".domain").remove();
                        })
                    
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
                    

                    /***** For an SVG tooltip *****/ 
                    var mouseG = svg.append("g")
                        .attr("class", "mouse-over-effects");

                    var mouseT = mouseG.append("text")
                        .attr("transform", "translate(7,-3)")
                        .attr("class", "mouse-text")
                        .style("fill", "#5d7293")
                        .style("opacity", "0");

                    mouseG.append("path") // this is the black vertical line to follow mouse
                        .attr("transform", "translate(0,0)")
                        .attr("class", "mouse-line")
                        .style("stroke", "black")
                        .style("stroke-width", 0.4)
                        .style("opacity", "0");

                    mouseG.append('svg:rect') // append a rect to catch mouse movements on canvas
                        .attr('width', width) // can't catch mouse events on a g element
                        .attr('height', height)
                        .attr('fill', 'none')
                        .attr('pointer-events', 'all')
                        .on('mouseover', function() { // on mouse in show line, circles and text
                            d3.select(".mouse-line")
                                .style("opacity", "1");
                        })
                        .on('mousemove', function(data) { // mouse moving over canvas
                            var mouse = d3.mouse(this);
                            var xDate = xScale.invert(mouse[0]),
                                parsedDate = data[1].map( d => parseDate(d)),
                                idx = d3.bisect(parsedDate, xDate); // returns the index to the current data item

                            d3.selectAll(".mouse-line")
                                .attr("d", function() {
                                    var d = "M" + mouse[0] + "," + height;
                                    d += " " + mouse[0] + "," + 0;
                                    return d;
                                })
                                .style("opacity", "1");

                            mouseT
                            .text(`${formatDate(parseDate(data[1][idx]))}: ${data[0][idx]}`)
                            .style("opacity", "1");
                         })
                        .on('mouseout', function() { // on mouse out hide line, circles and text
                            d3.select(".mouse-line")
                                .style("opacity", "0");
                            d3.selectAll(".mouse-text").style("opacity", "0");
                        });
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
                        barHeight = 24,
                        barPadding = (height-axisMargin-margin)*0.8/youtube_graph.length,
                        bar, svg, scale, mouseT, labelWidth = 48;

                var comment_max = [], like_max = [], view_max = [];

                times_google_youtube.forEach( d => {
                    comment_max.push(d['youtube'][0])
                    like_max.push(d['youtube'][2])
                    view_max.push(d['youtube'][1])
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
                
                mouseT = bar.append("text")
                    .attr("transform", "translate(7,-3)")
                    .attr("class", "youtube-text")
                    .style("fill", "#5d7293")
                    .style("opacity", "0");

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
                    
                bar
                .each(function(d) {
                    var icon_color = color;
                    if (d.label == "commentCount") {
                        if(d.value == d3.max(comment_max)){
                            icon_color = '#ff634c';
                        }
                        component = `<svg x="-12px" y="0" viewBox="155.571 399.782 250 200"><path style="fill:${icon_color};" d="M195.571,399.782h-36.667c-1.834,0-3.333,1.5-3.333,3.333v23.333c0,1.834,1.5,3.333,3.333,3.333h17.5 l12.5,10v-10h6.667c1.834,0,3.333-1.5,3.333-3.333v-23.334C198.903,401.282,197.403,399.782,195.571,399.782z M167.166,417.95 c-1.595,0-2.889-1.293-2.889-2.889s1.293-2.889,2.889-2.889c1.596,0,2.889,1.293,2.889,2.889S168.762,417.95,167.166,417.95z  M177.237,417.95c-1.596,0-2.889-1.293-2.889-2.889s1.293-2.889,2.889-2.889c1.595,0,2.889,1.293,2.889,2.889 S178.832,417.95,177.237,417.95z M187.305,417.95c-1.596,0-2.889-1.293-2.889-2.889s1.293-2.889,2.889-2.889 c1.595,0,2.889,1.293,2.889,2.889S188.901,417.95,187.305,417.95z"/></svg>`
                    } else if (d.label == "likeCount") {
                        if(d.value == d3.max(like_max)){
                            icon_color = '#ff634c';
                        }
                        component = `<svg x="-12px" y="0" viewBox="155.571 399.782 250 200"> <path style="fill:${icon_color};" d="M188.994,401.333c-4.337,0-8.162,2.196-10.423,5.536c-2.261-3.341-6.085-5.536-10.423-5.536 c-6.946,0-12.577,5.631-12.577,12.577c0,3.96,1.831,7.492,4.692,9.798l18.308,14.523l18.308-14.523 c2.861-2.305,4.692-5.837,4.692-9.798C201.571,406.964,195.94,401.333,188.994,401.333z"/></svg>`
                    } else {
                        if(d.value == d3.max(view_max)){
                            icon_color = '#ff634c';
                        }
                        component = `<svg x="-12px" y="0" viewBox="155.571 399.782 250 200"><path style="fill:${icon_color};" d="M196.569,404.664c-3.6-0.985-17.998-0.985-17.998-0.985s-14.399,0-17.998,0.948 c-1.933,0.53-3.524,2.122-4.055,4.092c-0.948,3.6-0.948,11.064-0.948,11.064s0,7.503,0.948,11.064 c0.531,1.97,2.084,3.524,4.055,4.055c3.637,0.985,17.998,0.985,17.998,0.985s14.399,0,17.998-0.948 c1.97-0.53,3.524-2.084,4.055-4.054c0.947-3.6,0.947-11.065,0.947-11.065s0.038-7.502-0.947-11.102 C200.093,406.748,198.539,405.194,196.569,404.664z M173.986,426.678v-13.792l11.973,6.896L173.986,426.678z"/> </svg>`
                    }
                    d3.select(this).html(component)
                    .on('mouseover', function(d) { // mouse moving over canvas
                        // console.log('data: ', d.label);
                        if (d.label == "commentCount") {
                            text_label = 'Comment'
                        } else if (d.label == "likeCount") {
                            text_label = 'Like'
                        } else {
                            text_label = 'View'
                        }
                        mouseT
                        .text(text_label)
                        .style("opacity", "1");
                        });
                    });

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
                            return Math.max(2, scale(d.value)*10);
                        } else {
                            // console.log('view: ', d.value, 'or ',scale(d.value), 'or ', scale(d.value)*0.2)
                            return Math.max(150, scale(d.value)*0.3);
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