
var w = 1400;
var h = 500;
var wPadding = 60;
var hPadding = 40;
var parseTime = d3.timeParse("%Y-%m-%d %H:%M:%S%Z");
var parseTime2 = d3.timeParse("%Y-%m-%d")


d3.select("body")
    .append("svg")
    .attr("width", w)
    .attr("height", 30)
    .attr("font-size", 30)
    .append("text")
    .attr("x", w/2-70)
    .attr("y", 22)
    .text("Analyzing the Effect of Twitter Hype on Financial Markets")
    .attr("text-anchor", "middle");



d3.dsv(",", "data/finance_data.csv", function (d) {
    return {
        datetime: parseTime(d.Datetime),
        TSLA_price: parseFloat(d.TSLA_price),
        ZM_price: parseFloat(d.ZM_price),
        AMZN_price: parseFloat(d.AMZN_price),
        DAL_price: parseFloat(d.DAL_price),
        NFLX_price: parseFloat(d.NFLX_price),
        NVS_price: parseFloat(d.NVS_price),
        PFE_price: parseFloat(d.PFE_price),
        TRIP_price: parseFloat(d.TRIP_price),
        GOOGL_price: parseFloat(d.GOOGL_price)
    }
} ).then(function(data) {
    d3.dsv(",", "data/final_hype.csv", function (d) {
        return {
            datetime: parseTime2(d.datetime),
            tesla_hype: parseFloat(d.tesla_hype),
            zm_hype: parseFloat(d.zoom_hype),
            amazon_hype: parseFloat(d.amazon_hype),
            delta_hype: parseFloat(d.delta_hype),
            google_hype: parseFloat(d.google_hype),
            netflix_hype: parseFloat(d.netflix_hype),
            novartis_hype: parseFloat(d.novartis_hype),
            pfizer_hype: parseFloat(d.pfizer_hype),
            tripadvisor_hype: parseFloat(d.tripadvisor_hype)
        }
    }).then(function (data2) {
        var minDate = d3.min(data, function(d) { return d.datetime});
        var maxDate = d3.max(data, function(d) { return d.datetime});
        var min2 = d3.min(data2, function(d) {return d.tesla_hype})
        var max2 = d3.max(data2, function(d) {return d.tesla_hype})
        var xScale = d3.scaleTime()
                        .domain([minDate,maxDate])
                        .range([wPadding*2, w-wPadding*4])

        var xAxis = d3.axisBottom()
                        .scale(xScale)
                        .tickValues(d3.timeDay.range(minDate, maxDate, 1))
                        .tickFormat(d3.timeFormat("%m/%d"));

        var yScale2 = d3.scaleLinear();

        if(min2 < 0) {
            yScale2.domain([(min2 + (min2*0.05)), (max2 + (max2*0.05))])
                    .range([h-hPadding,hPadding]);
        } else {
            yScale2.domain([-3, (max2 + (max2*0.05))])
                    .range([h-hPadding,hPadding]);
        }


        var yAxis2 = d3.axisRight()
                        .scale(yScale2)
                        .ticks(10)


        var selectContainer = d3.select("body")
                                .append("div")
                                .attr("width", 40)
                                .attr("height", 20);

        selectContainer.append("text")
                        .text("Select a stock: ")
                        .attr("class", "text")
                        .attr("font-size", "12px");

        selectContainer.append("select")
                        .selectAll("option")
                        .data(["Tesla (TSLA)", "Zoom (ZM)", "Amazon (AMZN)", "Delta (DAL)", "Google (GOOGL)", "Netflix (NFLX)", "Novartis (NVS)", "Pfizer (PFE)", "Trip Advisor (TRIP)"])
                        .enter()
                        .append("option")
                        .attr("class","text")
                        .text(function(d) {return d;})
                        .attr("value", function(d,i) {return i;});

        selectContainer.select("select")
                        .on("change", function(d) {
                            updateChart(d3.select(this).property("value"));
                        });

        var svg = d3.select("body")
                    .append("svg")
                    .attr("width", w)
                    .attr("height", h+400)
                    .attr("x", 0)
                    .attr("y", 0)
                    .style("background-color", "white");

        var svg2 = svg.append("g")
                        .attr("class", "svg 2")
                        .attr("transform", "translate(" + (w/2-300) + ", " + (h + 10) + " )");

        var info = svg.append("g")
                        .attr("class", "svg 2")
                        .attr("transform", "translate(" + (120) + ", " + (h + 150) + " )");

        info.append("text")
            .text("Welcome! Our website allows you to examine the effects of a stock's hype on twitter versus its stock price.");

        info.append("text")
            .attr("y", 18)
            .text("Select a stock to examine in the drop down menu.");

        info.append("text")
            .attr("y", 36)
            .text("Hover over the circles to view stock data at that point, and hover over the rectangles to view the hype data for that day.")

        info.append("text")
            .attr("y", 54)
            .text("Visualize how the stock data (line) is affected by the hype (rectangles).")

        info.append("text")
            .attr("y", 72)
            .text(" \"0\" or \"negative\" hype will be represented by small bars under the x axis.")

        info.append("text")
            .attr("y", 150)
            .attr("font-size", 12)
            .text("CX4242, Pietro Dominetto, Austin Fan, Katie Jooyoung Kim")

            // Initial bars of hype bar chart

            var width = (w-wPadding)/30;

            var rects = svg.selectAll("rect")
                        .data(data2)
                        .enter()
                        .append("rect")
                        .attr("x", function(d) {
                            return ((xScale(d.datetime))-(width*0.6)/2);
                        })
                        .attr("y", function(d) {
                            if (d.tesla_hype < 0) {
                                return yScale2(0)
                            } else {
                                return yScale2(d.tesla_hype);
                            }
                        })
                        .attr("height", function(d) {
                            if (d.tesla_hype == 0) {
                                return 10;
                            } else {
                                return Math.abs(yScale2(d.tesla_hype) - yScale2(0));
                            }
                        })
                        .attr("width", function(d) {
                            return width*0.6;
                        })
                        .style("fill", function(d) {
                            if(d.tesla_hype < 0) {
                                return "#cc4c02";
                            } else {
                                return "#ffffb2";
                            }
                        })
                        .on("mouseover", function(d) {
                            if(d.tesla_hype < 0) {
                                d3.select(this).style("fill", "#8c2d04");
                            } else {
                                d3.select(this).style("fill", "#fee391");
                            }
                            updateBarInfo(0, d3.select(this).data()[0]);
                        })
                        .on("mouseout", function(d) {
                            if(d.tesla_hype < 0) {
                                d3.select(this).style("fill", "#cc4c02");
                            } else {
                                d3.select(this).style("fill", "#ffffb2");
                            }
                            svg2.selectAll("*").remove();
                        });

            rects.each(function(d) {
                var data_arr = [[],[],[],[],[],[],[],[],[]]; //double array, 0=tsla, then Zoom, Amazon, DAL, Google, NFLX, NVS, PFE, Trip and within each array is the financial data price array for that day
                var hype_arr = [[],[],[],[],[],[],[],[],[]]; //double array, 0=tsla, then Zoom, Amazon, DAL, Google, NFLX, NVS, PFE, Trip and within each array is the financial data price array for that day
                var year = d.datetime.getYear();
                var month = d.datetime.getMonth();
                var day = d.datetime.getDate();
                data.forEach(function(d) {
                    if(d.datetime.getYear() == year && d.datetime.getMonth() == month && d.datetime.getDate() == day) {
                        data_arr[0].push(d.TSLA_price);
                        data_arr[1].push(d.ZM_price);
                        data_arr[2].push(d.AMZN_price);
                        data_arr[3].push(d.DAL_price);
                        data_arr[4].push(d.GOOGL_price);
                        data_arr[5].push(d.NFLX_price);
                        data_arr[6].push(d.NVS_price);
                        data_arr[7].push(d.PFE_price);
                        data_arr[8].push(d.TRIP_price);
                    }
                });
                data2.forEach(function(d) {
                    if(d.datetime.getYear() == year && d.datetime.getMonth() == month && d.datetime.getDate() == day) {
                        hype_arr[0].push(d.tesla_hype);
                        hype_arr[1].push(d.zoom_hype);
                        hype_arr[2].push(d.amazon_hype);
                        hype_arr[3].push(d.delta_hype);
                        hype_arr[4].push(d.google_hype);
                        hype_arr[5].push(d.netflix_hype);
                        hype_arr[6].push(d.novartis_hype);
                        hype_arr[7].push(d.pfizer_hype);
                        hype_arr[8].push(d.tripadvisor_hype);
                    }
                })
                d3.select(this).data()[0].fin_data = data_arr;
                d3.select(this).data()[0].hype_data = hype_arr;
            });


            rects.each(function(d) {
            fin_data = d3.select(this).data()[0].fin_data;
            max_price = [];
            percent_changes=[];
            for(var i = 0; i < fin_data.length; i++) {
                max_price.push(d3.max(fin_data[i]));
                percent_changes.push(Math.round(((fin_data[i][fin_data[i].length-1] - fin_data[i][0])/fin_data[i][0])*10000)/100);
            }

            //initial rect data set to Tesla
            d3.select(this).data()[0].max_price = max_price;
            d3.select(this).data()[0].percent_changes = percent_changes;

            });

            var min = d3.min(rects.data(), function(d) {return d.percent_changes[0]});
            var max = d3.max(rects.data(), function(d) {return d.percent_changes[0]});

            var yScalePos = d3.scaleLinear()
                            .domain([0, (max *1.05)])
                            .range([yScale2(0), hPadding]);
            var yScaleNeg = d3.scaleLinear()
                            .domain([min*1.05, 0])
                            .range([h-hPadding, yScale2(0)]);

            var yAxisPos = d3.axisLeft()
                            .scale(yScalePos)
                            .ticks(10);
            var yAxisNeg = d3.axisLeft()
                            .scale(yScaleNeg)
                            .ticks(10);

            var circles = svg.selectAll(".dot")
                            .data(rects.data())
                            .enter()
                            .append("circle")
                            .attr("class", "dot")
                            .attr("cx", function (d) {return xScale(d.datetime)})
                            .attr("cy", function(d) {
                                if(d.percent_changes[0] == undefined || isNaN(d.percent_changes[0])) {
                                    return -1000000;
                                } else {
                                    if(d.percent_changes[0] >= 0) {
                                        return yScalePos(d.percent_changes[0]);
                                    } else {
                                        return yScaleNeg(d.percent_changes[0]);
                                    }
                                }
                            })
                            .attr("r", "3px")
                            .style("fill", '#a6611a')
                            .on("mouseover", function() {
                                d3.select(this).attr("r", "5px");
                                updateInfo(0, d3.select(this).data()[0]);
                            })
                            .on("mouseout", function() {
                                d3.select(this)
                                .attr("r", "3px");
                                svg2.selectAll("*").remove();
                                rects.each(function(d) {
                                    if (d.on == true) {
                                        d.on == false;
                                    }
                                    if(d.tesla_hype < 0) {
                                        d3.select(this).style("fill", "#cc4c02");
                                    } else {
                                        d3.select(this).style("fill", "#ffffb2");
                                    }
                                })
                            });


        circles.each(function (d) {
            if(d.cy == -1000000) {
                d3.select(this).remove();
            }
        })

        var line = d3.line()
                        .defined(function(d) {return d.percent_changes[0] >= -100; })
                        .x(function(d) {return xScale(d.datetime)})
                        .y(function(d) {
                            if(d.percent_changes[0] >= 0) {
                                return yScalePos(d.percent_changes[0]);
                            } else {
                                return yScaleNeg(d.percent_changes[0]);
                            }
                        });

        var path = svg.append("g")

        path.append("path")
            .datum(circles.data())
            .attr("class", "line")
            .attr("d", line)
            .style("stroke", '#a6611a');

        var xAxisGroup = svg.append("g")
                        .attr("class", "x axis")
                        .attr("transform", "translate(0," + (yScale2(0)) + ")")
                        .call(xAxis);

        var yAxisPosVar = svg.append("g")
            .attr("class", "y axisPos")
            .attr("transform", "translate(" + wPadding*2 + ",0)")
            .call(yAxisPos);

        var yAxisNegVar = svg.append("g")
            .attr("class", "y axisNeg")
            .attr("transform", "translate(" + wPadding*2 + ",0)")
            .call(yAxisNeg);

        svg.append("g")
            .attr("class", "y axis2")
            .attr("transform", "translate(" + (w - wPadding*4) + ",0)")
            .call(yAxis2);


        svg.append("g")
            .attr("transform", "translate(" + (wPadding+25) + "," + h/2 + " )")
            .append("text")
            .attr("text-anchor", "middle")
            .attr("transform", "rotate(-90)")
            .text("Daily Percent Change");


        svg.append("g")
            .attr("transform", "translate(" + (w-wPadding*3-25) + "," + h/2 + " )")
            .append("text")
            .attr("text-anchor", "middle")
            .attr("transform", "rotate(90)")
            .text("Hype");

        svg.append("text")
            .attr("x", (w/2-wPadding))
            .attr("y", h)
            .text("Date");


        var updateChart = function(index) {

            line = d3.line()
                            .defined(function(d) {return d.percent_changes[index] >= -100; })
                            .x(function(d) {return xScale(d.datetime)})
                            .y(function(d) {
                                if(d.percent_changes[index] >= 0) {
                                    return yScalePos(d.percent_changes[index]);
                                } else {
                                    return yScaleNeg(d.percent_changes[index]);
                                }
                            });


            rects.on("mouseover", null);
            min = d3.min(circles.data(), function(d) {return d.percent_changes[index]});
            max = d3.max(circles.data(), function(d) {return d.percent_changes[index]});

            if(index == 0) {
                min2 = d3.min(data2, function(d) {return d.tesla_hype})
                max2 = d3.max(data2, function(d) {return d.tesla_hype})

            } else if (index == 1) {
                min2 = d3.min(data2, function(d) {return d.zm_hype})
                max2 = d3.max(data2, function(d) {return d.zm_hype})

            } else if (index == 2) {
                min2 = d3.min(data2, function(d) {return d.amazon_hype})
                max2 = d3.max(data2, function(d) {return d.amazon_hype})

            } else if (index == 3) {
                min2 = d3.min(data2, function(d) {return d.delta_hype})
                max2 = d3.max(data2, function(d) {return d.delta_hype})

            } else if (index == 4) {
                min2 = d3.min(data2, function(d) {return d.google_hype})
                max2 = d3.max(data2, function(d) {return d.google_hype})

            } else if (index == 5) {
                min2 = d3.min(data2, function(d) {return d.netflix_hype})
                max2 = d3.max(data2, function(d) {return d.netflix_hype})

            } else if (index == 6) {
                min2 = d3.min(data2, function(d) {return d.novartis_hype})
                max2 = d3.max(data2, function(d) {return d.novartis_hype})

            } else if (index == 7) {
                min2 = d3.min(data2, function(d) {return d.pfizer_hype})
                max2 = d3.max(data2, function(d) {return d.pfizer_hype})

            } else {
                min2 = d3.min(data2, function(d) {return d.tripadvisor_hype})
                max2 = d3.max(data2, function(d) {return d.tripadvisor_hype})

            }



            if(min2 < 0) {
                yScale2.domain([(min2 + (min2*0.05)), (max2 + (max2*0.05))])
                        .range([h-hPadding,hPadding]);
            } else {
                yScale2.domain([-3, (max2 + (max2*0.05))])
                        .range([h-hPadding,hPadding]);
            }



            yScalePos = d3.scaleLinear()
                                .domain([0, (max *1.05)])
                                .range([yScale2(0), hPadding]);
            yScaleNeg = d3.scaleLinear()
                                .domain([min*1.05, 0])
                                .range([h-hPadding, yScale2(0)]);


            svg.select(".line")
                .datum(circles.data())
                .transition()
                .duration(500)
                .attr("d", line);


            yAxisPos.scale(yScalePos).ticks(10);

            yAxisPosVar.transition()
            .duration(500)
            .call(yAxisPos);

            yAxisNeg.scale(yScaleNeg).ticks(10);

            yAxisNegVar.transition()
            .duration(500)
            .call(yAxisNeg);


            svg.select(".y.axis2")
            .transition()
            .duration(500)
            .call(yAxis2);



            xAxisGroup.transition()
                    .duration(500)
                    .attr("transform", "translate(0," + (yScale2(0)) + ")")
                    .call(xAxis);


            circles.transition()
                    .duration(500)
                    .attr("cx", function(d) {return xScale(d.datetime)})
                    .attr("cy", function(d) {
                        if(d.percent_changes[index] == undefined || isNaN(d.percent_changes[index])) {
                            return -1000000;
                        } else {
                            if(d.percent_changes[index] >= 0) {
                                return yScalePos(d.percent_changes[index]);
                            } else {
                                return yScaleNeg(d.percent_changes[index]);
                            }
                        }
                    });

            circles.on("mouseover", null)
                    .on("mouseout", null);

            circles.on("mouseover", function() {
                d3.select(this)
                    .attr("r", "5px");
                    updateInfo(index, d3.select(this).data()[0]);
                });


            circles.each(function (d) {
                if(d.cy == -1000000) {
                    d3.select(this).remove();
                }
            })



                //Changing the line
            if(index == 0) {
                rects.data(data2)
                        .transition()
                        .duration(500)
                        .attr("x", function(d) {
                            return ((xScale(d.datetime))-(width*0.6)/2);
                        })
                        .attr("y", function(d) {
                            if (d.tesla_hype < 0) {
                                return yScale2(0)
                            } else {
                                return yScale2(d.tesla_hype);
                            }
                        })
                        .attr("height", function(d) {
                            if (d.tesla_hype == 0) {
                                return 10;
                            } else {
                                return Math.abs(yScale2(d.tesla_hype) - yScale2(0));
                            }
                        })
                        .style("fill", function(d) {
                            if(d.tesla_hype < 0) {
                                return "#cc4c02";
                            } else {
                                return "#ffffb2";
                            }
                        })
                        .attr("width", function(d) {
                            return width*0.6;
                        })


                    rects.on("mouseover", function(d) {
                        if(d.tesla_hype < 0) {
                            d3.select(this).style("fill", "#8c2d04");
                        } else {
                            d3.select(this).style("fill", "#fee391");
                        }
                        updateBarInfo(0, d3.select(this).data()[0]);
                        })
                        .on("mouseout", function(d) {
                            if(d.tesla_hype < 0) {
                                d3.select(this).style("fill", "#cc4c02");
                            } else {
                                d3.select(this).style("fill", "#ffffb2");
                            }
                        svg2.selectAll("*").remove();

                    });

                    circles.on("mouseout", function() {
                        d3.select(this)
                        .attr("r", "3px");
                        svg2.selectAll("*").remove();
                        rects.each(function(d) {
                            if (d.on == true) {
                                d.on == false;
                            }
                            if(d.tesla_hype < 0) {
                                d3.select(this).style("fill", "#cc4c02");
                            } else {
                                d3.select(this).style("fill", "#ffffb2");
                            }
                        })
                    })
            } else if (index == 1) {
                    rects.data(data2)
                        .transition()
                        .duration(500)
                        .attr("x", function(d) {
                            return ((xScale(d.datetime))-(width*0.6)/2);
                        })
                        .attr("y", function(d) {
                            if (d.zm_hype < 0) {
                                return yScale2(0)
                            } else {
                                return yScale2(d.zm_hype);
                            }
                        })
                        .attr("height", function(d) {
                            if (d.zm_hype == 0) {
                                return 10;
                            } else {
                                return Math.abs(yScale2(d.zm_hype) - yScale2(0));
                            }
                        })
                        .style("fill", function(d) {
                            if(d.zm_hype < 0) {
                                return "#cc4c02";
                            } else {
                                return "#ffffb2";
                            }
                        })
                        .attr("width", function(d) {
                            return width*0.6;
                        });


                        rects.on("mouseover", function(d) {
                                if(d.zm_hype < 0) {
                                    d3.select(this).style("fill", "#8c2d04");
                                } else {
                                    d3.select(this).style("fill", "#fee391");
                                }
                                updateBarInfo(0, d3.select(this).data()[0]);
                                })
                            .on("mouseout", function(d) {
                                if(d.zm_hype < 0) {
                                    d3.select(this).style("fill", "#cc4c02");
                                } else {
                                    d3.select(this).style("fill", "#ffffb2");
                                }
                            svg2.selectAll("*").remove();

                        });

                        circles.on("mouseout", function() {
                                d3.select(this)
                                .attr("r", "3px");
                                svg2.selectAll("*").remove();
                                rects.each(function(d) {
                                    if (d.on == true) {
                                        d.on == false;
                                    }
                                    if(d.zm_hype < 0) {
                                        d3.select(this).style("fill", "#cc4c02");
                                    } else {
                                        d3.select(this).style("fill", "#ffffb2");
                                    }
                                })
                            })
            } else if (index == 2) {
                    rects.data(data2)
                        .transition()
                        .duration(500)
                        .attr("x", function(d) {
                            return ((xScale(d.datetime))-(width*0.6)/2);
                        })
                        .attr("y", function(d) {
                            if (d.amazon_hype < 0) {
                                return yScale2(0)
                            } else {
                                return yScale2(d.amazon_hype);
                            }
                        })
                        .attr("height", function(d) {
                            if (d.amazon_hype == 0) {
                                return 10;
                            } else {
                                return Math.abs(yScale2(d.amazon_hype) - yScale2(0));
                            }
                        })
                        .style("fill", function(d) {
                            if(d.amazon_hype < 0) {
                                return "#cc4c02";
                            } else {
                                return "#ffffb2";
                            }
                        })
                        .attr("width", function(d) {
                            return width*0.6;
                        });

                        rects.on("mouseover", function(d) {
                                if(d.amazon_hype < 0) {
                                    d3.select(this).style("fill", "#8c2d04");
                                } else {
                                    d3.select(this).style("fill", "#fee391");
                                }
                                updateBarInfo(0, d3.select(this).data()[0]);
                                })
                            .on("mouseout", function(d) {
                                if(d.amazon_hype < 0) {
                                    d3.select(this).style("fill", "#cc4c02");
                                } else {
                                    d3.select(this).style("fill", "#ffffb2");
                                }
                            svg2.selectAll("*").remove();

                        });

                        circles.on("mouseout", function() {
                                d3.select(this)
                                .attr("r", "3px");
                                svg2.selectAll("*").remove();
                                rects.each(function(d) {
                                    if (d.on == true) {
                                        d.on == false;
                                    }
                                    if(d.amazon_hype < 0) {
                                        d3.select(this).style("fill", "#cc4c02");
                                    } else {
                                        d3.select(this).style("fill", "#ffffb2");
                                    }
                                })
                            })
            } else if (index == 3) {
                    rects.data(data2)
                        .transition()
                        .duration(500)
                        .attr("x", function(d) {
                            console.log(d);
                            return ((xScale(d.datetime))-(width*0.6)/2);
                        })
                        .style("fill", function(d) {
                            if(d.delta_hype < 0) {
                                return "#cc4c02";
                            } else {
                                return "#ffffb2";
                            }
                        })
                        .attr("y", function(d) {
                            if (d.delta_hype < 0) {
                                return yScale2(0)
                            } else {
                                return yScale2(d.delta_hype);
                            }
                        })
                        .attr("height", function(d) {
                            if (d.delta_hype == 0) {
                                return 10;
                            } else {
                                return Math.abs(yScale2(d.delta_hype) - yScale2(0));
                            }
                        })
                        .attr("width", function(d) {
                            return width*0.6;
                        });

                        rects.on("mouseover", function(d) {
                                if(d.delta_hype < 0) {
                                    d3.select(this).style("fill", "#8c2d04");
                                } else {
                                    d3.select(this).style("fill", "#fee391");
                                }
                                updateBarInfo(0, d3.select(this).data()[0]);
                                })
                            .on("mouseout", function(d) {
                                if(d.delta_hype < 0) {
                                    d3.select(this).style("fill", "#cc4c02");
                                } else {
                                    d3.select(this).style("fill", "#ffffb2");
                                }
                            svg2.selectAll("*").remove();

                        });

                        circles.on("mouseout", function() {
                                d3.select(this)
                                .attr("r", "3px");
                                svg2.selectAll("*").remove();
                                rects.each(function(d) {
                                    if (d.on == true) {
                                        d.on == false;
                                    }
                                    if(d.delta_hype < 0) {
                                        d3.select(this).style("fill", "#cc4c02");
                                    } else {
                                        d3.select(this).style("fill", "#ffffb2");
                                    }
                                })
                            })
            } else if (index == 4) {
                    rects.data(data2)
                        .transition()
                        .duration(500)
                        .attr("x", function(d) {
                            return ((xScale(d.datetime))-(width*0.6)/2);
                        })
                        .style("fill", function(d) {
                            if(d.google_hype < 0) {
                                return "#cc4c02";
                            } else {
                                return "#ffffb2";
                            }
                        })
                        .attr("y", function(d) {
                            if (d.google_hype < 0) {
                                return yScale2(0)
                            } else {
                                return yScale2(d.google_hype);
                            }
                        })
                        .attr("height", function(d) {
                            if (d.google_hype == 0) {
                                return 10;
                            } else {
                                return Math.abs(yScale2(d.google_hype) - yScale2(0));
                            }
                        })
                        .attr("width", function(d) {
                            return width*0.6;
                        });
                        rects.on("mouseover", function(d) {
                                if(d.google_hype < 0) {
                                    d3.select(this).style("fill", "#8c2d04");
                                } else {
                                    d3.select(this).style("fill", "#fee391");
                                }
                                updateBarInfo(0, d3.select(this).data()[0]);
                                })
                            .on("mouseout", function(d) {
                                if(d.google_hype < 0) {
                                    d3.select(this).style("fill", "#cc4c02");
                                } else {
                                    d3.select(this).style("fill", "#ffffb2");
                                }
                            svg2.selectAll("*").remove();

                        });

                        circles.on("mouseout", function() {
                                d3.select(this)
                                .attr("r", "3px");
                                svg2.selectAll("*").remove();
                                rects.each(function(d) {
                                    if (d.on == true) {
                                        d.on == false;
                                    }
                                    if(d.google_hype < 0) {
                                        d3.select(this).style("fill", "#cc4c02");
                                    } else {
                                        d3.select(this).style("fill", "#ffffb2");
                                    }
                                })
                            })
            } else if (index == 5) {
                    rects.data(data2)
                        .transition()
                        .duration(500)
                        .attr("x", function(d) {
                            return ((xScale(d.datetime))-(width*0.6)/2);
                        })
                        .style("fill", function(d) {
                            if(d.netflix_hype < 0) {
                                return "#cc4c02";
                            } else {
                                return "#ffffb2";
                            }
                        })
                        .attr("y", function(d) {
                            if (d.netflix_hype < 0) {
                                return yScale2(0)
                            } else {
                                return yScale2(d.netflix_hype);
                            }
                        })
                        .attr("height", function(d) {
                            if (d.netflix_hype == 0) {
                                return 10;
                            } else {
                                return Math.abs(yScale2(d.netflix_hype) - yScale2(0));
                            }
                        })
                        .attr("width", function(d) {
                            return width*0.6;
                        });

                        rects.on("mouseover", function(d) {
                                if(d.netflix_hype < 0) {
                                    d3.select(this).style("fill", "#8c2d04");
                                } else {
                                    d3.select(this).style("fill", "#fee391");
                                }
                                updateBarInfo(0, d3.select(this).data()[0]);
                                })
                            .on("mouseout", function(d) {
                                if(d.netflix_hype < 0) {
                                    d3.select(this).style("fill", "#cc4c02");
                                } else {
                                    d3.select(this).style("fill", "#ffffb2");
                                }
                            svg2.selectAll("*").remove();

                        });

                        circles.on("mouseout", function() {
                                d3.select(this)
                                .attr("r", "3px");
                                svg2.selectAll("*").remove();
                                rects.each(function(d) {
                                    if (d.on == true) {
                                        d.on == false;
                                    }
                                    if(d.netflix_hype < 0) {
                                        d3.select(this).style("fill", "#cc4c02");
                                    } else {
                                        d3.select(this).style("fill", "#ffffb2");
                                    }
                                })
                            })
            } else if (index == 6) {
                    rects.data(data2)
                        .transition()
                        .duration(500)
                        .attr("x", function(d) {
                            return ((xScale(d.datetime))-(width*0.6)/2);
                        })
                        .attr("y", function(d) {
                            if (d.novartis_hype < 0) {
                                return yScale2(0)
                            } else {
                                return yScale2(d.novartis_hype);
                            }
                        })
                        .attr("height", function(d) {
                            if (d.novartis_hype == 0) {
                                return 10;
                            } else {
                                return Math.abs(yScale2(d.novartis_hype) - yScale2(0));
                            }
                        })
                        .style("fill", function(d) {
                            if(d.novartis_hype < 0) {
                                return "#cc4c02";
                            } else {
                                return "#ffffb2";
                            }
                        })
                        .attr("width", function(d) {
                            return width*0.6;
                        });

                        rects.on("mouseover", function(d) {
                                if(d.novartis_hype < 0) {
                                    d3.select(this).style("fill", "#8c2d04");
                                } else {
                                    d3.select(this).style("fill", "#fee391");
                                }
                                updateBarInfo(0, d3.select(this).data()[0]);
                                })
                            .on("mouseout", function(d) {
                                if(d.novartis_hype < 0) {
                                    d3.select(this).style("fill", "#cc4c02");
                                } else {
                                    d3.select(this).style("fill", "#ffffb2");
                                }
                            svg2.selectAll("*").remove();

                        });

                        circles.on("mouseout", function() {
                                d3.select(this)
                                .attr("r", "3px");
                                svg2.selectAll("*").remove();
                                rects.each(function(d) {
                                    if (d.on == true) {
                                        d.on == false;
                                    }
                                    if(d.novartis_hype < 0) {
                                        d3.select(this).style("fill", "#cc4c02");
                                    } else {
                                        d3.select(this).style("fill", "#ffffb2");
                                    }
                                })
                            })
            } else if (index == 7) {
                    rects.data(data2)
                        .transition()
                        .duration(500)
                        .attr("x", function(d) {
                            return ((xScale(d.datetime))-(width*0.6)/2);
                        })
                        .attr("y", function(d) {
                            if (d.pfizer_hype < 0) {
                                return yScale2(0)
                            } else {
                                return yScale2(d.pfizer_hype);
                            }
                        })
                        .attr("height", function(d) {
                            if (d.pfizer_hype == 0) {
                                return 10;
                            } else {
                                return Math.abs(yScale2(d.pfizer_hype) - yScale2(0));
                            }
                        })
                        .style("fill", function(d) {
                            if(d.pfizer_hype < 0) {
                                return "#cc4c02";
                            } else {
                                return "#ffffb2";
                            }
                        })
                        .attr("width", function(d) {
                            return width*0.6;
                        });

                        rects.on("mouseover", function(d) {
                                if(d.pfizer_hype < 0) {
                                    d3.select(this).style("fill", "#8c2d04");
                                } else {
                                    d3.select(this).style("fill", "#fee391");
                                }
                                updateBarInfo(0, d3.select(this).data()[0]);
                                })
                            .on("mouseout", function(d) {
                                if(d.pfizer_hype < 0) {
                                    d3.select(this).style("fill", "#cc4c02");
                                } else {
                                    d3.select(this).style("fill", "#ffffb2");
                                }
                            svg2.selectAll("*").remove();

                        });

                        circles.on("mouseout", function() {
                                d3.select(this)
                                .attr("r", "3px");
                                svg2.selectAll("*").remove();
                                rects.each(function(d) {
                                    if (d.on == true) {
                                        d.on == false;
                                    }
                                    if(d.pfizer_hype < 0) {
                                        d3.select(this).style("fill", "#cc4c02");
                                    } else {
                                        d3.select(this).style("fill", "#ffffb2");
                                    }
                                })
                            })
            } else {
                    rects.data(data2)
                        .transition()
                        .duration(500)
                        .attr("x", function(d) {
                            return ((xScale(d.datetime))-(width*0.6)/2);
                        })
                        .style("fill", function(d) {
                            if(d.tripadvisor_hype < 0) {
                                return "#cc4c02";
                            } else {
                                return "#ffffb2";
                            }
                        })
                        .attr("y", function(d) {
                            if (d.tripadvisor_hype < 0) {
                                return yScale2(0)
                            } else {
                                return yScale2(d.tripadvisor_hype);
                            }
                        })
                        .attr("height", function(d) {
                            if (d.tripadvisor_hype == 0) {
                                return 10;
                            } else {
                                return Math.abs(yScale2(d.tripadvisor_hype) - yScale2(0));
                            }
                        })
                        .attr("width", function(d) {
                            return width*0.6;
                        });
                        rects.on("mouseover", function(d) {
                                if(d.tripadvisor_hype < 0) {
                                    d3.select(this).style("fill", "#8c2d04");
                                } else {
                                    d3.select(this).style("fill", "#fee391");
                                }
                                updateBarInfo(0, d3.select(this).data()[0]);
                                })
                            .on("mouseout", function(d) {
                                if(d.tripadvisor_hype < 0) {
                                    d3.select(this).style("fill", "#cc4c02");
                                } else {
                                    d3.select(this).style("fill", "#ffffb2");
                                }
                            svg2.selectAll("*").remove();

                        });

                        circles.on("mouseout", function() {
                                d3.select(this)
                                .attr("r", "3px");
                                svg2.selectAll("*").remove();
                                rects.each(function(d) {
                                    if (d.on == true) {
                                        d.on == false;
                                    }
                                    if(d.tripadvisor_hype < 0) {
                                        d3.select(this).style("fill", "#cc4c02");
                                    } else {
                                        d3.select(this).style("fill", "#ffffb2");
                                    }
                                })
                            })
            }
        }

        //For separate SVG
        var updateInfo = function(index, val) {
            var day = val.datetime.getDate();
            var month = val.datetime.getMonth();
            var max_price;
            var percent_change;
            var hype;
            rects.each(function(d,i) {
                if(d.datetime.getMonth() == month && d.datetime.getDate() == day) {
                    d3.select(this).style("fill", "#fed98e").attr("on", true)
                    max_price = Math.round(d3.select(this).data()[0].max_price[index]*100)/100;
                    percent_change = d3.select(this).data()[0].percent_changes[index];
                    hype = d3.select(this).data()[0].hype_data[0][index]
                }
            })

            svg2.append("text")
                .attr("x", 2)
                .attr("y", 15)
                .attr("font-size", 16)
                .text(function() {
                    return "Time: " + val.datetime;
                });

            svg2.append("text")
                .attr("x", 2)
                .attr("y", 30)
                .attr("font-size", 16)
                .text(function() {
                    return "Hype: " + Math.round(hype*100)/100;
                });

            svg2.append("text")
                .attr("x", 2)
                .attr("y", 45)
                .attr("font-size", 16)
                .text(function() {
                    if (max_price == undefined || isNaN(max_price)) {
                        return "Day's High: Weekend, or no stock price data";
                    }
                    return "Day's High: $" + max_price;
                });
            svg2.append("text")
                .attr("x", 2)
                .attr("y", 60)
                .attr("font-size", 16)
                .text(function() {
                    if (percent_change == undefined || isNaN(percent_change)) {
                        return "Daily Percentage Change: Weekend, or no stock price data";
                    }
                    return "Daily Percentage Change: " + percent_change +"%";
                });
        }

        var updateBarInfo = function(index, obj) {
            var date = obj.datetime;
            var hype = obj.hype_data[index][0];
            var max_price = Math.round(obj.max_price[index] * 100)/100;
            var percent_change = obj.percent_changes[index];
            svg2.append("text")
                .attr("x", 2)
                .attr("y", 15)
                .attr("font-size", 16)
                .text(function() {
                    return "Day: " + date;
                });
            svg2.append("text")
                .attr("x", 2)
                .attr("y", 30)
                .attr("font-size", 16)
                .text(function() {
                    return "Hype: " + Math.round(hype*100)/100;
                });
            svg2.append("text")
                .attr("x", 2)
                .attr("y", 45)
                .attr("font-size", 16)
                .text(function() {
                    if (max_price == undefined || isNaN(max_price)) {
                        return "Day's High: Weekend, or no stock price data";
                    }
                    return "Day's High: $" + max_price;
                });
            svg2.append("text")
                .attr("x", 2)
                .attr("y", 60)
                .attr("font-size", 16)
                .text(function() {
                    if (percent_change == undefined || isNaN(percent_change)) {
                        return "Daily Percentage Change: Weekend, or no stock price data";
                    }
                    return "Daily Percentage Change: " + percent_change +"%";
                });
        }
    })
})