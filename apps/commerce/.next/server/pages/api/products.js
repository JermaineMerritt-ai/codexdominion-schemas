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
exports.id = "pages/api/products";
exports.ids = ["pages/api/products"];
exports.modules = {

/***/ "(api)/./pages/api/products.ts":
/*!*******************************!*\
  !*** ./pages/api/products.ts ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"default\": () => (/* binding */ handler)\n/* harmony export */ });\nfunction handler(req, res) {\n    if (req.method !== \"GET\") {\n        return res.status(405).json({\n            error: \"Method not allowed\"\n        });\n    }\n    const products = [\n        {\n            id: \"prod-1\",\n            name: \"AI Development Suite\",\n            price: 299.99,\n            description: \"Complete AI development toolkit with pre-trained models\"\n        },\n        {\n            id: \"prod-2\",\n            name: \"Healthcare Agent License\",\n            price: 499.99,\n            description: \"Enterprise healthcare automation agent\"\n        },\n        {\n            id: \"prod-3\",\n            name: \"Legal Compliance System\",\n            price: 799.99,\n            description: \"Automated legal compliance and audit system\"\n        },\n        {\n            id: \"prod-4\",\n            name: \"Cybersecurity Shield\",\n            price: 599.99,\n            description: \"Advanced AI-powered cybersecurity monitoring\"\n        },\n        {\n            id: \"prod-5\",\n            name: \"Commerce Analytics Platform\",\n            price: 399.99,\n            description: \"Real-time e-commerce analytics and insights\"\n        },\n        {\n            id: \"prod-6\",\n            name: \"Observatory Dashboard\",\n            price: 199.99,\n            description: \"Comprehensive system monitoring and observability\"\n        }\n    ];\n    res.status(200).json({\n        products\n    });\n}\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiKGFwaSkvLi9wYWdlcy9hcGkvcHJvZHVjdHMudHMiLCJtYXBwaW5ncyI6Ijs7OztBQUVlLFNBQVNBLFFBQVFDLEdBQW1CLEVBQUVDLEdBQW9CO0lBQ3ZFLElBQUlELElBQUlFLE1BQU0sS0FBSyxPQUFPO1FBQ3hCLE9BQU9ELElBQUlFLE1BQU0sQ0FBQyxLQUFLQyxJQUFJLENBQUM7WUFBRUMsT0FBTztRQUFxQjtJQUM1RDtJQUVBLE1BQU1DLFdBQVc7UUFDZjtZQUNFQyxJQUFJO1lBQ0pDLE1BQU07WUFDTkMsT0FBTztZQUNQQyxhQUFhO1FBQ2Y7UUFDQTtZQUNFSCxJQUFJO1lBQ0pDLE1BQU07WUFDTkMsT0FBTztZQUNQQyxhQUFhO1FBQ2Y7UUFDQTtZQUNFSCxJQUFJO1lBQ0pDLE1BQU07WUFDTkMsT0FBTztZQUNQQyxhQUFhO1FBQ2Y7UUFDQTtZQUNFSCxJQUFJO1lBQ0pDLE1BQU07WUFDTkMsT0FBTztZQUNQQyxhQUFhO1FBQ2Y7UUFDQTtZQUNFSCxJQUFJO1lBQ0pDLE1BQU07WUFDTkMsT0FBTztZQUNQQyxhQUFhO1FBQ2Y7UUFDQTtZQUNFSCxJQUFJO1lBQ0pDLE1BQU07WUFDTkMsT0FBTztZQUNQQyxhQUFhO1FBQ2Y7S0FDRDtJQUVEVCxJQUFJRSxNQUFNLENBQUMsS0FBS0MsSUFBSSxDQUFDO1FBQUVFO0lBQVM7QUFDbEMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AY29kZXgtZG9taW5pb24vY29tbWVyY2UvLi9wYWdlcy9hcGkvcHJvZHVjdHMudHM/MzUxNiJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgdHlwZSB7IE5leHRBcGlSZXF1ZXN0LCBOZXh0QXBpUmVzcG9uc2UgfSBmcm9tICduZXh0JztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaGFuZGxlcihyZXE6IE5leHRBcGlSZXF1ZXN0LCByZXM6IE5leHRBcGlSZXNwb25zZSkge1xuICBpZiAocmVxLm1ldGhvZCAhPT0gJ0dFVCcpIHtcbiAgICByZXR1cm4gcmVzLnN0YXR1cyg0MDUpLmpzb24oeyBlcnJvcjogJ01ldGhvZCBub3QgYWxsb3dlZCcgfSk7XG4gIH1cblxuICBjb25zdCBwcm9kdWN0cyA9IFtcbiAgICB7XG4gICAgICBpZDogJ3Byb2QtMScsXG4gICAgICBuYW1lOiAnQUkgRGV2ZWxvcG1lbnQgU3VpdGUnLFxuICAgICAgcHJpY2U6IDI5OS45OSxcbiAgICAgIGRlc2NyaXB0aW9uOiAnQ29tcGxldGUgQUkgZGV2ZWxvcG1lbnQgdG9vbGtpdCB3aXRoIHByZS10cmFpbmVkIG1vZGVscydcbiAgICB9LFxuICAgIHtcbiAgICAgIGlkOiAncHJvZC0yJyxcbiAgICAgIG5hbWU6ICdIZWFsdGhjYXJlIEFnZW50IExpY2Vuc2UnLFxuICAgICAgcHJpY2U6IDQ5OS45OSxcbiAgICAgIGRlc2NyaXB0aW9uOiAnRW50ZXJwcmlzZSBoZWFsdGhjYXJlIGF1dG9tYXRpb24gYWdlbnQnXG4gICAgfSxcbiAgICB7XG4gICAgICBpZDogJ3Byb2QtMycsXG4gICAgICBuYW1lOiAnTGVnYWwgQ29tcGxpYW5jZSBTeXN0ZW0nLFxuICAgICAgcHJpY2U6IDc5OS45OSxcbiAgICAgIGRlc2NyaXB0aW9uOiAnQXV0b21hdGVkIGxlZ2FsIGNvbXBsaWFuY2UgYW5kIGF1ZGl0IHN5c3RlbSdcbiAgICB9LFxuICAgIHtcbiAgICAgIGlkOiAncHJvZC00JyxcbiAgICAgIG5hbWU6ICdDeWJlcnNlY3VyaXR5IFNoaWVsZCcsXG4gICAgICBwcmljZTogNTk5Ljk5LFxuICAgICAgZGVzY3JpcHRpb246ICdBZHZhbmNlZCBBSS1wb3dlcmVkIGN5YmVyc2VjdXJpdHkgbW9uaXRvcmluZydcbiAgICB9LFxuICAgIHtcbiAgICAgIGlkOiAncHJvZC01JyxcbiAgICAgIG5hbWU6ICdDb21tZXJjZSBBbmFseXRpY3MgUGxhdGZvcm0nLFxuICAgICAgcHJpY2U6IDM5OS45OSxcbiAgICAgIGRlc2NyaXB0aW9uOiAnUmVhbC10aW1lIGUtY29tbWVyY2UgYW5hbHl0aWNzIGFuZCBpbnNpZ2h0cydcbiAgICB9LFxuICAgIHtcbiAgICAgIGlkOiAncHJvZC02JyxcbiAgICAgIG5hbWU6ICdPYnNlcnZhdG9yeSBEYXNoYm9hcmQnLFxuICAgICAgcHJpY2U6IDE5OS45OSxcbiAgICAgIGRlc2NyaXB0aW9uOiAnQ29tcHJlaGVuc2l2ZSBzeXN0ZW0gbW9uaXRvcmluZyBhbmQgb2JzZXJ2YWJpbGl0eSdcbiAgICB9XG4gIF07XG5cbiAgcmVzLnN0YXR1cygyMDApLmpzb24oeyBwcm9kdWN0cyB9KTtcbn1cbiJdLCJuYW1lcyI6WyJoYW5kbGVyIiwicmVxIiwicmVzIiwibWV0aG9kIiwic3RhdHVzIiwianNvbiIsImVycm9yIiwicHJvZHVjdHMiLCJpZCIsIm5hbWUiLCJwcmljZSIsImRlc2NyaXB0aW9uIl0sInNvdXJjZVJvb3QiOiIifQ==\n//# sourceURL=webpack-internal:///(api)/./pages/api/products.ts\n");

/***/ })

};
;

// load runtime
var __webpack_require__ = require("../../webpack-api-runtime.js");
__webpack_require__.C(exports);
var __webpack_exec__ = (moduleId) => (__webpack_require__(__webpack_require__.s = moduleId))
var __webpack_exports__ = (__webpack_exec__("(api)/./pages/api/products.ts"));
module.exports = __webpack_exports__;

})();