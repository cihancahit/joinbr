!function(e){if("object"==typeof exports&&"undefined"!=typeof module)module.exports=e();else if("function"==typeof define&&define.amd)define([],e);else{("undefined"!=typeof window?window:"undefined"!=typeof global?global:"undefined"!=typeof self?self:this).raterJs=e()}}(function(){return function(){return function e(t,n,r){function i(s,o){if(!n[s]){if(!t[s]){var l="function"==typeof require&&require;if(!o&&l)return l(s,!0);if(a)return a(s,!0);var u=new Error("Cannot find module '"+s+"'");throw u.code="MODULE_NOT_FOUND",u}var c=n[s]={exports:{}};t[s][0].call(c.exports,function(e){return i(t[s][1][e]||e)},c,c.exports,e,t,n,r)}return n[s].exports}for(var a="function"==typeof require&&require,s=0;s<r.length;s++)i(r[s]);return i}}()({1:[function(e,t,n){"use strict";e("./style.css");t.exports=function(e){var t=!0;if(void 0===e.element||null===e.element)throw new Error("element required");if(void 0!==e.showToolTip&&(t=!!e.showToolTip),void 0!==e.step&&(e.step<=0||e.step>1))throw new Error("step must be a number between 0 and 1");var n,r=e.element,i=e.reverse,a=e.max||5,s=e.starSize||16,o=e.step||1,l=e.onHover,u=e.onLeave,c=null;r.classList.add("star-rating");var d=document.createElement("div");d.classList.add("star-value"),i&&d.classList.add("rtl"),d.style.backgroundSize=s+"px",r.appendChild(d),r.style.width=s*a+"px",r.style.height=s+"px",r.style.backgroundSize=s+"px";var f,v,p,m=e.rateCallback,h=!!e.readOnly,g=!1,b=e.isBusyText;if(f=void 0!==e.disableText?e.disableText:"{rating}/{maxRating}",p=void 0!==e.ratingText?e.ratingText:"{rating}/{maxRating}",e.rating)T(e.rating);else{var y=r.dataset.rating;y&&T(+y)}function w(e){x(e,!1)}function x(e,n){if(!0!==h&&!0!==g){var s,u=r.offsetWidth,d=r.getBoundingClientRect();if(i)s=(u-(n?e.changedTouches[0].pageX-d.left:e.pageX-window.scrollX-d.left))/(u/100);else s=(n?e.changedTouches[0].pageX-d.left:e.offsetX)/u*100;if(s<101){if(1===o)v=Math.ceil(s/100*a);else for(var f=s/100*a,m=0;;m+=o)if(m>=f){v=m;break}if(v>a&&(v=a),r.querySelector(".star-value").style.width=v/a*100+"%",t){var b=p.replace("{rating}",v);b=b.replace("{maxRating}",a),r.setAttribute("title",b)}"function"==typeof l&&l(v,c)}}}function E(e){c?(r.querySelector(".star-value").style.width=c/a*100+"%",r.setAttribute("data-rating",c)):(r.querySelector(".star-value").style.width="0%",r.removeAttribute("data-rating")),"function"==typeof u&&u(v,c)}function A(e){!0!==h&&!0!==g&&void 0!==m&&(g=!0,n=v,void 0===b?r.removeAttribute("title"):r.setAttribute("title",b),r.classList.add("is-busy"),m.call(this,n,function(){!1===h&&r.removeAttribute("title"),g=!1,r.classList.remove("is-busy")}))}function L(){if(h=!0,r.classList.add("disabled"),t&&f){var e=f.replace("{rating}",c||0);e=e.replace("{maxRating}",a),r.setAttribute("title",e)}else r.removeAttribute("title")}function T(e){if(void 0===e)throw new Error("Value not set.");if(null===e)throw new Error("Value cannot be null.");if("number"!=typeof e)throw new Error("Value must be a number.");if(e<0||e>a)throw new Error("Value too high. Please set a rating of "+a+" or below.");c=e,r.querySelector(".star-value").style.width=e/a*100+"%",r.setAttribute("data-rating",e),console.log(r.getElementsByClassName("stars")),r.getElementsByClassName("stars")[0].value=c}c||(r.querySelector(".star-value").style.width="0px"),h&&L(),r.addEventListener("mousemove",w),r.addEventListener("mouseleave",E);var S={setRating:T,getRating:function(){return c},disable:L,enable:function(){h=!1,r.removeAttribute("title"),r.classList.remove("disabled")},clear:function(){c=null,r.querySelector(".star-value").style.width="0px",r.removeAttribute("title")},dispose:function(){r.removeEventListener("mousemove",w),r.removeEventListener("mouseleave",E),r.removeEventListener("click",A),r.removeEventListener("touchmove",k,!1),r.removeEventListener("touchstart",q,!1),r.removeEventListener("touchend",C,!1),r.removeEventListener("touchcancel",X,!1)},get element(){return r}};function k(e){e.preventDefault(),x(e,!0)}function q(e){e.preventDefault(),x(e,!0)}function C(e){e.preventDefault(),x(e,!0),A.call(S)}function X(e){e.preventDefault(),E()}return r.addEventListener("click",A.bind(S)),r.addEventListener("touchmove",k,!1),r.addEventListener("touchstart",q,!1),r.addEventListener("touchend",C,!1),r.addEventListener("touchcancel",X,!1),S}},{"./style.css":2}],2:[function(e,t,n){var r='.star-rating {\n  width: 0;\n  position: relative;\n  display: inline-block;\n background-position: 0 0;\n  background-repeat: repeat-x;\n  cursor: pointer;\n}\n.star-rating .star-value {\n  position: absolute;\n  height: 100%;\n  width: 100%;\n  background-repeat: repeat-x;\n}\n.star-rating.disabled {\n  cursor: default;\n}\n.star-rating.is-busy {\n  cursor: wait;\n}\n.star-rating .star-value.rtl {\n  -moz-transform: scaleX(-1);\n  -o-transform: scaleX(-1);\n  -webkit-transform: scaleX(-1);\n  transform: scaleX(-1);\n  filter: FlipH;\n  -ms-filter: "FlipH";\n  right: 0;\n  left: auto;\n}\n';e("browserify-css").createStyle(r,{href:"lib\\style.css"},{insertAt:"bottom"}),t.exports=r},{"browserify-css":3}],3:[function(e,t,n){"use strict";var r=[],i=function(e,t){var n=document.head||document.getElementsByTagName("head")[0],i=r[r.length-1];if((t=t||{}).insertAt=t.insertAt||"bottom","top"===t.insertAt)i?i.nextSibling?n.insertBefore(e,i.nextSibling):n.appendChild(e):n.insertBefore(e,n.firstChild),r.push(e);else{if("bottom"!==t.insertAt)throw new Error("Invalid value for parameter 'insertAt'. Must be 'top' or 'bottom'.");n.appendChild(e)}};t.exports={createLink:function(e,t){var n=document.head||document.getElementsByTagName("head")[0],r=document.createElement("link");for(var i in r.href=e,r.rel="stylesheet",t)if(t.hasOwnProperty(i)){var a=t[i];r.setAttribute("data-"+i,a)}n.appendChild(r)},createStyle:function(e,t,n){n=n||{};var r=document.createElement("style");for(var a in r.type="text/css",t)if(t.hasOwnProperty(a)){var s=t[a];r.setAttribute("data-"+a,s)}r.sheet?(r.innerHTML=e,r.sheet.cssText=e,i(r,{insertAt:n.insertAt})):r.styleSheet?(i(r,{insertAt:n.insertAt}),r.styleSheet.cssText=e):(r.appendChild(document.createTextNode(e)),i(r,{insertAt:n.insertAt}))}}},{}]},{},[1])(1)});