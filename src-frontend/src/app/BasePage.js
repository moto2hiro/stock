import { ContentRoute, LayoutSplashScreen } from '../_metronic/layout';
import React, { Suspense } from 'react';
import { Redirect, Switch } from 'react-router-dom';

import BackTestComponent from './modules/BackTest/BackTestComponent';
import ChartSandboxComponent from './modules/ChartSandbox/ChartSandboxComponent';
import DashboardComponent from './modules/Dashboard/DashboardComponent';
import PriceDataMaintComponent from './modules/Maintenance/PriceData/PriceDataMaintComponent';
import Sp500MaintComponent from './modules/Maintenance/Sp500/Sp500MaintComponent';
import SymbolsMaintComponent from './modules/Maintenance/Symbols/SymbolsMaintComponent';
import TradeSuggestionsComponent from './modules/Trade/TradeSuggestions/TradeSuggestionsComponent';

export default function BasePage() {
  return (
    <Suspense fallback={<LayoutSplashScreen />}>
      <Switch>
        {<Redirect exact from='/' to='/dashboard' />}
        <ContentRoute path='/dashboard' component={DashboardComponent} />
        <ContentRoute path='/backTest' component={BackTestComponent} />
        <ContentRoute path='/chartSandbox' component={ChartSandboxComponent} />
        <ContentRoute path='/maintenance/symbols' component={SymbolsMaintComponent} />
        <ContentRoute path='/maintenance/pricedata' component={PriceDataMaintComponent} />
        <ContentRoute path='/maintenance/sp500' component={Sp500MaintComponent} />
        <ContentRoute path='/trade/suggestions' component={TradeSuggestionsComponent} />
        <Redirect to='error/error-v1' />
      </Switch>
    </Suspense>
  );
}
