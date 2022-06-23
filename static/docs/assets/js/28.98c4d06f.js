(window.webpackJsonp=window.webpackJsonp||[]).push([[28],{211:function(t,s,a){"use strict";a.r(s);var o=a(0),e=Object(o.a)({},(function(){var t=this.$createElement;this._self._c;return this._m(0)}),[function(){var t=this,s=t.$createElement,a=t._self._c||s;return a("div",{staticClass:"content"},[a("h1",{attrs:{id:"motors"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#motors"}},[t._v("#")]),t._v(" Motors")]),t._v(" "),a("p",[t._v("Motors can be used for all sorts of things, besides just moving your robot. For instance, they could also be used as part of a mechanism to collect cubes. However you decide to use them, they're really simple to control.")]),t._v(" "),a("p",[t._v("When you control motors, you can choose how much power you want to give them. This is expressed as a percentage, so 0% means a stopped motor and 100% means a motor at full power.")]),t._v(" "),a("div",{staticClass:"tip custom-block"},[a("p",{staticClass:"custom-block-title"},[t._v("TIP")]),t._v(" "),a("p",[t._v("If you have large motors you should avoid using 100% power when the motor is stalled or stationary, otherwise the rush of current may cause the robot to shut down the motor output. Instead of jumping from 0% to 100% start at a lower value such as 50% and work your way up.")])]),t._v(" "),a("p",[t._v("If you want to spin your motors in reverse, just stick a negative sign in front of your percentage.")]),t._v(" "),a("h2",{attrs:{id:"python"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#python"}},[t._v("#")]),t._v(" Python")]),t._v(" "),a("p",[t._v("You can control motors using the "),a("code",[t._v("motors")]),t._v(" property of the "),a("code",[t._v("Robot")]),t._v(" object. To set the power of the first motor to 60% use:")]),t._v(" "),a("div",{staticClass:"language-python extra-class"},[a("pre",{pre:!0,attrs:{class:"language-python"}},[a("code",[t._v("R"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("motors"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("[")]),a("span",{pre:!0,attrs:{class:"token number"}},[t._v("1")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("]")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token number"}},[t._v("60")]),t._v("\n")])])]),a("div",{staticClass:"warning custom-block"},[a("p",{staticClass:"custom-block-title"},[t._v("WARNING")]),t._v(" "),a("p",[t._v("If you are using the mini-bot or similar motors. Do not exceed a motor power of 25% otherwise they will burn out.")])]),t._v(" "),a("p",[t._v("To control the second motor instead, replace "),a("code",[t._v("motors[1]")]),t._v(" with "),a("code",[t._v("motors[2]")]),t._v(".")]),t._v(" "),a("p",[t._v("To stop both motors:")]),t._v(" "),a("div",{staticClass:"language-python extra-class"},[a("pre",{pre:!0,attrs:{class:"language-python"}},[a("code",[t._v("R"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("motors"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("[")]),a("span",{pre:!0,attrs:{class:"token number"}},[t._v("1")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("]")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token number"}},[t._v("0")]),t._v("\nR"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("motors"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("[")]),a("span",{pre:!0,attrs:{class:"token number"}},[t._v("2")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("]")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token number"}},[t._v("0")]),t._v("\n")])])]),a("p",[t._v("Here's a more complete example:")]),t._v(" "),a("div",{staticClass:"language-python extra-class"},[a("pre",{pre:!0,attrs:{class:"language-python"}},[a("code",[a("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("import")]),t._v(" robot\n\nR "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" robot"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("Robot"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n\n"),a("span",{pre:!0,attrs:{class:"token comment"}},[t._v("# set motor 1 to 60% power")]),t._v("\nR"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("motors"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("[")]),a("span",{pre:!0,attrs:{class:"token number"}},[t._v("1")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("]")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token number"}},[t._v("60")]),t._v("\n\n"),a("span",{pre:!0,attrs:{class:"token comment"}},[t._v("# set motor 2 to 60% power in the backwards direction")]),t._v("\nR"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("motors"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("[")]),a("span",{pre:!0,attrs:{class:"token number"}},[t._v("2")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("]")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("-")]),a("span",{pre:!0,attrs:{class:"token number"}},[t._v("60")]),t._v("\n\n"),a("span",{pre:!0,attrs:{class:"token comment"}},[t._v("# turn both motors off")]),t._v("\nR"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("motors"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("[")]),a("span",{pre:!0,attrs:{class:"token number"}},[t._v("1")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("]")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token number"}},[t._v("0")]),t._v("\nR"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("motors"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("[")]),a("span",{pre:!0,attrs:{class:"token number"}},[t._v("2")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("]")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token number"}},[t._v("0")]),t._v("\n")])])]),a("h2",{attrs:{id:"blockly"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#blockly"}},[t._v("#")]),t._v(" Blockly")]),t._v(" "),a("p",[t._v("Blocks for controlling motors can be found in the "),a("strong",[t._v("Movement")]),t._v(" section.")]),t._v(" "),a("h1",{attrs:{id:"using-larger-motors-than-supplied"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#using-larger-motors-than-supplied"}},[t._v("#")]),t._v(" Using larger motors than supplied")]),t._v(" "),a("p",[t._v("The Brainbox outputs 12v pulses and by default is restricted to 25% for safe use with the 6v motors, if you wish to use other motors you may wish to change the maximum duty cycle, for example 12v motors may accept 100% duty cycles.\nYou can use any motors you like with the brain box as long as the total current requested does not exceed 20A.")]),t._v(" "),a("p",[t._v("The maximum motor current is a feature of the robot and can only be set when first initilizing the robot object")]),t._v(" "),a("div",{staticClass:"language-python extra-class"},[a("pre",{pre:!0,attrs:{class:"language-python"}},[a("code",[a("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("import")]),t._v(" robot\n\nR "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" robot"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("Robot"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),t._v("motor_max"),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),a("span",{pre:!0,attrs:{class:"token number"}},[t._v("100")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n")])])])])}],!1,null,null,null);s.default=e.exports}}]);