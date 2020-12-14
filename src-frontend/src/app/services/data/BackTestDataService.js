import * as AppConsts from '../../AppConsts';
import BaseDataService from './BaseDataService';

export default class BackTestDataService extends BaseDataService {
  run(req) {
    return this.postJson(`${AppConsts.ROUTE_BACK_TEST}/run`, req);
  }
}
