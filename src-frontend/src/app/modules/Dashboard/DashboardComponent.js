import * as AppConsts from '../../AppConsts';

import DashboardTemplate from './DashboardTemplate';
import React from 'react';
import TradeDataService from '../../services/data/TradeDataService';

export default class DashboardComponent extends React.Component {
  constructor(props) {
    super(props);
    this._tradeDataService = new TradeDataService();
    this.state = {
      is_snackbar_open: false,
      snackbar_content: '',
      account: null,
      orders: null,
      onCloseSnackbar: this.onCloseSnackbar,
    };
  }

  componentDidMount() {
    this._tradeDataService
      .getAccount()
      .then((resp) => {
        console.log(resp);
        if (resp?.http_status_code === AppConsts.HTTP_STATUS_CODE_OK) {
          this.setState(() => ({
            account: resp.data.raw,
          }));
        } else {
          this.setState(() => ({
            is_snackbar_open: true,
            snackbar_content: `Error [${resp.http_status_code}]: ${resp.error_message}`,
          }));
        }
      })
      .fail((resp) => {
        console.log(resp);
        this.setState(() => ({
          is_snackbar_open: true,
          snackbar_content: 'ERROR!',
        }));
      });

    this._tradeDataService
      .getTradeOrders({
        status: [
          AppConsts.ORDER_STATUS_SUBMITTED_ENTRY,
          AppConsts.ORDER_STATUS_CANCELLED_ENTRY,
          AppConsts.ORDER_STATUS_IN_POSITION,
          AppConsts.ORDER_STATUS_SUBMITTED_EXIT,
          AppConsts.ORDER_STATUS_CANCELLED_EXIT,
        ],
      })
      .then((resp) => {
        console.log(resp);
        if (resp?.http_status_code === AppConsts.HTTP_STATUS_CODE_OK) {
          this.setState(() => ({
            orders: resp.data,
          }));
        } else {
          this.setState(() => ({
            is_snackbar_open: true,
            snackbar_content: `Error [${resp.http_status_code}]: ${resp.error_message}`,
          }));
        }
      })
      .fail((resp) => {
        console.log(resp);
        this.setState(() => ({
          is_snackbar_open: true,
          snackbar_content: 'ERROR!',
        }));
      });
  }

  onCloseSnackbar = () => {
    this.setState(() => ({ is_snackbar_open: false }));
  };

  render() {
    return <DashboardTemplate {...this.state} />;
  }
}
