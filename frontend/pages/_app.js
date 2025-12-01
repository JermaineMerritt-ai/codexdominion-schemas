"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var styled_components_1 = require("styled-components");
var theme_1 = require("../theme");
function MyApp(_a) {
    var Component = _a.Component, pageProps = _a.pageProps;
    return (<styled_components_1.ThemeProvider theme={theme_1.theme}>
      <Component {...pageProps}/>
    </styled_components_1.ThemeProvider>);
}
exports.default = MyApp;
