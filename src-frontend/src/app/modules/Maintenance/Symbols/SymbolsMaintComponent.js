import * as AppConsts from '../../../AppConsts';

import FormUtils from '../../../appUtils/FormUtils';
import NumberUtils from '../../../appUtils/NumberUtils';
import PropUtils from '../../../appUtils/PropUtils';
import React from 'react';
import StockDataService from '../../../services/data/StockDataService';
import SymbolsMaintTemplate from './SymbolsMaintTemplate';

export default class SymbolsMaintComponent extends React.Component {
  constructor(props) {
    super(props);
    this._stockDataService = new StockDataService();
    this.state = {
      is_processing: false,
      is_snackbar_open: false,
      snackbar_content: '',
      is_modal_open: false,
      query: 'MSFT',
      symbolsInView: [],
      symbolsAll: [],
      request: {},
      onChangeQuery: this.onChangeQuery,
      onChangeRequest: this.onChangeRequest,
      onBlurRequest: this.onBlurRequest,
      onKeyPress: this.onKeyPress,
      onClickEdit: this.onClickEdit,
      onClickSave: this.onClickSave,
      onCloseSnackbar: this.onCloseSnackbar,
      onCloseModal: this.onCloseModal,
    };
  }

  componentDidMount() {
    this.getSymbols();
  }

  getSymbols = () => {
    this._stockDataService
      .getSymbols(AppConsts.INSTRUMENT_STOCK)
      .then((resp) => {
        console.log('response', resp);
        if (resp?.http_status_code === AppConsts.HTTP_STATUS_CODE_OK && resp.data && resp.data.length > 0) {
          this.setState(() => ({ symbolsAll: resp.data }));
          this.getSymbolsFiltered();
          FormUtils.focusFirstInput();
        } else {
          this.setState(() => ({
            is_processing: false,
            is_snackbar_open: true,
            snackbar_content: `Error [${resp.http_status_code}]: ${resp.error_message}`,
          }));
        }
      })
      .fail((resp) => {
        console.log('response', resp);
        this.setState(() => ({
          is_processing: false,
          is_snackbar_open: true,
          snackbar_content: 'ERROR!',
        }));
      });
  };

  getSymbolsFiltered = () => {
    var filtered = !this.state.query
      ? []
      : this.state.symbolsAll.filter((s) => {
          return (
            s.symbol.startsWith(this.state.query.toUpperCase()) ||
            s.name.toUpperCase().startsWith(this.state.query.toUpperCase())
          );
        });
    this.setState((state) => ({ symbolsInView: filtered }));
  };

  onChangeQuery = (event) => {
    const { value } = event?.target;
    this.setState((state) => ({ query: value ? value.trim() : '' }));
  };

  onBlurRequest = (event, fieldName, fieldValue) => {
    this.setState((state) => ({
      request: PropUtils.setValue(state.request, fieldName, fieldValue),
    }));
  };

  onChangeRequest = (event) => {
    const { name, value } = event?.target;
    this.setState((state) => ({
      request: PropUtils.setValue(state.request, name, value),
    }));
  };

  onKeyPress = (event) => {
    const key = event?.key;
    if (key === 'Enter') {
      this.getSymbolsFiltered();
    }
  };

  onClickEdit = (symbol) => {
    this.setState(() => ({
      is_modal_open: true,
      request: {
        ...symbol,
        is_excluded_from_trade: NumberUtils.hasBit(symbol.status, AppConsts.SYMBOL_STATUS_EXCLUDE_TRADE),
      },
    }));
  };

  onClickSave = () => {
    if (this.state.is_processing) {
      return;
    }

    this.setState(() => ({ is_processing: true }));
    var req = this.state.request;
    req.status = req.is_excluded_from_trade
      ? NumberUtils.addBit(req.status, AppConsts.SYMBOL_STATUS_EXCLUDE_TRADE)
      : NumberUtils.deleteBit(req.status, AppConsts.SYMBOL_STATUS_EXCLUDE_TRADE);
    console.log('request', this.state.request);

    this._stockDataService
      .updateSymbol(req)
      .then((resp) => {
        console.log(resp);
        if (resp?.http_status_code === AppConsts.HTTP_STATUS_CODE_OK) {
          this.getSymbols();
          this.setState(() => ({
            is_processing: false,
            is_modal_open: false,
            is_snackbar_open: true,
            snackbar_content: 'Successfully Saved.',
          }));
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
    return <SymbolsMaintTemplate {...this.state} />;
  }
}
