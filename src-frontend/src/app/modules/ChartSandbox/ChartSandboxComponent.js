import * as AppConsts from '../../AppConsts';

import ChartSandboxTemplate from './ChartSandboxTemplate';
import FormUtils from '../../appUtils/FormUtils';
import GoogleChartService from '../../services/GoogleChartService';
import NumberUtils from '../../appUtils/NumberUtils';
import PropUtils from '../../appUtils/PropUtils';
import React from 'react';
import StockDataService from '../../services/data/StockDataService';

export default class ChartSandboxComponent extends React.Component {
  constructor(props) {
    super(props);
    this._stockDataService = new StockDataService();
    this.state = {
      has_run_charts: false,
      is_processing: false,
      is_snackbar_open: false,
      snackbar_content: '',
      request: {
        is_random_symbols: true,
        no_of_charts: 5,
        symbol: 'MSFT',
        date_from: '2005-01-01',
        date_to: '2005-06-01',
        is_exclude_sma: true,
        sma_period_1: 20,
        sma_period_1_color: AppConsts.COLOR_TURQUOISE,
        sma_period_2: 100,
        sma_period_2_color: AppConsts.COLOR_PURPLE,
        is_exclude_exponential_smoothing_prices: false,
        exponential_smoothing_prices_color: AppConsts.COLOR_YELLOW,
        exponential_smoothing_prices_shift: 1.05,
        exponential_smoothing_alpha: 0.8,
        is_exclude_exponential_smoothing_max_min: false,
        exponential_smoothing_max_min_color: AppConsts.COLOR_ORANGE,
        exponential_smoothing_max_min_diff: 0.7,
        is_exclude_abz: true,
        abz_er_period: 10,
        abz_std_distance: 0.8,
        abz_constant_k: 60,
        abz_middle_color: AppConsts.COLOR_BROWN,
        abz_upper_color: AppConsts.COLOR_BROWN,
        abz_lower_color: AppConsts.COLOR_BROWN,
      },
      validation: { isInvalid: false, formData: {} },
      chartItems: [],
      chartOptions: {},
      onChangeRequest: this.onChangeRequest,
      onBlurRequest: this.onBlurRequest,
      onClickGetCharts: this.onClickGetCharts,
      onCloseSnackbar: this.onCloseSnackbar,
    };
  }

  onChangeRequest = (event) => {
    const { name, value } = event?.target;
    this.setState((state) => ({
      request: PropUtils.setValue(state.request, name, value),
    }));
  };

  onBlurRequest = (event, fieldName, fieldValue) => {
    this.setState((state) => ({
      request: PropUtils.setValue(state.request, fieldName, fieldValue),
    }));
    this.validate();
  };

  onClickGetCharts = () => {
    this.validate();
    if (this.state.validation.isInvalid) {
      FormUtils.focusInvalidInput();
      return;
    }

    this.setState(() => ({ has_run_get_charts: true }));

    if (this.state.is_processing) {
      return;
    }

    this.setState(() => ({
      is_processing: true,
      chartItems: [],
      chartOptions: {},
    }));
    console.log('request', this.state.request);

    this._stockDataService
      .getSamplePricesForCharts(this.state.request)
      .then((resp) => {
        console.log('response', resp);
        if (resp?.http_status_code === AppConsts.HTTP_STATUS_CODE_OK && resp.data && resp.data.length > 0) {
          let chartItems = [];
          resp.data.forEach((items) => {
            if (items) {
              let headers = [
                AppConsts.PRICE_COL_DATE,
                AppConsts.PRICE_COL_LOW,
                AppConsts.PRICE_COL_OPEN,
                AppConsts.PRICE_COL_CLOSE,
                AppConsts.PRICE_COL_HIGH,
              ];
              if (!this.state.request.is_exclude_sma) {
                headers.push(`${AppConsts.CUSTOM_COL_SMA}_${this.state.request.sma_period_1}`);
                headers.push(`${AppConsts.CUSTOM_COL_SMA}_${this.state.request.sma_period_2}`);
              }
              if (!this.state.request.is_exclude_exponential_smoothing_prices) {
                headers.push(AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_PRICE);
              }
              if (!this.state.request.is_exclude_exponential_smoothing_max_min) {
                headers.push(AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_MAX);
              }
              if (!this.state.request.is_exclude_abz) {
                headers.push(AppConsts.CUSTOM_COL_ABZ_MIDDLE);
                headers.push(AppConsts.CUSTOM_COL_ABZ_UPPER);
                headers.push(AppConsts.CUSTOM_COL_ABZ_LOWER);
              }
              let mappedData = [headers];
              items.forEach((item) => {
                let dataRow = [
                  item.price_date,
                  NumberUtils.toFloat(item.low_price),
                  NumberUtils.toFloat(item.open_price),
                  NumberUtils.toFloat(item.close_price),
                  NumberUtils.toFloat(item.high_price),
                ];
                if (!this.state.request.is_exclude_sma) {
                  var val1 = item.sma_period_1 ? NumberUtils.toFloat(item.sma_period_1) : null;
                  var val2 = item.sma_period_2 ? NumberUtils.toFloat(item.sma_period_2) : null;
                  dataRow.push(val1);
                  dataRow.push(val2);
                }
                if (!this.state.request.is_exclude_exponential_smoothing_prices) {
                  dataRow.push(
                    NumberUtils.toFloat(
                      item.exponential_smoothing_price * this.state.request.exponential_smoothing_prices_shift
                    )
                  );
                }
                if (!this.state.request.is_exclude_exponential_smoothing_max_min) {
                  if (item.is_exponential_smoothing_max || item.is_exponential_smoothing_min) {
                    dataRow.push(
                      NumberUtils.toFloat(
                        item.exponential_smoothing_price * this.state.request.exponential_smoothing_prices_shift
                      )
                    );
                  } else {
                    dataRow.push(null);
                  }
                }
                if (!this.state.request.is_exclude_abz) {
                  dataRow.push(NumberUtils.toFloat(item.abz_middle));
                  dataRow.push(NumberUtils.toFloat(item.abz_upper));
                  dataRow.push(NumberUtils.toFloat(item.abz_lower));
                }
                mappedData.push(dataRow);
              });
              chartItems.push(mappedData);
            }

            let extraChartSeries = [];
            if (!this.state.request.is_exclude_sma) {
              extraChartSeries.push(GoogleChartService.getLineSeries(this.state.request.sma_period_1_color));
              extraChartSeries.push(GoogleChartService.getLineSeries(this.state.request.sma_period_2_color));
            }
            if (!this.state.request.is_exclude_exponential_smoothing_prices) {
              extraChartSeries.push(
                GoogleChartService.getLineSeries(this.state.request.exponential_smoothing_prices_color)
              );
            }
            if (!this.state.request.is_exclude_exponential_smoothing_max_min) {
              extraChartSeries.push(
                GoogleChartService.getScatterSeries(this.state.request.exponential_smoothing_max_min_color)
              );
            }
            if (!this.state.request.is_exclude_abz) {
              extraChartSeries.push(GoogleChartService.getLineSeries(this.state.request.abz_middle_color));
              extraChartSeries.push(GoogleChartService.getLineSeries(this.state.request.abz_upper_color));
              extraChartSeries.push(GoogleChartService.getLineSeries(this.state.request.abz_lower_color));
            }
            let chartOptions = GoogleChartService.get_candle_stick_combo_options(extraChartSeries);
            this.setState({
              is_processing: false,
              chartItems: chartItems,
              chartOptions: chartOptions,
            });
          });
        } else {
          this.setState(() => ({
            is_processing: false,
            is_snackbar_open: true,
            snackbar_content: `Error [${resp.http_status_code}]: ${resp.error_message}`,
          }));
        }
      })
      .fail((resp) => {
        console.log(resp);
        this.setState(() => ({
          is_processing: false,
          is_snackbar_open: true,
          snackbar_content: 'ERROR!',
        }));
      });
  };

  onCloseSnackbar = () => {
    this.setState(() => ({ is_snackbar_open: false }));
  };

  componentDidUpdate() {
    if (this.state.is_processing && document.querySelector('.resultsDiv')) {
      document.querySelector('.resultsDiv').scrollIntoView({ behavior: 'smooth' });
    }
  }

  validate = () => {
    var ruleObj = {
      date_from: {
        required: true,
        min: AppConsts.MIN_DATE,
        lessThan: 'date_to',
      },
      date_to: {
        required: true,
        min: AppConsts.MIN_DATE,
        greaterThan: 'date_from',
      },
      sma_period_1: {
        required: true,
        min: 1,
        max: 200,
        notEqual: 'sma_period_2',
      },
      sma_period_2: {
        required: true,
        min: 1,
        max: 200,
        notEqual: 'sma_period_1',
      },
      exponential_smoothing_prices_shift: {
        required: true,
        min: 0.9,
        max: 1.1,
      },
      exponential_smoothing_alpha: {
        required: true,
        min: 0.01,
        max: 1,
      },
      exponential_smoothing_max_min_diff: {
        required: true,
        min: 0.01,
        max: 5,
      },
      abz_er_period: {
        required: true,
        min: 1,
        max: 100,
      },
      abz_std_distance: {
        required: true,
        min: 0.01,
        max: 5,
      },
      abz_constant_k: {
        required: true,
        min: 0.01,
        max: 200,
      },
    };
    if (this.state.request.is_random_symbols) {
      ruleObj.no_of_charts = {
        required: true,
        min: 1,
        max: 10,
      };
    } else {
      ruleObj.symbol = {
        required: true,
      };
    }
    var validation = FormUtils.validate(this.state.request, ruleObj);
    this.setState((state) => ({ validation: validation }));
  };

  render() {
    return <ChartSandboxTemplate {...this.state} />;
  }
}
