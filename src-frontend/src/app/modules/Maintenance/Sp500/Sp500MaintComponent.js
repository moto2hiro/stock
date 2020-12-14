import * as AppConsts from '../../../AppConsts';

import ImportDataService from '../../../services/data/ImportDataService';
import React from 'react';
import Sp500MaintTemplate from './Sp500MaintTemplate';
import StockDataService from '../../../services/data/StockDataService';

export default class Sp500MaintComponent extends React.Component {
  constructor(props) {
    super(props);
    this._stockDataService = new StockDataService();
    this._importDataService = new ImportDataService();
    this.state = {
      is_processing: false,
      is_snackbar_open: false,
      snackbar_content: '',
      new_sp500_symbols: null,
      non_sp500_symbols: null,
      onClickImport: this.onClickImport,
      onCloseSnackbar: this.onCloseSnackbar,
    };
  }

  onClickImport = () => {
    if (this.state.is_processing) {
      return;
    }

    this.setState(() => ({ is_processing: true }));
    this._importDataService
      .importSymbols()
      .then((resp) => {
        if (resp?.http_status_code === AppConsts.HTTP_STATUS_CODE_OK) {
          this.setState(() => ({
            is_processing: false,
            is_snackbar_open: true,
            snackbar_content: 'Successfully Imported.',
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

  render() {
    return <Sp500MaintTemplate {...this.state} />;
  }
}
