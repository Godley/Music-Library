/** Pseudo-support for requestFullscreen()
  * Needs a view object with the methods showFullScreen() and showNormal()
  * Won’t support :fullscreen (I used .fullscreen instead)
  * If view doesn’t use document.fullscreenElement to determine what to maximize, anything could be maximized.
  */

'use strict';

document.fullscreenEnabled = true;
document.fullscreenElement = null;

function fullscreenChange() {
	document.dispatchEvent(new CustomEvent('fullscreenchange', {bubbles:true}));
}

document.exitFullscreen = function() {
	document.fullscreenElement.classList.remove('fullscreen');
	document.fullscreenElement = null;
	view.showNormal();
	setTimeout(fullscreenChange, 100);
};

Element.prototype.requestFullscreen = function() {
	this.classList.add('fullscreen');
	document.fullscreenElement = this;
	view.showFullScreen();
	setTimeout(fullscreenChange, 100);