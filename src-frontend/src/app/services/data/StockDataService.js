import * as AppConsts from '../../AppConsts';

import BaseDataService from './BaseDataService';

export default class StockDataService extends BaseDataService {
  getStockTest() {
    return this.getJson(`${AppConsts.ROUTE_STOCK}/test`);
  }

  getSymbols(instrument = AppConsts.INSTRUMENT_STOCK) {
    return this.getJson(`${AppConsts.ROUTE_STOCK}/get_symbols/${instrument}`);
  }

  updateSymbol(req) {
    return this.postJson(`${AppConsts.ROUTE_STOCK}/update_symbol`, req);
  }

  deleteOldPrices() {
    return this.getJson(`${AppConsts.ROUTE_STOCK}/delete_old_prices`);
  }

  getSamplePricesForCharts(req) {
    return this.postJson(`${AppConsts.ROUTE_STOCK}/get_sample_prices_for_charts`, req);
  }

  getSp500Mismatches(is_missing) {
    return this.getJson(`${AppConsts.ROUTE_STOCK}/get_sp500_mismatches/${is_missing ? 'True' : 'False'}`);
  }
}
