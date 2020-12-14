import * as AppConsts from '../AppConsts';

// https://developers.google.com/chart
// and
// https://www.npmjs.com/package/react-google-charts
const GoogleChartService = {
  get_candle_stick_combo_options: function(extraSeries) {
    var ret = {
      legend: 'none',
      backgroundColor: AppConsts.COLOR_BLACK,
      candlestick: {
        fallingColor: {
          fill: AppConsts.COLOR_RED,
          stroke: AppConsts.COLOR_RED,
        },
        risingColor: {
          fill: AppConsts.COLOR_GREEN,
          stroke: AppConsts.COLOR_GREEN,
        },
      },
      chartArea: {
        backgroundColor: AppConsts.COLOR_BLACK,
      },
      hAxis: {
        baselineColor: AppConsts.COLOR_BLACK,
        gridlines: { count: 0 },
        minorGridlines: { count: 0 },
        textPosition: 'none',
      },
      vAxis: {
        baselineColor: AppConsts.COLOR_BLACK,
        gridlines: { count: 0 },
        minorGridlines: { count: 0 },
        textPosition: 'none',
      },
      seriesType: AppConsts.GOOGLE_CHART_SERIES_CANDLE,
      series: {},
    };

    if (extraSeries) {
      extraSeries.forEach((item, i) => {
        ret.series[i + 1] = item;
      });
    }

    return ret;
  },

  getLineSeries(color) {
    return {
      type: AppConsts.GOOGLE_CHART_SERIES_LINE,
      lineWidth: 1,
      color: color,
    };
  },

  getScatterSeries(color) {
    return {
      type: AppConsts.GOOGLE_CHART_SERIES_SCATTER,
      pointSize: 10,
      color: color,
      dataOpacity: 0.5,
    };
  },
};

export default GoogleChartService;
