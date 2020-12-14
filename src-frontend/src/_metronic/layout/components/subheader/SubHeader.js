/* eslint-disable no-script-url,jsx-a11y/anchor-is-valid */

import React, { useEffect, useLayoutEffect, useMemo } from 'react';
import { getBreadcrumbsAndTitle, useSubheader } from '../../_core/MetronicSubheader';

import { BreadCrumbs } from './components/BreadCrumbs';
import objectPath from 'object-path';
import { useHtmlClassService } from '../../_core/MetronicLayout';
import { useLocation } from 'react-router-dom';

export function SubHeader() {
  const uiService = useHtmlClassService();
  const location = useLocation();
  const subheader = useSubheader();

  const layoutProps = useMemo(() => {
    return {
      config: uiService.config,
      subheaderMobileToggle: objectPath.get(uiService.config, 'subheader.mobile-toggle'),
      subheaderCssClasses: uiService.getClasses('subheader', true),
      subheaderContainerCssClasses: uiService.getClasses('subheader_container', true),
    };
  }, [uiService]);

  useLayoutEffect(() => {
    const header = getBreadcrumbsAndTitle('kt_header_menu', location.pathname);
    let breadcrumbs = [];
    breadcrumbs = header.breadcrumbs;

    subheader.setBreadcrumbs(breadcrumbs);
    subheader.setTitle(header.title);
    // eslint-disable-next-line
  }, [location.pathname]);

  // Do not remove this useEffect, need from update title/breadcrumbs outside (from the page)
  useEffect(() => {}, [subheader]);

  return (
    <div id='kt_subheader' className={`subheader py-2 py-lg-4   ${layoutProps.subheaderCssClasses}`}>
      <div
        className={`${layoutProps.subheaderContainerCssClasses} d-flex align-items-center justify-content-between flex-wrap flex-sm-nowrap`}
      >
        {/* Info */}
        <div className='d-flex align-items-center flex-wrap mr-1'>
          {/* begin::Mobile Toggle */}
          {layoutProps.subheaderMobileToggle && (
            <button
              className='burger-icon burger-icon-left mr-4 d-inline-block d-lg-none'
              id='kt_subheader_mobile_toggle'
            >
              <span />
            </button>
          )}
          {/* end::Mobile Toggle */}

          {/* begin::Heading */}
          <div className='d-flex flex-column'>
            {/* begin::Title */}
            <h2 className='text-white font-weight-bold my-2 mr-5'>{subheader.title}</h2>
            {/* end::Title */}

            <BreadCrumbs items={subheader.breadcrumbs} />
          </div>
          {/* end::Heading */}
        </div>
      </div>
    </div>
  );
}
