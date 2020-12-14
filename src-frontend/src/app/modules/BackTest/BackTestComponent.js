import * as AppConsts from '../../AppConsts';

import BackTestDataService from '../../services/data/BackTestDataService';
import BackTestTemplate from './BackTestTemplate';
import FormUtils from '../../appUtils/FormUtils';
import PropUtils from '../../appUtils/PropUtils';
import React from 'react';

export default class BackTestComponent extends React.Component {
  constructor(props) {
    super(props);
    this._backTestDataService = new BackTestDataService();
    this.state = {
      has_run_back_test: false,
      is_processing: false,
      is_snackbar_open: false,
      snackbar_content: '',
      current_strategy_config: AppConsts.STRATEGY_CONFIG[AppConsts.STRATEGY_DOUBLE_BOTTOMS],
      request: {
        start_capital: 120000,
        pct_risk_per_trade: 10,
        portfolio_max: 100,
        benchmark_etfs: [AppConsts.BENCHMARK_ETF_SPY, AppConsts.BENCHMARK_ETF_DIA],
        date_from: '2019-01-01',
        date_to: '2020-01-01',
        slippage: 10,
        volume_limit: 0.01,
        test_limit_symbol: 20,
        adv_min: AppConsts.ADV_MIN_DFLT,
        adpv_min: AppConsts.ADPV_MIN_DFLT,
        strategy_type: AppConsts.STRATEGY_DOUBLE_BOTTOMS,
        strategy_request: {
          exponential_smoothing_alpha: 0.8,
          exponential_smoothing_max_min_diff: 0.7,
          double_bottoms_diff: 1,
        },
      },
      validation: { isInvalid: false, formData: { strategy_request: {} } },
      results: [],
      chart_data: [],
      onChangeRequest: this.onChangeRequest,
      onBlurRequest: this.onBlurRequest,
      onDeleteBenchmark: this.onDeleteBenchmark,
      onClickRunBackTest: this.onClickRunBackTest,
      onCloseSnackbar: this.onCloseSnackbar,
    };
  }

  onChangeRequest = (event) => {
    const { name, value } = event?.target;
    this.setState((state) => ({
      request: PropUtils.setValue(state.request, name, value),
    }));

    if (name === 'strategy_type') {
      var config = AppConsts.STRATEGY_CONFIG[value];
      this.setState((state) => ({
        current_strategy_config: config,
        request: {
          ...state.request,
          strategy_request: {},
        },
      }));
      if (config && config.fields) {
        config.fields.forEach((field) => {
          this.setState((state) => ({
            request: PropUtils.setValue(state.request, `strategy_request.${field?.name}`, field?.default),
          }));
        });
      }
      this.validate();
    }
  };

  onBlurRequest = (event, fieldName, fieldValue) => {
    this.setState((state) => ({
      request: PropUtils.setValue(state.request, fieldName, fieldValue),
    }));
    this.validate();
  };

  onDeleteBenchmark = (value) => {
    this.setState((state) => ({
      request: {
        ...state.request,
        benchmark_etfs: state.request.benchmark_etfs.filter((b) => b !== value),
      },
    }));
  };

  onClickRunBackTest = () => {
    this.validate();
    if (this.state.validation.isInvalid) {
      FormUtils.focusInvalidInput();
      return;
    }

    this.setState(() => ({ has_run_back_test: true }));

    if (this.state.is_processing) {
      return;
    }

    this.setState(() => ({
      is_processing: true,
      results: [],
      chart_data: [],
    }));
    console.log('request', this.state.request);

    this._backTestDataService
      .run(this.state.request)
      .then((resp) => {
        console.log('response', resp);

        window.response = resp;

        if (resp?.http_status_code === AppConsts.HTTP_STATUS_CODE_OK && resp.data.back_test_result_items) {
          let chart_data = [];
          let labels = ['symbol-date'];
          resp.data.back_test_result_items.forEach((item) => {
            labels.push(item.target);
          });
          chart_data.push(labels);

          for (let date in resp.data.back_test_result_items[0].capital) {
            let capital = [date];
            resp.data.back_test_result_items.forEach((item) => {
              capital.push(item.capital[date]);
            });
            chart_data.push(capital);
          }

          this.setState({
            results: resp.data.back_test_result_items,
            chart_data: chart_data,
            is_processing: false,
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
      start_capital: {
        required: true,
        min: 100,
      },
      pct_risk_per_trade: {
        required: true,
        min: 0.01,
        max: 100,
      },
      portfolio_max: {
        required: true,
        min: 1,
        max: 200,
      },
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
      slippage: {
        required: true,
        min: 0,
        max: 100,
      },
      test_limit_symbol: {
        required: true,
        min: 1,
      },
      adv_min: {
        required: true,
        min: 1,
      },
      adpv_min: {
        required: true,
        min: 0.01,
      },
      strategy_request: {},
    };
    this.state.current_strategy_config.fields.forEach(function(field) {
      ruleObj.strategy_request[field.name] = field.validation;
    });
    var validation = FormUtils.validate(this.state.request, ruleObj);
    this.setState((state) => ({ validation: validation }));
  };

  render() {
    return <BackTestTemplate {...this.state} />;
  }
}
