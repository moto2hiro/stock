import * as AppConsts from '../../../AppConsts';

import DateUtils from '../../../appUtils/DateUtils';
import React from 'react';
import TradeDataService from '../../../services/data/TradeDataService';
import TradeSuggestionsTemplate from './TradeSuggestionsTemplate';

export default class TradeSuggestionsComponent extends React.Component {
  constructor(props) {
    super(props);
    this._tradeDataService = new TradeDataService();
    this.state = {
      is_processing: false,
      is_snackbar_open: false,
      snackbar_content: '',
      is_modal_open: false,
      created: DateUtils.toYYYY_MM_DD(new Date()),
      results: [],
      has_key_info: false,
      key_info: {},
      onClickSymbol: this.onClickSymbol,
      onChangeRequest: this.onChangeRequest,
      onBlurRequest: this.onBlurRequest,
      onCloseSnackbar: this.onCloseSnackbar,
      onCloseModal: this.onCloseModal,
    };
  }

  componentDidMount() {
    this.getTradeOrders();
  }

  onClickSymbol = (symbol) => {
    this.setState(() => ({ has_key_info: false, key_info: {} }));
    this._tradeDataService.getKeyInfo(symbol).then((resp) => {
      console.log('response', resp);
      this.setState(() => ({
        has_key_info: true,
        key_info: {
          symbol: symbol,
          ...resp.data,
        },
        is_modal_open: true,
      }));
      console.log(this.state.key_info);
    });
  };

  onChangeRequest = (event) => {
    const { value } = event?.target;
    this.setState((state) => ({ created: value }));
  };

  onBlurRequest = (event, fieldName, fieldValue) => {
    this.getTradeOrders();
  };

  getTradeOrders = () => {
    this.setState(() => ({
      is_processing: true,
      results: [],
    }));

    console.log('request', this.state.created);

    this._tradeDataService
      .getTradeOrders({ created: this.state.created })
      .then((resp) => {
        console.log('response', resp);
        if (resp?.http_status_code === AppConsts.HTTP_STATUS_CODE_OK && resp.data?.length) {
          this.setState({
            is_processing: false,
            results: resp.data,
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

  onCloseModal = () => {
    this.setState(() => ({ is_modal_open: false }));
  };

  render() {
    return <TradeSuggestionsTemplate {...this.state} />;
  }
}
