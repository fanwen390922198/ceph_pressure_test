#!/usr/bin/python

print("Content-type: text/html\n")
print("""
<!---
This page contains Javascript that generates the HTML for displaying the
sample charts on the right frame. To view the HTML, please right click on
an empty position on the right frame, and select "View Source" (for IE) or
"This Frame -> View Frame Source" (for FireFox).
--->
<html>
<head>
<script language="Javascript">
var charts = [
    ['', "Pie Charts"],
    ['simplepie.py', "Simple Pie Chart", 1],
    ['threedpie.py', "3D Pie Chart", 1],
    ['multidepthpie.py', "Multi-Depth Pie Chart", 1],
    ['sidelabelpie.py', "Side Label Layout", 1],
    ['circlelabelpie.py', "Circular Label Layout", 2],
    ['legendpie.py', "Pie Chart with Legend (1)", 1],
    ['legendpie2.py', "Pie Chart with Legend (2)", 1],
    ['explodedpie.py', "Exploded Pie Chart", 1],
    ['iconpie.py', "Icon Pie Chart (1)", 1],
    ['iconpie2.py', "Icon Pie Chart (2)", 1],
    ['multipie.py', "Multi-Pie Chart", 3],
    ['donut.py', "Donut Chart", 1],
    ['threeddonut.py', "3D Donut Chart", 1],
    ['icondonut.py', "Icon Donut Chart", 1],
    ['texturedonut.py', "Texture Donut Chart", 1],
    ['concentric.py', "Concentric Donut Chart", 1],
    ['pieshading.py', "2D Pie Shading", 6],
    ['threedpieshading.py', "3D Pie Shading", 7],
    ['donutshading.py', "2D Donut Shading", 7],
    ['threeddonutshading.py', "3D Donut Shading", 8],
    ['fontpie.py', "Text Style and Colors", 1],
    ['threedanglepie.py', "3D Angle", 7],
    ['threeddepthpie.py', "3D Depth", 5],
    ['shadowpie.py', "3D Shadow Mode", 4],
    ['anglepie.py', "Start Angle and Direction", 2],
    ['donutwidth.py', "Donut Width", 5],
    ['', ""],
    ['', "Bar Charts"],
    ['simplebar.py', "Simple Bar Chart (1)", 1],
    ['simplebar2.py', "Simple Bar Chart (2)", 1],
    ['barlabel.py', "Bar Labels", 1],
    ['colorbar.py', "Multi-Color Bar Chart (1)", 1],
    ['colorbar2.py', "Multi-Color Bar Chart (2)", 1],
    ['softlightbar.py', "Soft Bar Shading", 1],
    ['glasslightbar.py', "Glass Bar Shading", 1],
    ['gradientbar.py', "Gradient Bar Shading", 1],
    ['cylinderlightbar.py', "Cylinder Bar Shading", 1],
    ['threedbar.py', "3D Bar Chart", 1],
    ['cylinderbar.py', "Cylinder Bar Shape", 1],
    ['polygonbar.py', "Polygon Bar Shapes", 1],
    ['stackedbar.py', "Stacked Bar Chart", 1],
    ['percentbar.py', "Percentage Bar Chart", 1],
    ['multibar.py', "Multi-Bar Chart", 1],
    ['softmultibar.py', "Soft Multi-Bar Chart", 1],
    ['glassmultibar.py', "Glass Multi-Bar Chart", 1],
    ['gradientmultibar.py', "Gradient Multi-Bar Chart", 1],
    ['multicylinder.py', "Multi-Cylinder Chart", 1],
    ['multishapebar.py', "Multi-Shape Bar Chart", 1],
    ['overlapbar.py', "Overlapping Bar Chart", 1],
    ['multistackbar.py', "Multi-Stacked Bar Chart", 1],
    ['depthbar.py', "Depth Bar Chart", 1],
    ['posnegbar.py', "Positive Negative Bars", 1],
    ['hbar.py', "Borderless Bar Chart", 1],
    ['dualhbar.py', "Dual Horizontal Bar Charts", 1],
    ['markbar.py', "Bars with Marks", 1],
    ['histogram.py', "Histogram with Bell Curve", 1],
    ['pareto.py', "Pareto Chart", 1],
    ['varwidthbar.py', "Variable Width Bar Chart", 1],
    ['gapbar.py', "Bar Gap", 6],
    ['', ""],
    ['', "Line Charts"],
    ['simpleline.py', "Simple Line Chart", 1],
    ['compactline.py', "Compact Line Chart", 1],
    ['threedline.py', "3D Line Chart", 1],
    ['multiline.py', "Multi-Line Chart (1)", 1],
    ['multiline2.py', "Multi-Line Chart (2)", 1],
    ['symbolline.py', "Symbol Line Chart (1)", 1],
    ['symbolline2.py', "Symbol Line Chart (2)", 1],
    ['missingpoints.py', "Missing Data Points", 1],
    ['unevenpoints.py', "Uneven Data Points ", 1],
    ['splineline.py', "Spline Line Chart", 1],
    ['stepline.py', "Step Line Chart", 1],
    ['linefill.py', "Inter-Line Coloring", 1],
    ['linecompare.py', "Line with Target Zone", 1],
    ['errline.py', "Line with Error Symbols", 1],
    ['multisymbolline.py', "Multi-Symbol Line Chart", 1],
    ['binaryseries.py', "Binary Data Series", 1],
    ['customsymbolline.py', "Custom Symbols", 1],
    ['rotatedline.py', "Rotated Line Chart", 1],
    ['xyline.py', "Arbitrary XY Line Chart", 1],
    ['', ""],
    ['', "Trending and Curve Fitting"],
    ['trendline.py', "Trend Line Chart", 1],
    ['scattertrend.py', "Scatter Trend Chart", 1],
    ['confidenceband.py', "Confidence Band", 1],
    ['paramcurve.py', "Parametric Curve Fitting", 1],
    ['curvefitting.py', "General Curve Fitting", 1],
    ['', ""],
    ['', "Scatter/Bubble/Vector Charts"],
    ['scatter.py', "Scatter Chart", 1],
    ['builtinsymbols.py', "Built-in Symbols", 1],
    ['scattersymbols.py', "Custom Scatter Symbols", 1],
    ['scatterlabels.py', "Custom Scatter Labels", 1],
    ['bubble.py', "Bubble Chart", 1],
    ['threedbubble.py', "3D Bubble Chart (1)", 1],
    ['threedbubble2.py', "3D Bubble Chart (2)", 1],
    ['threedbubble3.py', "3D Bubble Chart (3)", 1],
    ['bubblescale.py', "Bubble XY Scaling", 1],
    ['vector.py', "Vector Chart", 1],
    ['', ""],
    ['', "Area Charts"],
    ['simplearea.py', "Simple Area Chart", 1],
    ['enhancedarea.py', "Enhanced Area Chart", 1],
    ['arealine.py', "Area Line Chart", 1],
    ['threedarea.py', "3D Area Chart", 1],
    ['patternarea.py', "Pattern Area Chart", 1],
    ['stackedarea.py', "Stacked Area Chart", 1],
    ['threedstackarea.py', "3D Stacked Area Chart", 1],
    ['percentarea.py', "Percentage Area Chart", 1],
    ['deptharea.py', "Depth Area Chart", 1],
    ['rotatedarea.py', "Rotated Area Chart", 1],
    ['', ""],
    ['', "Floating Box/Waterfall Charts"],
    ['boxwhisker.py', "Box-Whisker Chart (1)", 1],
    ['boxwhisker2.py', "Box-Whisker Chart (2)", 1],
    ['hboxwhisker.py', "Horizontal Box-Whisker Chart", 1],
    ['floatingbox.py', "Floating Box Chart", 1],
    ['waterfall.py', "Waterfall Chart", 1],
    ['posnegwaterfall.py', "Pos/Neg Waterfall Chart", 1],
    ['', ""],
    ['', "Gantt Charts"],
    ['gantt.py', "Simple Gantt Chart", 1],
    ['colorgantt.py', "Multi-Color Gantt Chart", 1],
    ['layergantt.py', "Multi-Layer Gantt Chart", 1],
    ['', ""],
    ['', "Contour Charts/Heat Maps"],
    ['contour.py', "Contour Chart", 1],
    ['scattercontour.py', "Scattered Data Contour Chart", 1],
    ['contourcolor.py', "Contour Color Scale", 4],
    ['contourlegend.py', "Contour Color Legend", 1],
    ['smoothcontour.py', "Continuous Contour Coloring", 1],
    ['contourinterpolate.py', "Contour Interpolation", 4],
    ['', ""],
    ['', "Finance Charts"],
    ['hloc.py', "Simple HLOC Chart", 1],
    ['candlestick.py', "Simple Candlestick Chart", 1],
    ['finance.py', "Finance Chart (1)", 1],
    ['finance2.py', "Finance Chart (2)", 1],
    ['financesymbols.py', "Finance Chart Custom Symbols", 1],
    ['<a href="javascript:window.open(\\'financedemo.py\\', \\'financedemo\\').focus();">', "Interactive Financial Chart", -1],
    ['', ""],
    ['', "Other XY Chart Features"],
    ['markzone.py', "Marks and Zones (1)", 1],
    ['markzone2.py', "Marks and Zones (2)", 1],
    ['yzonecolor.py', "Y Zone Coloring", 1],
    ['xzonecolor.py', "X Zone Coloring", 1],
    ['dualyaxis.py', "Dual Y-Axis", 1],
    ['dualxaxis.py', "Dual X-Axis", 1],
    ['multiaxes.py', "Multiple Axes", 1],
    ['fourq.py', "4 Quadrant Chart", 1],
    ['datatable.py', "Data Table (1)", 1],
    ['datatable2.py', "Data Table (2)", 1],
    ['fontxy.py', "Text Style and Colors", 1],
    ['background.py', "Background and Wallpaper", 4],
    ['logaxis.py', "Log Scale Axis", 2],
    ['axisscale.py', "Y-Axis Scaling", 5],
    ['ticks.py', "Tick Density", 2],
    ['', ""],
    ['', "3D Surface Charts"],
    ['surface.py', "Surface Chart (1)", 1],
    ['surface2.py', "Surface Chart (2)", 1],
    ['surface3.py', "Surface Chart (3)", 1],
    ['scattersurface.py', "Scattered Data Surface Chart", 1],
    ['surfaceaxis.py', "Surface Chart Axis Types", 1],
    ['surfacelighting.py', "Surface Lighting", 4],
    ['surfaceshading.py', "Surface Shading", 4],
    ['surfacewireframe.py', "Surface Wireframe", 6],
    ['surfaceperspective.py', "Surface Perspective", 6],
    ['', ""],
    ['', "3D Scatter Charts"],
    ['threedscatter.py', "3D Scatter Chart (1)", 1],
    ['threedscatter2.py', "3D Scatter Chart (2)", 1],
    ['threedscattergroups.py', "3D Scatter Groups", 1],
    ['threedscatteraxis.py', "3D Scatter Axis Types", 1],
    ['', ""],
    ['', "Polar/Radar Charts"],
    ['simpleradar.py', "Simple Radar Chart", 1],
    ['multiradar.py', "Multi Radar Chart", 1],
    ['stackradar.py', "Stacked Radar Chart", 1],
    ['polarline.py', "Polar Line Chart", 1],
    ['polararea.py', "Polar Area Chart", 1],
    ['polarspline.py', "Polar Spline Chart", 1],
    ['polarscatter.py', "Polar Scatter Chart", 1],
    ['polarbubble.py', "Polar Bubble Chart", 1],
    ['polarvector.py', "Polar Vector Chart", 1],
    ['rose.py', "Simple Rose Chart", 1],
    ['stackrose.py', "Stacked Rose Chart", 1],
    ['polarzones.py', "Circular Zones", 1],
    ['polarzones2.py', "Sector Zones", 1],
    ['', ""],
    ['', "Pyramids/Cones/Funnels"],
    ['simplepyramid.py', "Simple Pyramid Chart", 1],
    ['threedpyramid.py', "3D Pyramid Chart", 1],
    ['rotatedpyramid.py', "Rotated Pyramid Chart", 1],
    ['cone.py', "Cone Chart", 1],
    ['funnel.py', "Funnel Chart", 1],
    ['pyramidelevation.py', "Pyramid Elevation", 7],
    ['pyramidrotation.py', "Pyramid Rotation", 7],
    ['pyramidgap.py', "Pyramid Gap", 6],
    ['', ""],
    ['', "Angular Meters/Guages"],
    ['semicirclemeter.py', "Semicircle Meter", 1],
    ['colorsemicirclemeter.py', "Color Semicircle Meters", 6],
    ['blacksemicirclemeter.py', "Black Semicircle Meters", 6],
    ['whitesemicirclemeter.py', "White Semicircle Meters", 6],
    ['semicirclemeterreadout.py', "Semicircle Meter with Readout", 2],
    ['roundmeter.py', "Round Meter", 1],
    ['colorroundmeter.py', "Color Round Meters", 6],
    ['blackroundmeter.py', "Black Round Meters", 6],
    ['whiteroundmeter.py', "White Round Meters", 6],
    ['neonroundmeter.py', "Neon Round Meters", 4],
    ['roundmeterreadout.py', "Round Meters with Readout", 2],
    ['rectangularmeter.py', "Rectangular Angular Meters", 6],
    ['squareameter.py', "Square Angular Meters", 4],
    ['angularpointer.py', "Angular Meter Pointers (1)", 1],
    ['angularpointer2.py', "Angular Meter Pointers (2)", 1],
    ['iconameter.py', "Icon Angular Meter", 1],
    ['', ""],
    ['', "Linear Meters/Guages"],
    ['hlinearmeter.py', "Horizontal Linear Meter", 1],
    ['colorhlinearmeter.py', "Color Horizontal Linear Meters", 6],
    ['blackhlinearmeter.py', "Black Horizontal Linear Meters", 6],
    ['whitehlinearmeter.py', "White Horizontal Linear Meters", 6],
    ['hlinearmeterorientation.py', "H-Linear Meter Orientation", 4],
    ['vlinearmeter.py', "Vertical Linear Meter", 1],
    ['colorvlinearmeter.py', "Color Vertical Linear Meters", 6],
    ['blackvlinearmeter.py', "Black Vertical Linear Meters", 6],
    ['whitevlinearmeter.py', "White Vertical Linear Meters", 6],
    ['vlinearmeterorientation.py', "V-Linear Meter Orientation", 2],
    ['multihmeter.py', "Multi-Pointer Horizontal Meter", 1],
    ['multivmeter.py', "Multi-Pointer Vertical Meter", 1],
    ['linearzonemeter.py', "Linear Zone Meter", 1],
    ['', ""],
    ['', "Bar Meters/Guages"],
    ['hbarmeter.py', "Horizontal Bar Meter", 1],
    ['colorhbarmeter.py', "Color Horizontal Bar Meters", 6],
    ['blackhbarmeter.py', "Black Horizontal Bar Meters", 6],
    ['whitehbarmeter.py', "White Horizontal Bar Meters", 6],
    ['hbarmeterorientation.py', "H-Bar Meter Orientation", 4],
    ['vbarmeter.py', "Vertical Bar Meter", 1],
    ['colorvbarmeter.py', "Color Vertical Bar Meters", 6],
    ['blackvbarmeter.py', "Black Vertical Bar Meters", 6],
    ['whitevbarmeter.py', "White Vertical Bar Meters", 6],
    ['vbarmeterorientation.py', "V-Bar Meter Orientation", 4],
    ['', ""],
    ['', "Clickable Charts"],
    ['clickbar.py', "Simple Clickable Charts", 0],
    ['jsclick.py', "Javascript Clickable Chart", 0],
    ['customclick.py', "Custom Clickable Objects", 0],
    ['', ""],
    ['', "Working With Database"],
    ['dbdemo1.py', "Database Integration (1)", 0],
    ['dbdemo2.py', "Database Integration (2)", 0],
    ['dbdemo3.py', "Database Clickable Charts", 0],
    ['', ""],
    ['', "Programmable Track Cursor"],
    ['tracklegend.py', "Track Line with Legend", 0],
    ['tracklabel.py', "Track Line with Data Labels", 0],
    ['trackaxis.py', "Track Line with Axis Labels", 0],
    ['trackvlegend.py', "Track Line with Vertical Legend", 0],
    ['trackbox.py', "Track Box with Floating Legend", 0],
    ['trackfinance.py', "Finance Chart Track Line", 0],
    ['crosshair.py', "Crosshair with Axis Labels", 0],
    ['', ""],
    ['', "Zooming and Scrolling"],
    ['<a href="javascript:window.open(\\'simplezoomscroll.py\\', \\'simplezoomscroll\\').focus();">', "Simple Zooming and Scrolling", -1],
    ['<a href="javascript:window.open(\\'zoomscrolltrack.py\\', \\'zoomscrolltrack\\').focus();">', "Zoom/Scroll with Track Line", -1],
    ['<a href="javascript:window.open(\\'viewportcontroldemo.py\\', \\'viewportcontroldemo\\').focus();">', "Zoom/Scroll Viewport Control", -1],
    ['<a href="javascript:window.open(\\'xyzoomscroll.py\\', \\'xyzoomscroll\\').focus();">', "XY Zooming and Scrolling", -1],
    ['', ""],
    ['', "Realtime Charts"],
    ['<a href="javascript:window.open(\\'realtimedemo.py\\', \\'realtimedemo\\').focus();">', "Simple Realtime Chart", -1],
    ['<a href="javascript:window.open(\\'realtimesnapshot.py\\', \\'realtimesnapshot\\').focus();">', "Realtime Chart with Snapshot", -1],
    ['<a href="javascript:window.open(\\'realtimetrack.py\\', \\'realtimetrack\\').focus();">', "Realtime Chart with Track Line", -1],
    ['', ""]
    ];
function setChart(c)
{
    var doc = top.indexright.document;
    doc.open();
    doc.writeln('<body style="margin:5px 0px 0px 5px">');
    doc.writeln('<div style="font-size:18pt; font-family:verdana; font-weight:bold">');
    doc.writeln('    ' + charts[c][1]);
    doc.writeln('</div>');
    doc.writeln('<hr style="border:solid 1px #000080" />');
    doc.writeln('<div style="font-size:10pt; font-family:verdana; margin-bottom:1.5em">');
    doc.writeln('    <a href="viewsource.py?file=' + charts[c][0] + '">View Chart Source Code</a>');
    doc.writeln('</div>');
    if (charts[c][2] > 1)
    {
        for (var i = 0; i < charts[c][2]; ++i)
            doc.writeln('<img src="' + charts[c][0] + '?img=' + i + '">');
    }
    else
        doc.writeln('<img src="' + charts[c][0] + '">');
    doc.writeln('</body>');
    doc.close();
}
</script>
<style type="text/css">
p.demotitle {margin-top:1; margin-bottom:2; padding-left:1; font-family:verdana; font-weight:bold; font-size:9pt;}
p.demolink {margin-top:0; margin-bottom:0; padding-left:3; padding-top:2; padding-bottom:1; font-family:verdana; font-size:8pt;}
</style>
</head>
<body style="margin:0px">
<table width="100%" border="0" cellpadding="0" cellspacing="0" style="font-family:verdana; font-size:8pt;">
<script language="Javascript">
for (var c in charts)
{
    if (charts[c][1] == "")
        document.writeln('<tr><td><p class="demolink">&nbsp;</p></td></tr>');
    if (charts[c][0] == "")
        document.writeln('<tr><td colspan="2" bgcolor="#9999FF"><p class="demotitle">' + charts[c][1] + '</p></td></tr>');
    else
    {
        document.write('<tr valign="top"><td><p class="demolink">&#8226;</p></td><td><p class="demolink">');
        if (charts[c][2] > 0)
            document.write('<a href="javascript:;" onclick="setChart(\\'' + c + '\\');">');
        else if (charts[c][2] == 0)
               document.write('<a href="' + charts[c][0] + '" target="indexright">');
        else
               document.write(charts[c][0]);
           document.write(charts[c][1]);
           document.writeln('</a></p></td></tr>');
    }
}
</script>
</table>
</body>
</html>
""")
