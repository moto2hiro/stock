import React, { useLayoutEffect } from 'react';

import KTLayoutContent from '../../_assets/js/layout/base/content';
import KTLayoutFooter from '../../_assets/js/layout/base/footer';
import KTLayoutHeader from '../../_assets/js/layout/base/header';
import KTLayoutHeaderMenu from '../../_assets/js/layout/base/header-menu';
import KTLayoutHeaderTopbar from '../../_assets/js/layout/base/header-topbar';
import KTLayoutQuickUser from '../../_assets/js/layout/extended/quick-user';
import KTLayoutScrolltop from '../../_assets/js/layout/extended/scrolltop';
import KTLayoutSubheader from '../../_assets/js/layout/base/subheader';
import { KTUtil } from '../../_assets/js/components/util';

export function LayoutInit() {
  useLayoutEffect(() => {
    // Initialization
    KTUtil.ready(function() {
      ////////////////////////////////////////////////////
      // Layout Base Partials(mandatory for core layout)//
      ////////////////////////////////////////////////////
      // Init Desktop & Mobile Headers
      KTLayoutHeader.init('kt_header', 'kt_header_mobile');

      // Init Header Menu
      KTLayoutHeaderMenu.init('kt_header_menu', 'kt_header_menu_wrapper');
      // Init Header Topbar For Mobile Mode
      KTLayoutHeaderTopbar.init('kt_header_mobile_topbar_toggle');

      // Init subheader
      KTLayoutSubheader.init('kt_subheader');

      // Init Content
      KTLayoutContent.init('kt_content');

      // Init Footer
      KTLayoutFooter.init('kt_footer');

      //////////////////////////////////////////////
      // Layout Extended Partials(optional to use)//
      //////////////////////////////////////////////

      // Init Scrolltop
      KTLayoutScrolltop.init('kt_scrolltop');

      // Init Quick User Panel
      KTLayoutQuickUser.init('kt_quick_user');
    });
  }, []);
  return <></>;
}
