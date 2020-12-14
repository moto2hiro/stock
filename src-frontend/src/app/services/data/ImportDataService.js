import * as AppConsts from '../../AppConsts';

import BaseDataService from './BaseDataService';

export default class ImportDataService extends BaseDataService {
  importSymbols() {
    return this.getJson(`${AppConsts.ROUTE_IMPORT}/symbols`);
  }

  importPrices() {
    return this.getJson(`${AppConsts.ROUTE_IMPORT}/prices`);
  }
}
