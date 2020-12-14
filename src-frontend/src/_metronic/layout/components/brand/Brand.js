import React, { useMemo } from 'react';
import { Link } from 'react-router-dom';
import SVG from 'react-inlinesvg';
import { useHtmlClassService } from '../../_core/MetronicLayout';
import { toAbsoluteUrl } from '../../../_helpers';

export function Brand() {
  const uiService = useHtmlClassService();

  const layoutProps = useMemo(() => {
    return {
      brandClasses: uiService.getClasses('brand', true),
      headerLogo: uiService.getLogo(),
      headerStickyLogo: uiService.getStickyLogo(),
    };
  }, [uiService]);

  return (
    <>
      {/* begin::Brand */}
      <div className={`brand flex-column-auto ${layoutProps.brandClasses}`} id='kt_brand'>
        {/* begin::Logo */}
        <Link to='' className='brand-logo'>
          <img alt='logo' src={layoutProps.headerLogo} />
        </Link>
        {/* end::Logo */}
      </div>
      {/* end::Brand */}
    </>
  );
}
