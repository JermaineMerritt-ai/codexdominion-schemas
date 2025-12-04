"use strict";
/*
 * ATTENTION: An "eval-source-map" devtool has been used.
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file with attached SourceMaps in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
(() => {
var exports = {};
exports.id = "pages/api/metrics";
exports.ids = ["pages/api/metrics"];
exports.modules = {

/***/ "(api)/./pages/api/metrics.ts":
/*!******************************!*\
  !*** ./pages/api/metrics.ts ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"default\": () => (/* binding */ handler)\n/* harmony export */ });\nfunction handler(req, res) {\n    if (req.method !== \"GET\") {\n        return res.status(405).json({\n            error: \"Method not allowed\"\n        });\n    }\n    const metrics = [\n        {\n            name: \"Requests/sec\",\n            value: 600 + Math.random() * 100,\n            change: (Math.random() - 0.5) * 20,\n            unit: \"\"\n        },\n        {\n            name: \"Response Time\",\n            value: 250 + Math.random() * 100,\n            change: (Math.random() - 0.5) * 15,\n            unit: \"ms\"\n        },\n        {\n            name: \"Error Rate\",\n            value: Math.random() * 2,\n            change: (Math.random() - 0.5) * 10,\n            unit: \"%\"\n        },\n        {\n            name: \"CPU Usage\",\n            value: 45 + Math.random() * 30,\n            change: (Math.random() - 0.5) * 15,\n            unit: \"%\"\n        },\n        {\n            name: \"Memory Usage\",\n            value: 60 + Math.random() * 20,\n            change: (Math.random() - 0.5) * 10,\n            unit: \"%\"\n        },\n        {\n            name: \"Active Users\",\n            value: 1200 + Math.random() * 300,\n            change: (Math.random() - 0.5) * 25,\n            unit: \"\"\n        }\n    ];\n    res.status(200).json({\n        metrics\n    });\n}\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiKGFwaSkvLi9wYWdlcy9hcGkvbWV0cmljcy50cyIsIm1hcHBpbmdzIjoiOzs7O0FBRWUsU0FBU0EsUUFBUUMsR0FBbUIsRUFBRUMsR0FBb0I7SUFDdkUsSUFBSUQsSUFBSUUsTUFBTSxLQUFLLE9BQU87UUFDeEIsT0FBT0QsSUFBSUUsTUFBTSxDQUFDLEtBQUtDLElBQUksQ0FBQztZQUFFQyxPQUFPO1FBQXFCO0lBQzVEO0lBRUEsTUFBTUMsVUFBVTtRQUNkO1lBQ0VDLE1BQU07WUFDTkMsT0FBTyxNQUFNQyxLQUFLQyxNQUFNLEtBQUs7WUFDN0JDLFFBQVEsQ0FBQ0YsS0FBS0MsTUFBTSxLQUFLLEdBQUUsSUFBSztZQUNoQ0UsTUFBTTtRQUNSO1FBQ0E7WUFDRUwsTUFBTTtZQUNOQyxPQUFPLE1BQU1DLEtBQUtDLE1BQU0sS0FBSztZQUM3QkMsUUFBUSxDQUFDRixLQUFLQyxNQUFNLEtBQUssR0FBRSxJQUFLO1lBQ2hDRSxNQUFNO1FBQ1I7UUFDQTtZQUNFTCxNQUFNO1lBQ05DLE9BQU9DLEtBQUtDLE1BQU0sS0FBSztZQUN2QkMsUUFBUSxDQUFDRixLQUFLQyxNQUFNLEtBQUssR0FBRSxJQUFLO1lBQ2hDRSxNQUFNO1FBQ1I7UUFDQTtZQUNFTCxNQUFNO1lBQ05DLE9BQU8sS0FBS0MsS0FBS0MsTUFBTSxLQUFLO1lBQzVCQyxRQUFRLENBQUNGLEtBQUtDLE1BQU0sS0FBSyxHQUFFLElBQUs7WUFDaENFLE1BQU07UUFDUjtRQUNBO1lBQ0VMLE1BQU07WUFDTkMsT0FBTyxLQUFLQyxLQUFLQyxNQUFNLEtBQUs7WUFDNUJDLFFBQVEsQ0FBQ0YsS0FBS0MsTUFBTSxLQUFLLEdBQUUsSUFBSztZQUNoQ0UsTUFBTTtRQUNSO1FBQ0E7WUFDRUwsTUFBTTtZQUNOQyxPQUFPLE9BQU9DLEtBQUtDLE1BQU0sS0FBSztZQUM5QkMsUUFBUSxDQUFDRixLQUFLQyxNQUFNLEtBQUssR0FBRSxJQUFLO1lBQ2hDRSxNQUFNO1FBQ1I7S0FDRDtJQUVEWCxJQUFJRSxNQUFNLENBQUMsS0FBS0MsSUFBSSxDQUFDO1FBQUVFO0lBQVE7QUFDakMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AY29kZXgtZG9taW5pb24vb2JzZXJ2YXRvcnkvLi9wYWdlcy9hcGkvbWV0cmljcy50cz9lZDY5Il0sInNvdXJjZXNDb250ZW50IjpbImltcG9ydCB0eXBlIHsgTmV4dEFwaVJlcXVlc3QsIE5leHRBcGlSZXNwb25zZSB9IGZyb20gJ25leHQnO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBoYW5kbGVyKHJlcTogTmV4dEFwaVJlcXVlc3QsIHJlczogTmV4dEFwaVJlc3BvbnNlKSB7XG4gIGlmIChyZXEubWV0aG9kICE9PSAnR0VUJykge1xuICAgIHJldHVybiByZXMuc3RhdHVzKDQwNSkuanNvbih7IGVycm9yOiAnTWV0aG9kIG5vdCBhbGxvd2VkJyB9KTtcbiAgfVxuXG4gIGNvbnN0IG1ldHJpY3MgPSBbXG4gICAge1xuICAgICAgbmFtZTogJ1JlcXVlc3RzL3NlYycsXG4gICAgICB2YWx1ZTogNjAwICsgTWF0aC5yYW5kb20oKSAqIDEwMCxcbiAgICAgIGNoYW5nZTogKE1hdGgucmFuZG9tKCkgLSAwLjUpICogMjAsXG4gICAgICB1bml0OiAnJ1xuICAgIH0sXG4gICAge1xuICAgICAgbmFtZTogJ1Jlc3BvbnNlIFRpbWUnLFxuICAgICAgdmFsdWU6IDI1MCArIE1hdGgucmFuZG9tKCkgKiAxMDAsXG4gICAgICBjaGFuZ2U6IChNYXRoLnJhbmRvbSgpIC0gMC41KSAqIDE1LFxuICAgICAgdW5pdDogJ21zJ1xuICAgIH0sXG4gICAge1xuICAgICAgbmFtZTogJ0Vycm9yIFJhdGUnLFxuICAgICAgdmFsdWU6IE1hdGgucmFuZG9tKCkgKiAyLFxuICAgICAgY2hhbmdlOiAoTWF0aC5yYW5kb20oKSAtIDAuNSkgKiAxMCxcbiAgICAgIHVuaXQ6ICclJ1xuICAgIH0sXG4gICAge1xuICAgICAgbmFtZTogJ0NQVSBVc2FnZScsXG4gICAgICB2YWx1ZTogNDUgKyBNYXRoLnJhbmRvbSgpICogMzAsXG4gICAgICBjaGFuZ2U6IChNYXRoLnJhbmRvbSgpIC0gMC41KSAqIDE1LFxuICAgICAgdW5pdDogJyUnXG4gICAgfSxcbiAgICB7XG4gICAgICBuYW1lOiAnTWVtb3J5IFVzYWdlJyxcbiAgICAgIHZhbHVlOiA2MCArIE1hdGgucmFuZG9tKCkgKiAyMCxcbiAgICAgIGNoYW5nZTogKE1hdGgucmFuZG9tKCkgLSAwLjUpICogMTAsXG4gICAgICB1bml0OiAnJSdcbiAgICB9LFxuICAgIHtcbiAgICAgIG5hbWU6ICdBY3RpdmUgVXNlcnMnLFxuICAgICAgdmFsdWU6IDEyMDAgKyBNYXRoLnJhbmRvbSgpICogMzAwLFxuICAgICAgY2hhbmdlOiAoTWF0aC5yYW5kb20oKSAtIDAuNSkgKiAyNSxcbiAgICAgIHVuaXQ6ICcnXG4gICAgfVxuICBdO1xuXG4gIHJlcy5zdGF0dXMoMjAwKS5qc29uKHsgbWV0cmljcyB9KTtcbn1cbiJdLCJuYW1lcyI6WyJoYW5kbGVyIiwicmVxIiwicmVzIiwibWV0aG9kIiwic3RhdHVzIiwianNvbiIsImVycm9yIiwibWV0cmljcyIsIm5hbWUiLCJ2YWx1ZSIsIk1hdGgiLCJyYW5kb20iLCJjaGFuZ2UiLCJ1bml0Il0sInNvdXJjZVJvb3QiOiIifQ==\n//# sourceURL=webpack-internal:///(api)/./pages/api/metrics.ts\n");

/***/ })

};
;

// load runtime
var __webpack_require__ = require("../../webpack-api-runtime.js");
__webpack_require__.C(exports);
var __webpack_exec__ = (moduleId) => (__webpack_require__(__webpack_require__.s = moduleId))
var __webpack_exports__ = (__webpack_exec__("(api)/./pages/api/metrics.ts"));
module.exports = __webpack_exports__;

})();
