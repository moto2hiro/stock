import * as AppConsts from '../../../AppConsts';

import ImportDataService from '../../../services/data/ImportDataService';
import PriceDataMaintTemplate from './PriceDataMaintTemplate';
import React from 'react';
import StockDataService from '../../../services/data/StockDataService';

export default class PriceDataMaintComponent extends React.Component {
  constructor(props) {
    super(props);
    this._importDataService = new ImportDataService();
    this._stockDataService = new StockDataService();
    this.state = {
      is_processing: false, //true, // false,
      is_snackbar_open: false,
      snackbar_content: '',
      onClickImport: this.onClickImport,
      onClickDelete: this.onClickDelete,
      onCloseSnackbar: this.onCloseSnackbar,
    };
  }

  onClickImport = () => {
    if (this.state.is_processing) {
      return;
    }

    this.setState(() => ({ is_processing: true }));
    this._importDataService
      .importPrices()
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

  onClickDelete = () => {
    if (this.state.is_processing) {
      return;
    }

    this.setState(() => ({ is_processing: true }));
    this._stockDataService
      .deleteOldPrices()
      .then((resp) => {
        if (resp?.http_status_code === AppConsts.HTTP_STATUS_CODE_OK) {
          this.setState(() => ({
            is_processing: false,
            is_snackbar_open: true,
            snackbar_content: 'Successfully Deleted.',
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
    return <PriceDataMaintTemplate {...this.state} />;
  }
}
