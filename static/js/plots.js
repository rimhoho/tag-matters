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
    fetch(base_url + '/youtube')
])
.then(resp => {
    console.log(resp);
    return Promise.all( resp.map(r => r.clone().json()) )
})
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

    var makeTables = function(filteredTime) {

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
                        times['youtube'] = [item.commentCount, item.viewCount, item.likeCount, {img_url: item.img_url, url: item.url, title: item.title}];
                    }
                })
            };
          });

        //////////////////////
        // Initialize Table //
        //////////////////////

        var thead = table.append("thead").attr("class", '_' + filteredTime).append("tr"),
            tbody = table.append("tbody").attr("class", '_' + filteredTime),
            times_colspan = 4,
            youtube_colspan = 3,
            columnNames = ["TOP 10 TAGS", "COUNTS", "NEW YORK TIMES"],
            columns = ["tag", "frequency", "title", "date", "img_URL", "url"],
            youtube_columns = ["viewCount", "commentCount", "likeCount", "video"],
            google_columns = ['trendIndex', 'trendDate', 'busiest'],
            youtube_graph = [],
            color = "#5d7293"; //  Set the color;

        thead.selectAll("th")
            .data(columnNames)
            .enter()
            .append("th")
            .each(function (d) {
                var col = d3.select(this);
                if (d == 'NEW YORK TIMES') {
                    col.attr('colspan', times_colspan).text(d).attr("class", "pb-4 heading thead-line");
                } else if (d == 'TOP 10 TAGS') {
                    col.text(d).attr("class", "left-align pb-4 heading thead-line tag-col");
                } else {
                    col.text(d).attr("class", "right-align pb-4 heading thead-line table-super-narrow");
                }
            });

        // Add rows for new data
        var rows = tbody.selectAll("tr")
            .data(times_google_youtube)
            .enter()
            .append("tr")
            .attr("class", "rows");

        var flag = {};
        
        rows.selectAll("td.times")
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
                        cell.attr('colspan', times_colspan).html('<a href="' + flag['href'] + '" target="_blank" class="text-dark"> <p class="mb-0 text-dark news-title">' + flag['title'] + ' »</a></p>')
                        flag = {};
                    } else {
                        cell.remove();
                    }
                } else {
                    if (typeof(d.value) == 'number') {
                        cell.html(d3.format(',')(d.value)).attr('class', 'right-align make-bold news-title');
                    } else {
                        cell.html(d.value).attr('class', 'line-height');
                    }
                }
            });

        //////////////////
        // Create Graph //
        //////////////////

        // 1. Update Thead (add google column with graphs)
        thead.append("th").attr("class", "tomato right-align pb-4 pl-0 heading thead-line").text('GOOGLE SEARCH');
        
        // Use a class so you don't re-select the existing <td> elements
        rows.selectAll("td.google-graph")
            .data(function (row){
                var arr = [];
                return google_columns.map( function (column) {
                    arr.push(row[column]);
                    return arr;
                });
            })
            .enter()
            .append('td')
            .attr("class", "google-graph")
            .each(function (google_data, index) {
                var cell = d3.select(this);
                var more_infos = false;

                create_google(google_data, index, cell, color, more_infos);
                create_side_infos(google_data, index, cell, color, more_infos);
                delete_oldRows(index, filteredTime);
        });

        // 2. Update Thead (add Youtube column with graphs)
        thead.append("th").attr("class", "tomato text-center pb-4 heading thead-line table-wide pl-0").text("YOUTUBE");
        
        // Use a class so you don't re-select the existing <td> elements
        rows.selectAll("td.youtube-graph")
        .data(function (row){
            return youtube_columns.map( function (column) {
                if (column == 'viewCount') {
                   return { column: column, value: row['youtube'][1]};
                } else if (column == 'commentCount') {
                   return { column: column, value: row['youtube'][0]};
                } else if (column =='likeCount') {
                   return { column: column, value: row['youtube'][2]};
                } else {
                   return { column: column, value: row['youtube'][3]};
                }
            });
        })
        .enter()
        .append('td')
        .attr("class", "youtube-graph")
        .each(function (youtube_data, index) {

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
                ];
                flag = {};
            };

            var cell = d3.select(this)//.attr('id', (d,i) => 'youtube' + index);
            create_youtube(youtube_graph, index, times_google_youtube, color, cell);
            // create_side_infos(youtube_data, index, times_google_youtube, color, cell, more_infos);
            delete_oldRows(index, filteredTime);
        })

        // Create Default Side Information
        var side_infos = d3.select("#more_infos");

        // Check ther's no previous infos
        if (side_infos) {
            side_infos.selectAll('.side-tag').remove();
            side_infos.selectAll('.recent_news').remove();
            side_infos.selectAll('.recent_videos').remove();
        };
        
        var side = side_infos.selectAll(".recent_news").data(times_google_youtube).enter()
        
        side.append("div").attr("class", "side-tag pt-2 heading text-white").attr("id", (d,i) => "tag" + i).text((d, i) => {
            if (i == 0) {
                return 'MOST RELEVANT TIMES & YOUTUBE'// + d.tag
                // return 
            } 
            if (i > 0) {
                side_infos.selectAll("#tag"+i).remove();
            }
        });

        side.append("div").attr("class", "mt-4 pb-4 recent_news text-white").attr("id", (d,i) => "news" + i).html((d, i) => {
            if (i == 0) {
                return '<a href="'+ d.url + '" target="_blank" class="text-white"><img src="' + d.img_URL + '" width="100%" height="100%" class="max-image"></a><p class="mb-0 news-title">' + d.title + '<a href="'+ d.url + '" target="_blank" class="text-white"> »</a></p>'//<p class="pt-2 make-bold make-small text-white">' + d.date + '</p>'
            } 
            if (i > 0) {
                side_infos.selectAll("#news" + i).remove();
            }
        });

        side.append("div").attr("class", "recent_videos text-white").attr("id", (d,i) => "videos" + i).html((d, i) => {
            
            if (i == 0) {
                return '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/' + d['youtube'][3]['url'].split('=')[1] + '" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe><p class="mb-0 news-title">' + d['youtube'][3]['title'] + '<a href="https://www.youtube.com/watch?v='+ d['youtube'][3]['url'].split('=')[1] + '" target="_blank" class="text-white"> »</a></p>';
            } ;
            
            if (i > 0) {
                side_infos.selectAll("#videos" + i).remove();
            };
        });
    };

    var create_side_infos = function() {
        d3.select(".rows").classed('rows-hover',true);

        // On click, place each infos per row
        d3.selectAll("tr").on("click", function(d) {
            d3.select(".rows").classed('rows-hover',false);
            var side_infos = d3.select("#more_infos");
            
            if (side_infos) {
                side_infos.selectAll('.side-tag').remove();
                side_infos.selectAll('.recent_news').remove();
                side_infos.selectAll('.recent_videos').remove();
            };
    
            side_infos.append("div").attr("class", "side-tag pt-2 heading text-white").text('MOST RELEVANT TIMES & YOUTUBE');

            side_infos.append("div").attr("class", "mt-4 pb-4 recent_news text-white").html(
                '<a href="'+ d.url + '" target="_blank" class="text-white"><img src="' + d.img_URL + '" width="100%" height="100%" class="max-image"></a><p class="mb-0 news-title">' + d.title + '<a href="'+ d.url + '" target="_blank" class="text-white"> »</a></p>'//<p class="pt-2 make-bold make-small text-white">' + d.date + '</p>'
            );
            
            side_infos.append("div").attr("class", "recent_videos text-white").html(
                '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/' + d['youtube'][3]['url'].split('=')[1] + '" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe><p class="mb-0 news-title text-white">' + d['youtube'][3]['title'] + '<a href="https://www.youtube.com/watch?v='+ d['youtube'][3]['url'].split('=')[1] + '" target="_blank" class="text-white"> »</a></p>'
            );
        
        });
    };

    var create_google = function(google_data, index, cell, color){
        if (index == 0) {
            var margin = {top: 4, bottom: 20, left: "ml-2"},
                width = 50,
                height = 10,
                viewHeight = 15,
                parseDate = d3.time.format("%Y-%m-%d").parse,
                formatDate = d3.time.format("%b %m, %Y"),
                google_graph = [];
                
            // Make googe_date to be parsed with date.time function
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

            var maxY = d3.max(google_graph, function(d) {return d.index;});

            // Define the axes
            var xAxis = d3.svg.axis().scale(xScale).orient("bottom").ticks(3).tickFormat(formatDate);
            // var yAxis = d3.svg.axis().scale(yScale).orient("left").ticks(4).tickSize(-width);

            // Set the area
            var area = d3.svg.area()
                .x(function(d) {return xScale(d.dates);})
                .y0(function(d) {return yScale(0);})
                .y1(function(d) {return yScale(d.index);})
                .interpolate("monotone");

            var outline = d3.svg.line()
                .x(function(d) {return xScale(d.dates);})
                .y(function(d) {return yScale(d.index);});

            // Most popular searches
            cell.append("div").attr("class", "busiest make-xsmall tomato pl-2 pb-0").text(d => formatDate(parseDate(d[2])));


            var svg = cell.append("svg")
                .attr("class", margin.left)
                .attr("viewBox", `0 0 ${width} ${viewHeight}`)
                .append("g")
                .attr("transform", "translate(0," + margin.top + ")");

            svg.append("circle")
                .attr("cx", (d) => {
                    target = d3.max(d[0]);
                    index = d[0].indexOf(target);
                    busiest = parseDate(d[1][index]);
                    // console.log("target: ", xScale(busiest))
                    return xScale(busiest);
                })
                .attr("cy", (d) => {
                    // console.log("target: ", yScale(d3.max(d[0])))
                    return 0;
                })
                .attr("r", 1)
                .attr("class", "tomato");

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
            });
        } else {
            cell.remove();
        }
    };

    var create_youtube = function(youtube_graph, index, times_google_youtube, color, cell){
        
        var comment_max = [], like_max = [], view_max = [],
            viewHeight = 50,
            viewWidth = 80;

        if (index == 2) {
            times_google_youtube.forEach( d => {
                view_max.push(d['youtube'][1])
                comment_max.push(d['youtube'][0])
                like_max.push(d['youtube'][2])
            });
            
            var axisMargin = 12,
                    margin = 20,
                    rangeWidth = 80,
                    height = 800,
                    barHeight = 8,
                    barPadding = (height-axisMargin-margin)*0.8/youtube_graph.length,
                    max = d3.max(view_max),
                    bar, svg, scale, mouseT;

            svg = cell.append("svg").attr("viewBox", `0 0 ${viewWidth} ${viewHeight}`).attr("transform", "translate(0, 10)");

            bar = svg.selectAll("g")
                    .data(youtube_graph)
                    .enter()
                    .append("g");

            bar.attr("class", "bar")
                .attr("cx",0)
                .attr("transform", function(d, i) {
                    if (i == 2) {
                        return "translate(" + margin + "," + (i * (barHeight + barPadding) - 397)+ ")";
                    } else if (i == 1){
                        return "translate(" + margin + "," + (i * (barHeight + barPadding) - 198)+ ")";
                    } else {
                        return "translate(" + margin + "," + (i * (barHeight + barPadding))+ ")";
                    }
                });
            
            scale = d3.scale.linear()
                    .domain([0, max])
                    .range([2, rangeWidth]);

            xAxis = d3.svg.axis()
                    .scale(scale)
                    .tickSize(-height + 2*margin + axisMargin)
                    .orient("bottom");

            bar.append("rect")
                .attr("transform", "translate(10, 1)")
                .attr("height", barHeight)
                .attr("width", function(d){
                    if (scale(d.value) > 20 && scale(d.value) < 40) {
                        return scale(d.value) + 14;
                    } else {
                        return scale(d.value);
                    }
                })
                .style("fill", d => {
                    if (d.value == d3.max(comment_max) || d.value == d3.max(like_max) || d.value == d3.max(view_max)) {
                        return "tomato";
                    }
                    return color;
                });

            bar.append("text")
                .attr("y", 8)
                .attr("x", function(d){
                    if (scale(d.value) > 20) {
                        return 15;
                    } else {
                        return scale(d.value) + axisMargin;
                    }
                })
                .text(function(d, i){
                    return d3.format(',')(d.value);
                })
                .attr("class", d => {
                    if (d.value == d3.max(comment_max) || d.value == d3.max(like_max) || d.value == d3.max(view_max)) {
                        if (scale(d.value) > 40) {
                            return 'value white';
                        } else {
                            return 'value tomato';
                        }
                    } else if (scale(d.value) > 20) {
                        return 'value white';
                    } else {
                        return 'value main-color';
                    }
                });
                
            bar.append('g').attr('class', 'icon').each(function(d) {
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
                d3.select(this).html(component);
                });
        } else {
            cell.remove();
        }
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
    // console.log('* initialData * ', initialData)

    // Call the table, side-infos
    makeTables(initialData);

}).catch(function(err) {
    if (err) return console.warn(err);
});