/* eslint-disable no-script-url,jsx-a11y/anchor-is-valid */

import { NavLink } from 'react-router-dom';
import React from 'react';
import { checkIsActive } from '../../../../_helpers';
import { useLocation } from 'react-router';

export function HeaderMenu({ layoutProps }) {
  const location = useLocation();
  const getMenuItemActive = (url) => {
    return checkIsActive(location, url) ? 'menu-item-active' : '';
  };

  return (
    <div
      id='kt_header_menu'
      className={`header-menu header-menu-left header-menu-mobile ${layoutProps.ktMenuClasses}`}
      {...layoutProps.headerMenuAttributes}
    >
      <ul className={`menu-nav ${layoutProps.ulClasses}`}>
        <li className={`menu-item menu-item-rel ${getMenuItemActive('/dashboard')}`}>
          <NavLink className='menu-link' to='/dashboard'>
            <span className='menu-text'>Dashboard</span>
            {layoutProps.rootArrowEnabled && <i className='menu-arrow' />}
          </NavLink>
        </li>
        <li className={`menu-item menu-item-rel ${getMenuItemActive('/backtest')}`}>
          <NavLink className='menu-link' to='/backtest'>
            <span className='menu-text'>Back Test</span>
            {layoutProps.rootArrowEnabled && <i className='menu-arrow' />}
          </NavLink>
        </li>
        <li className={`menu-item menu-item-rel ${getMenuItemActive('/chartSandbox')}`}>
          <NavLink className='menu-link' to='/chartSandbox'>
            <span className='menu-text'>Chart Sandbox</span>
            {layoutProps.rootArrowEnabled && <i className='menu-arrow' />}
          </NavLink>
        </li>
        <li
          data-menu-toggle={layoutProps.menuDesktopToggle}
          aria-haspopup='true'
          className={`menu-item menu-item-submenu menu-item-rel ${getMenuItemActive('/trade')}`}
        >
          <NavLink className='menu-link menu-toggle' to='/trade'>
            <span className='menu-text'>Trade</span>
            <i className='menu-arrow'></i>
          </NavLink>
          <div className='menu-submenu menu-submenu-classic menu-submenu-left'>
            <ul className='menu-subnav'>
              <li className={`menu-item ${getMenuItemActive('/trade/suggestions')}`}>
                <NavLink className='menu-link' to='/trade/suggestions'>
                  <span className='menu-text'>Trade Suggestions</span>
                </NavLink>
              </li>
            </ul>
          </div>
        </li>
        <li
          data-menu-toggle={layoutProps.menuDesktopToggle}
          aria-haspopup='true'
          className={`menu-item menu-item-submenu menu-item-rel ${getMenuItemActive('/maintenance')}`}
        >
          <NavLink className='menu-link menu-toggle' to='/maintenance'>
            <span className='menu-text'>Maintenance</span>
            <i className='menu-arrow'></i>
          </NavLink>
          <div className='menu-submenu menu-submenu-classic menu-submenu-left'>
            <ul className='menu-subnav'>
              <li className={`menu-item ${getMenuItemActive('/maintenance/symbols')}`}>
                <NavLink className='menu-link' to='/maintenance/symbols'>
                  <span className='menu-text'>Symbols</span>
                </NavLink>
              </li>
              <li className={`menu-item ${getMenuItemActive('/maintenance/pricedata')}`}>
                <NavLink className='menu-link' to='/maintenance/pricedata'>
                  <span className='menu-text'>Price Data</span>
                </NavLink>
              </li>
              <li className={`menu-item ${getMenuItemActive('/maintenance/sp500')}`}>
                <NavLink className='menu-link' to='/maintenance/sp500'>
                  <span className='menu-text'>SP 500</span>
                </NavLink>
              </li>
            </ul>
          </div>
        </li>
      </ul>
    </div>
  );
}
