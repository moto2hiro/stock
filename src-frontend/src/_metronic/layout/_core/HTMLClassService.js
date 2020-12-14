import objectPath from 'object-path';
import { toAbsoluteUrl } from '../../_helpers';

export class HtmlClassService {
  // Public properties
  config;
  classes;
  attributes;

  /**
   * Build html element classes from layout config
   * @param layoutConfig
   */
  setConfig(layoutConfig) {
    this.config = layoutConfig;

    // scope list of classes
    this.classes = {
      header: [],
      header_container: [],
      header_mobile: [],
      header_menu: [],
      subheader: [],
      subheader_container: [],
      content: [],
      content_container: [],
      footer_container: [],
    };

    this.attributes = {
      header_mobile: {},
      header_menu: {},
    };

    // init base layout
    this.initLoader();
    this.initLayout();

    // init header and subheader menu
    this.initHeader();
    this.initSubheader();

    this.initContent();

    // init footer
    this.initFooter();
  }

  /**
   * Returns Classes
   *
   * @param path: string
   * @param toString boolean
   */
  getClasses(path, toString) {
    if (path) {
      const classes = objectPath.get(this.classes, path) || '';
      if (toString && Array.isArray(classes)) {
        return classes.join(' ');
      }
      return classes.toString();
    }
    return this.classes;
  }

  getAttributes(path) {
    if (path) {
      const attributes = objectPath.get(this.attributes, path) || [];
      return attributes;
    }
    return [];
  }

  getLogo() {
    const brandSkin = objectPath.get(this.config, 'brand.self.theme');
    if (brandSkin === 'light') {
      return toAbsoluteUrl('/media/logos/logo-dark.png');
    } else {
      return toAbsoluteUrl('/media/logos/logo-light.png');
    }
  }

  getStickyLogo() {
    let logo = objectPath.get(this.config, 'self.logo.sticky');
    if (typeof logo === 'undefined') {
      logo = this.getLogo();
    }
    return logo + '';
  }

  /**
   * Init Layout
   */
  initLayout() {
    const selfBodyBackgroundImage = objectPath.get(this.config, 'self.body.backgroundImage');
    if (selfBodyBackgroundImage) {
      const backgroundImageUrl = `${toAbsoluteUrl('/media/' + selfBodyBackgroundImage)}`;
      document.body.style.backgroundImage = `url("${backgroundImageUrl}")`;
    }

    const _selfBodyClass = objectPath.get(this.config, 'self.body.class');
    if (_selfBodyClass) {
      const bodyClasses = _selfBodyClass.toString().split(' ');
      bodyClasses.forEach((cssClass) => document.body.classList.add(cssClass));
    }

    // Offcanvas directions
    document.body.classList.add('quick-panel-right');
    document.body.classList.add('demo-panel-right');
    document.body.classList.add('offcanvas-right');
  }

  /**
   * Init Loader
   */
  initLoader() {}

  /**
   * Init Header
   */
  initHeader() {
    // Fixed header
    const headerSelfFixedDesktop = objectPath.get(this.config, 'header.self.fixed.desktop');
    if (headerSelfFixedDesktop) {
      document.body.classList.add('header-fixed');
      objectPath.push(this.classes, 'header', 'header-fixed');
    } else {
      document.body.classList.add('header-static');
    }

    const headerSelfFixedMobile = objectPath.get(this.config, 'header.self.fixed.mobile');
    if (headerSelfFixedMobile) {
      document.body.classList.add('header-mobile-fixed');
      objectPath.push(this.classes, 'header_mobile', 'header-mobile-fixed');
    }

    // Menu
    const headerMenuSelfDisplay = objectPath.get(this.config, 'header.menu.self.display');
    if (headerMenuSelfDisplay) {
      const headerMenuSelfLayout = objectPath.get(this.config, 'header.menu.self.layout');
      const headerMenuLayoutCssClass = `header-menu-layout-${headerMenuSelfLayout}`;
      objectPath.push(this.classes, 'header_menu', headerMenuLayoutCssClass);

      if (objectPath.get(this.config, 'header.menu.self.root-arrow')) {
        objectPath.push(this.classes, 'header_menu', 'header-menu-root-arrow');
      }
    }

    const headerSelfWidth = objectPath.get(this.config, 'header.self.width');
    if (headerSelfWidth === 'fluid') {
      objectPath.push(this.classes, 'header_container', 'container-fluid');
    } else {
      objectPath.push(this.classes, 'header_container', 'container');
    }
  }

  /**
   * Init Subheader
   */
  initSubheader() {
    const subheaderDisplay = objectPath.get(this.config, 'subheader.display');
    if (subheaderDisplay) {
      document.body.classList.add('subheader-enabled');
    } else {
      return;
    }

    // Fixed content head
    const subheaderFixed = objectPath.get(this.config, 'subheader.fixed');
    const headerSelfFixedDesktop = objectPath.get(this.config, 'header.self.fixed.desktop');
    if (subheaderFixed && headerSelfFixedDesktop) {
      document.body.classList.add('subheader-fixed');
      // Page::setOption('layout', 'subheader/style', 'solid'); => See preInit()
    } else {
      // Page::setOption('layout', 'subheader/fixed', false); => See preInit()
    }

    const subheaderStyle = objectPath.get(this.config, 'subheader.style');
    if (subheaderStyle) {
      const subheaderClass = `subheader-${subheaderStyle}`;
      objectPath.push(this.classes, 'subheader', subheaderClass);
    }

    const subheaderWidth = objectPath.get(this.config, 'subheader.width');
    if (subheaderWidth === 'fluid') {
      objectPath.push(this.classes, 'subheader_container', 'container-fluid');
    } else {
      objectPath.push(this.classes, 'subheader_container', 'container');
    }
  }

  /**
   * Init Content
   */
  initContent() {
    if (objectPath.get(this.config, 'content.fit-top')) {
      objectPath.push(this.classes, 'content', 'pt-0');
    }

    if (objectPath.get(this.config, 'content.fit-bottom')) {
      objectPath.push(this.classes, 'content', 'pb-0');
    }

    if (objectPath.get(this.config, 'content.width') === 'fluid') {
      objectPath.push(this.classes, 'content_container', 'container-fluid');
    } else {
      objectPath.push(this.classes, 'content_container', 'container');
    }
  }

  /**
   * Init Footer
   */
  initFooter() {
    if (objectPath.get(this.config, 'footer.width') === 'fluid') {
      objectPath.push(this.classes, 'footer_container', 'container-fluid');
    } else {
      objectPath.push(this.classes, 'footer_container', 'container');
    }
  }
}
