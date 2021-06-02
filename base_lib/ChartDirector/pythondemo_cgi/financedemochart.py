#!/usr/bin/python
from FinanceChart import *
import cgi, sys

# Get HTTP query parameters
query = cgi.FieldStorage(keep_blank_values = 1)

#
# Create a finance chart based on user selections, which are encoded as query parameters. This code
# is designed to work with the financedemo HTML form.
#

# The timeStamps, volume, high, low, open and close data
#
# ** NOTE ** : This sample code is written assuming the time stamps are in ChartDirector chartTime
# format. It is because this format supports dates before 1970 (which may be needed in some long
# term charts). See the ChartDirector documentation on chartTime for details. When you retrieve the
# time stamps from your database, please remember to convert them to chartTime.
timeStamps = None
volData = None
highData = None
lowData = None
openData = None
closeData = None

# An extra data series to compare with the close data
compareData = None

# The resolution of the data in seconds. 1 day = 86400 seconds.
resolution = 86400

#/ <summary>
#/ Get the timeStamps, highData, lowData, openData, closeData and volData.
#/ </summary>
#/ <param name="ticker">The ticker symbol for the data series.</param>
#/ <param name="startDate">The starting date/time for the data series.</param>
#/ <param name="endDate">The ending date/time for the data series.</param>
#/ <param name="durationInDays">The number of trading days to get.</param>
#/ <param name="extraPoints">The extra leading data points needed in order to
#/ compute moving averages.</param>
#/ <returns>True if successfully obtain the data, otherwise false.</returns>
def getData(ticker, startDate, endDate, durationInDays, extraPoints) :

    global resolution

    # This method should return false if the ticker symbol is invalid. In this sample code, as we
    # are using a random number generator for the data, all ticker symbol is allowed, but we still
    # assumed an empty symbol is invalid.
    if ticker == "" :
        return 0

    # In this demo, we can get 15 min, daily, weekly or monthly data depending on the time range.
    resolution = 86400
    if durationInDays <= 10 :
        # 10 days or less, we assume 15 minute data points are available
        resolution = 900

        # We need to adjust the startDate backwards for the extraPoints. We assume 6.5 hours trading
        # time per day, and 5 trading days per week.
        dataPointsPerDay = 6.5 * 3600 / resolution
        adjustedStartDate = startDate - startDate % 86400 - int(
            extraPoints / dataPointsPerDay * 7 / 5 + 0.9999999) * 86400 - 2 * 86400

        # Get the required 15 min data
        get15MinData(ticker, adjustedStartDate, endDate)

    elif durationInDays >= 4.5 * 360 :
        # 4 years or more - use monthly data points.
        resolution = 30 * 86400

        # Adjust startDate backwards to cater for extraPoints
        YMD = getChartYMD(startDate)
        currentMonth = int(YMD / 100) % 100 - extraPoints
        currentYear = int(YMD / 10000)
        while currentMonth < 1 :
            currentYear = currentYear - 1
            currentMonth = currentMonth + 12
        adjustedStartDate = chartTime(currentYear, currentMonth, 1)

        # Get the required monthly data
        getMonthlyData(ticker, adjustedStartDate, endDate)

    elif durationInDays >= 1.5 * 360 :
        # 1 year or more - use weekly points.
        resolution = 7 * 86400

        # Adjust startDate backwards to cater for extraPoints
        adjustedStartDate = startDate - extraPoints * 7 * 86400 - 6 * 86400

        # Get the required weekly data
        getWeeklyData(ticker, adjustedStartDate, endDate)

    else :
        # Default - use daily points
        resolution = 86400

        # Adjust startDate backwards to cater for extraPoints. We multiply the days by 7/5 as we
        # assume 1 week has 5 trading days.
        adjustedStartDate = startDate - startDate % 86400 - int((extraPoints * 7 + 4) / 5
            ) * 86400 - 2 * 86400

        # Get the required daily data
        getDailyData(ticker, adjustedStartDate, endDate)

    return 1

#/ <summary>
#/ Get 15 minutes data series for timeStamps, highData, lowData, openData, closeData
#/ and volData.
#/ </summary>
#/ <param name="ticker">The ticker symbol for the data series.</param>
#/ <param name="startDate">The starting date/time for the data series.</param>
#/ <param name="endDate">The ending date/time for the data series.</param>
def get15MinData(ticker, startDate, endDate) :
    #
    # In this demo, we use a random number generator to generate the data. In practice, you may get
    # the data from a database or by other means. If you do not have 15 minute data, you may modify
    # the "drawChart" method below to not using 15 minute data.
    #
    generateRandomData(ticker, startDate, endDate, 900)

#/ <summary>
#/ Get daily data series for timeStamps, highData, lowData, openData, closeData
#/ and volData.
#/ </summary>
#/ <param name="ticker">The ticker symbol for the data series.</param>
#/ <param name="startDate">The starting date/time for the data series.</param>
#/ <param name="endDate">The ending date/time for the data series.</param>
def getDailyData(ticker, startDate, endDate) :
    #
    # In this demo, we use a random number generator to generate the data. In practice, you may get
    # the data from a database or by other means.
    #
    generateRandomData(ticker, startDate, endDate, 86400)

#/ <summary>
#/ Get weekly data series for timeStamps, highData, lowData, openData, closeData
#/ and volData.
#/ </summary>
#/ <param name="ticker">The ticker symbol for the data series.</param>
#/ <param name="startDate">The starting date/time for the data series.</param>
#/ <param name="endDate">The ending date/time for the data series.</param>
def getWeeklyData(ticker, startDate, endDate) :
    #
    # If you do not have weekly data, you may call "getDailyData(startDate, endDate)" to get daily
    # data, then call "convertDailyToWeeklyData()" to convert to weekly data.
    #
    generateRandomData(ticker, startDate, endDate, 86400 * 7)

#/ <summary>
#/ Get monthly data series for timeStamps, highData, lowData, openData, closeData
#/ and volData.
#/ </summary>
#/ <param name="ticker">The ticker symbol for the data series.</param>
#/ <param name="startDate">The starting date/time for the data series.</param>
#/ <param name="endDate">The ending date/time for the data series.</param>
def getMonthlyData(ticker, startDate, endDate) :
    #
    # If you do not have weekly data, you may call "getDailyData(startDate, endDate)" to get daily
    # data, then call "convertDailyToMonthlyData()" to convert to monthly data.
    #
    generateRandomData(ticker, startDate, endDate, 86400 * 30)

#/ <summary>
#/ A random number generator designed to generate realistic financial data.
#/ </summary>
#/ <param name="ticker">The ticker symbol for the data series.</param>
#/ <param name="startDate">The starting date/time for the data series.</param>
#/ <param name="endDate">The ending date/time for the data series.</param>
#/ <param name="resolution">The period of the data series.</param>
def generateRandomData(ticker, startDate, endDate, resolution) :

    global timeStamps, volData, highData, lowData, openData, closeData

    db = FinanceSimulator(ticker, startDate, endDate, resolution)
    timeStamps = db.getTimeStamps()
    highData = db.getHighData()
    lowData = db.getLowData()
    openData = db.getOpenData()
    closeData = db.getCloseData()
    volData = db.getVolData()

#/ <summary>
#/ A utility to convert daily to weekly data.
#/ </summary>
def convertDailyToWeeklyData() :

    global timeStamps

    aggregateData(ArrayMath(timeStamps).selectStartOfWeek())

#/ <summary>
#/ A utility to convert daily to monthly data.
#/ </summary>
def convertDailyToMonthlyData() :

    global timeStamps

    aggregateData(ArrayMath(timeStamps).selectStartOfMonth())

#/ <summary>
#/ An internal method used to aggregate daily data.
#/ </summary>
def aggregateData(aggregator) :

    global timeStamps, volData, highData, lowData, openData, closeData

    timeStamps = aggregator.aggregate(timeStamps, AggregateFirst)
    highData = aggregator.aggregate(highData, AggregateMax)
    lowData = aggregator.aggregate(lowData, AggregateMin)
    openData = aggregator.aggregate(openData, AggregateFirst)
    closeData = aggregator.aggregate(closeData, AggregateLast)
    volData = aggregator.aggregate(volData, AggregateSum)

#/ <summary>
#/ Create a financial chart according to user selections. The user selections are
#/ encoded in the query parameters.
#/ </summary>
def drawChart() :

    global timeStamps, volData, highData, lowData, openData, closeData
    global compareData, resolution

    # In this demo, we just assume we plot up to the latest time. So end date is now.
    endDate = chartTime2(time.time())

    # If the trading day has not yet started (before 9:30am), or if the end date is on on Sat or
    # Sun, we set the end date to 4:00pm of the last trading day
    while (endDate % 86400 < 9 * 3600 + 30 * 60) or (getChartWeekDay(endDate) == 0) or (
        getChartWeekDay(endDate) == 6) :
        endDate = endDate - endDate % 86400 - 86400 + 16 * 3600

    # The duration selected by the user
    durationInDays = int(query["TimeRange"].value)

    # Compute the start date by subtracting the duration from the end date.
    startDate = endDate
    if durationInDays >= 30 :
        # More or equal to 30 days - so we use months as the unit
        YMD = getChartYMD(endDate)
        startMonth = int(YMD / 100) % 100 - int(durationInDays / 30)
        startYear = int(YMD / 10000)
        while startMonth < 1 :
            startYear = startYear - 1
            startMonth = startMonth + 12
        startDate = chartTime(startYear, startMonth, 1)
    else :
        # Less than 30 days - use day as the unit. The starting point of the axis is always at the
        # start of the day (9:30am). Note that we use trading days, so we skip Sat and Sun in
        # counting the days.
        startDate = endDate - endDate % 86400 + 9 * 3600 + 30 * 60
        for i in range(1, durationInDays) :
            if getChartWeekDay(startDate) == 1 :
                startDate = startDate - 3 * 86400
            else :
                startDate = startDate - 86400

    # The moving average periods selected by the user.
    avgPeriod1 = 0
    try: avgPeriod1 = int(query["movAvg1"].value)
    except: pass
    avgPeriod2 = 0
    try: avgPeriod2 = int(query["movAvg2"].value)
    except: pass

    if avgPeriod1 < 0 :
        avgPeriod1 = 0
    elif avgPeriod1 > 300 :
        avgPeriod1 = 300

    if avgPeriod2 < 0 :
        avgPeriod2 = 0
    elif avgPeriod2 > 300 :
        avgPeriod2 = 300

    # We need extra leading data points in order to compute moving averages.
    extraPoints = 20
    if avgPeriod1 > extraPoints :
        extraPoints = avgPeriod1
    if avgPeriod2 > extraPoints :
        extraPoints = avgPeriod2

    # Get the data series to compare with, if any.
    compareKey = string.strip(query["CompareWith"].value)
    compareData = None
    if getData(compareKey, startDate, endDate, durationInDays, extraPoints) :
          compareData = closeData

    # The data series we want to get.
    tickerKey = string.strip(query["TickerSymbol"].value)
    if not getData(tickerKey, startDate, endDate, durationInDays, extraPoints) :
        return errMsg("Please enter a valid ticker symbol")

    # We now confirm the actual number of extra points (data points that are before the start date)
    # as inferred using actual data from the database.
    extraPoints = len(timeStamps)
    for i in range(0, len(timeStamps)) :
        if timeStamps[i] >= startDate :
            extraPoints = i
            break

    # Check if there is any valid data
    if extraPoints >= len(timeStamps) :
        # No data - just display the no data message.
        return errMsg("No data available for the specified time period")

    # In some finance chart presentation style, even if the data for the latest day is not fully
    # available, the axis for the entire day will still be drawn, where no data will appear near the
    # end of the axis.
    if resolution < 86400 :
        # Add extra points to the axis until it reaches the end of the day. The end of day is
        # assumed to be 16:00 (it depends on the stock exchange).
        lastTime = timeStamps[len(timeStamps) - 1]
        extraTrailingPoints = int((16 * 3600 - lastTime % 86400) / resolution)
        for i in range(0, extraTrailingPoints) :
            timeStamps.append(lastTime + resolution * (i + 1))

    #
    # At this stage, all data are available. We can draw the chart as according to user input.
    #

    #
    # Determine the chart size. In this demo, user can select 4 different chart sizes. Default is
    # the large chart size.
    #
    width = 780
    mainHeight = 255
    indicatorHeight = 80

    size = query["ChartSize"].value
    if size == "S" :
        # Small chart size
        width = 450
        mainHeight = 160
        indicatorHeight = 60
    elif size == "M" :
        # Medium chart size
        width = 620
        mainHeight = 215
        indicatorHeight = 70
    elif size == "H" :
        # Huge chart size
        width = 1000
        mainHeight = 320
        indicatorHeight = 90

    # Create the chart object using the selected size
    m = FinanceChart(width)

    # Set the data into the chart object
    m.setData(timeStamps, highData, lowData, openData, closeData, volData, extraPoints)

    #
    # We configure the title of the chart. In this demo chart design, we put the company name as the
    # top line of the title with left alignment.
    #
    m.addPlotAreaTitle(TopLeft, tickerKey)

    # We displays the current date as well as the data resolution on the next line.
    resolutionText = ""
    if resolution == 30 * 86400 :
        resolutionText = "Monthly"
    elif resolution == 7 * 86400 :
        resolutionText = "Weekly"
    elif resolution == 86400 :
        resolutionText = "Daily"
    elif resolution == 900 :
        resolutionText = "15-min"

    m.addPlotAreaTitle(BottomLeft, "<*font=arial.ttf,size=8*>%s - %s chart" % (m.formatValue(
        chartTime2(time.time()), "mmm dd, yyyy"), resolutionText))

    # A copyright message at the bottom left corner the title area
    m.addPlotAreaTitle(BottomRight, "<*font=arial.ttf,size=8*>(c) Advanced Software Engineering")

    #
    # Add the first techical indicator according. In this demo, we draw the first indicator on top
    # of the main chart.
    #
    addIndicator(m, query["Indicator1"].value, indicatorHeight)

    #
    # Add the main chart
    #
    m.addMainChart(mainHeight)

    #
    # Set log or linear scale according to user preference
    #
    if query["LogScale"].value == "1" :
        m.setLogScale(1)

    #
    # Set axis labels to show data values or percentage change to user preference
    #
    if query["PercentageScale"].value == "1" :
        m.setPercentageAxis()

    #
    # Draw any price line the user has selected
    #
    mainType = query["ChartType"].value
    if mainType == "Close" :
        m.addCloseLine(0x000040)
    elif mainType == "TP" :
        m.addTypicalPrice(0x000040)
    elif mainType == "WC" :
        m.addWeightedClose(0x000040)
    elif mainType == "Median" :
        m.addMedianPrice(0x000040)

    #
    # Add comparison line if there is data for comparison
    #
    if compareData != None :
        if len(compareData) > extraPoints :
            m.addComparison(compareData, 0x0000ff, compareKey)

    #
    # Add moving average lines.
    #
    addMovingAvg(m, query["avgType1"].value, avgPeriod1, 0x663300)
    addMovingAvg(m, query["avgType2"].value, avgPeriod2, 0x9900ff)

    #
    # Draw candlesticks or OHLC symbols if the user has selected them.
    #
    if mainType == "CandleStick" :
        m.addCandleStick(0x33ff33, 0xff3333)
    elif mainType == "OHLC" :
        m.addHLOC(0x008800, 0xcc0000)

    #
    # Add parabolic SAR if necessary
    #
    if query["ParabolicSAR"].value == "1" :
        m.addParabolicSAR(0.02, 0.02, 0.2, DiamondShape, 5, 0x008800, 0x000000)

    #
    # Add price band/channel/envelop to the chart according to user selection
    #
    bandType = query["Band"].value
    if bandType == "BB" :
        m.addBollingerBand(20, 2, 0x9999ff, 0xc06666ff)
    elif bandType == "DC" :
        m.addDonchianChannel(20, 0x9999ff, 0xc06666ff)
    elif bandType == "Envelop" :
        m.addEnvelop(20, 0.1, 0x9999ff, 0xc06666ff)

    #
    # Add volume bars to the main chart if necessary
    #
    if query["Volume"].value == "1" :
        m.addVolBars(indicatorHeight, 0x99ff99, 0xff9999, 0xc0c0c0)

    #
    # Add additional indicators as according to user selection.
    #
    addIndicator(m, query["Indicator2"].value, indicatorHeight)
    addIndicator(m, query["Indicator3"].value, indicatorHeight)
    addIndicator(m, query["Indicator4"].value, indicatorHeight)

    return m

#/ <summary>
#/ Add a moving average line to the FinanceChart object.
#/ </summary>
#/ <param name="m">The FinanceChart object to add the line to.</param>
#/ <param name="avgType">The moving average type (SMA/EMA/TMA/WMA).</param>
#/ <param name="avgPeriod">The moving average period.</param>
#/ <param name="color">The color of the line.</param>
#/ <returns>The LineLayer object representing line layer created.</returns>
def addMovingAvg(m, avgType, avgPeriod, color) :
    if avgPeriod > 1 :
        if avgType == "SMA" :
            return m.addSimpleMovingAvg(avgPeriod, color)
        elif avgType == "EMA" :
            return m.addExpMovingAvg(avgPeriod, color)
        elif avgType == "TMA" :
            return m.addTriMovingAvg(avgPeriod, color)
        elif avgType == "WMA" :
            return m.addWeightedMovingAvg(avgPeriod, color)
    return None

#/ <summary>
#/ Add an indicator chart to the FinanceChart object. In this demo example, the
#/ indicator parameters (such as the period used to compute RSI, colors of the lines,
#/ etc.) are hard coded to commonly used values. You are welcome to design a more
#/ complex user interface to allow users to set the parameters.
#/ </summary>
#/ <param name="m">The FinanceChart object to add the line to.</param>
#/ <param name="indicator">The selected indicator.</param>
#/ <param name="height">Height of the chart in pixels</param>
#/ <returns>The XYChart object representing indicator chart.</returns>
def addIndicator(m, indicator, height) :
    if indicator == "RSI" :
        return m.addRSI(height, 14, 0x800080, 20, 0xff6666, 0x6666ff)
    elif indicator == "StochRSI" :
        return m.addStochRSI(height, 14, 0x800080, 30, 0xff6666, 0x6666ff)
    elif indicator == "MACD" :
        return m.addMACD(height, 26, 12, 9, 0x0000ff, 0xff00ff, 0x008000)
    elif indicator == "FStoch" :
        return m.addFastStochastic(height, 14, 3, 0x006060, 0x606000)
    elif indicator == "SStoch" :
        return m.addSlowStochastic(height, 14, 3, 0x006060, 0x606000)
    elif indicator == "ATR" :
        return m.addATR(height, 14, 0x808080, 0x0000ff)
    elif indicator == "ADX" :
        return m.addADX(height, 14, 0x008000, 0x800000, 0x000080)
    elif indicator == "DCW" :
        return m.addDonchianWidth(height, 20, 0x0000ff)
    elif indicator == "BBW" :
        return m.addBollingerWidth(height, 20, 2, 0x0000ff)
    elif indicator == "DPO" :
        return m.addDPO(height, 20, 0x0000ff)
    elif indicator == "PVT" :
        return m.addPVT(height, 0x0000ff)
    elif indicator == "Momentum" :
        return m.addMomentum(height, 12, 0x0000ff)
    elif indicator == "Performance" :
        return m.addPerformance(height, 0x0000ff)
    elif indicator == "ROC" :
        return m.addROC(height, 12, 0x0000ff)
    elif indicator == "OBV" :
        return m.addOBV(height, 0x0000ff)
    elif indicator == "AccDist" :
        return m.addAccDist(height, 0x0000ff)
    elif indicator == "CLV" :
        return m.addCLV(height, 0x0000ff)
    elif indicator == "WilliamR" :
        return m.addWilliamR(height, 14, 0x800080, 30, 0xff6666, 0x6666ff)
    elif indicator == "Aroon" :
        return m.addAroon(height, 14, 0x339933, 0x333399)
    elif indicator == "AroonOsc" :
        return m.addAroonOsc(height, 14, 0x0000ff)
    elif indicator == "CCI" :
        return m.addCCI(height, 20, 0x800080, 100, 0xff6666, 0x6666ff)
    elif indicator == "EMV" :
        return m.addEaseOfMovement(height, 9, 0x006060, 0x606000)
    elif indicator == "MDX" :
        return m.addMassIndex(height, 0x800080, 0xff6666, 0x6666ff)
    elif indicator == "CVolatility" :
        return m.addChaikinVolatility(height, 10, 10, 0x0000ff)
    elif indicator == "COscillator" :
        return m.addChaikinOscillator(height, 0x0000ff)
    elif indicator == "CMF" :
        return m.addChaikinMoneyFlow(height, 21, 0x008000)
    elif indicator == "NVI" :
        return m.addNVI(height, 255, 0x0000ff, 0x883333)
    elif indicator == "PVI" :
        return m.addPVI(height, 255, 0x0000ff, 0x883333)
    elif indicator == "MFI" :
        return m.addMFI(height, 14, 0x800080, 30, 0xff6666, 0x6666ff)
    elif indicator == "PVO" :
        return m.addPVO(height, 26, 12, 9, 0x0000ff, 0xff00ff, 0x008000)
    elif indicator == "PPO" :
        return m.addPPO(height, 26, 12, 9, 0x0000ff, 0xff00ff, 0x008000)
    elif indicator == "UO" :
        return m.addUltimateOscillator(height, 7, 14, 28, 0x800080, 20, 0xff6666, 0x6666ff)
    elif indicator == "Vol" :
        return m.addVolIndicator(height, 0x99ff99, 0xff9999, 0xc0c0c0)
    elif indicator == "TRIX" :
        return m.addTRIX(height, 12, 0x0000ff)
    return None

#/ <summary>
#/ Creates a dummy chart to show an error message.
#/ </summary>
#/ <param name="msg">The error message.
#/ <returns>The BaseChart object containing the error message.</returns>
def errMsg(msg) :
    m = MultiChart(400, 200)
    m.addTitle2(Center, msg, "arial.ttf", 10).setMaxWidth(m.getWidth())
    return m

# create the finance chart
c = drawChart()

# Output the chart
print("Content-type: image/png\n")
binaryPrint(c.makeChart2(PNG))

