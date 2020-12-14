import * as AppConsts from '../../AppConsts';

import BaseDataService from './BaseDataService';

export default class TradeDataService extends BaseDataService {
  getAccount() {
    return this.getJson(`${AppConsts.ROUTE_TRADE}/getAccount`);
  }

  getKeyInfo(symbol) {
    return this.getJson(`${AppConsts.ROUTE_TRADE}/getKeyInfo/${symbol}`);
  }

  getTradeOrders(req) {
    return this.postJson(`${AppConsts.ROUTE_TRADE}/getTradeOrders`, req);
  }

  getSuggestions(req) {
    return this.postJson(`${AppConsts.ROUTE_TRADE}/getSuggestions`, req);
  }
}
